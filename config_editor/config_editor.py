"""
CloudCurio Config Editor - Web-based Configuration Management System

This module provides a web interface for managing system configurations,
recording user actions with Puppeteer, and training AI models to automate
similar tasks in the future.
"""

import os
import json
import sqlite3
import threading
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Web framework imports
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Puppeteer automation
import asyncio
from pyppeteer import launch

# AI/ML for action classification
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Local imports
from ..sysmon.sysmon import DatabaseManager, EventType, SystemEvent


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of actions that can be recorded"""
    DOWNLOAD_SOFTWARE = "download_software"
    INSTALL_SOFTWARE = "install_software"
    CONFIGURE_SERVICE = "configure_service"
    CREATE_API_KEY = "create_api_key"
    MODIFY_CONFIG_FILE = "modify_config_file"
    ADD_REPOSITORY = "add_repository"
    REMOVE_SOFTWARE = "remove_software"
    START_SERVICE = "start_service"
    STOP_SERVICE = "stop_service"
    OTHER = "other"


@dataclass
class RecordedAction:
    """Represents a recorded user action"""
    id: Optional[int]
    action_type: ActionType
    timestamp: datetime
    description: str
    url: Optional[str]  # For web-based actions
    selector: Optional[str]  # CSS selector for the element
    data: Dict[str, Any]  # Additional data specific to the action
    session_id: str  # Session in which the action was recorded
    step_group: Optional[str]  # Group this action belongs to
    confidence: float  # AI confidence in classification


class ActionDatabase:
    """Manages the database for recorded actions"""
    
    def __init__(self, db_path: str = "~/.cloudcurio/config_editor.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create actions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    description TEXT NOT NULL,
                    url TEXT,
                    selector TEXT,
                    data TEXT,  -- JSON string
                    session_id TEXT NOT NULL,
                    step_group TEXT,
                    confidence REAL DEFAULT 0.0
                )
            ''')
            
            # Create downloads table to track software downloads
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS software_downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    download_url TEXT NOT NULL,
                    download_path TEXT,
                    timestamp TEXT NOT NULL,
                    version TEXT,
                    source TEXT  -- where it was downloaded from
                )
            ''')
            
            # Create step_groups table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS step_groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    category TEXT,  -- e.g., "API key creation", "Service installation"
                    timestamp TEXT NOT NULL,
                    is_template BOOLEAN DEFAULT 0  -- Can be reused for automation
                )
            ''')
            
            # Create indexes for faster queries
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON actions(session_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_action_type ON actions(action_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_step_group ON actions(step_group)')
            
            conn.commit()
    
    def insert_action(self, action: RecordedAction) -> int:
        """Insert an action into the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO actions (action_type, timestamp, description, url, selector, data, session_id, step_group, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                action.action_type.value,
                action.timestamp.isoformat(),
                action.description,
                action.url,
                action.selector,
                json.dumps(action.data),
                action.session_id,
                action.step_group,
                action.confidence
            ))
            
            action_id = cursor.lastrowid
            conn.commit()
            return action_id
    
    def insert_download(self, name: str, download_url: str, version: str = None, source: str = None):
        """Insert a software download record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO software_downloads (name, download_url, timestamp, version, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                name,
                download_url,
                datetime.now().isoformat(),
                version,
                source
            ))
            
            conn.commit()
    
    def get_actions(self, session_id: str = None, limit: int = 100) -> List[RecordedAction]:
        """Retrieve actions from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if session_id:
                cursor.execute('''
                    SELECT id, action_type, timestamp, description, url, selector, data, session_id, step_group, confidence
                    FROM actions
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (session_id, limit))
            else:
                cursor.execute('''
                    SELECT id, action_type, timestamp, description, url, selector, data, session_id, step_group, confidence
                    FROM actions
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            actions = []
            for row in cursor.fetchall():
                action = RecordedAction(
                    id=row[0],
                    action_type=ActionType(row[1]),
                    timestamp=datetime.fromisoformat(row[2]),
                    description=row[3],
                    url=row[4],
                    selector=row[5],
                    data=json.loads(row[6]) if row[6] else {},
                    session_id=row[7],
                    step_group=row[8],
                    confidence=row[9]
                )
                actions.append(action)
            
            return actions
    
    def create_step_group(self, name: str, description: str, category: str):
        """Create a new step group in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO step_groups (name, description, category, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (name, description, category, datetime.now().isoformat()))
            
            conn.commit()
    
    def get_step_groups(self) -> List[Dict[str, Any]]:
        """Retrieve all step groups"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT name, description, category, timestamp FROM step_groups ORDER BY timestamp DESC')
            
            groups = []
            for row in cursor.fetchall():
                groups.append({
                    "name": row[0],
                    "description": row[1],
                    "category": row[2],
                    "timestamp": row[3]
                })
            
            return groups


class ActionClassifier:
    """AI-powered classifier for action categorization"""
    
    def __init__(self):
        # Load a pre-trained sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define action categories and their representative phrases
        self.categories = {
            "API Key Creation": [
                "create api key",
                "generate api token",
                "get api key",
                "set up authentication",
                "create credentials",
                "authentication token",
                "access key",
                "secret key"
            ],
            "Software Installation": [
                "install software",
                "download package",
                "install application",
                "setup program",
                "add software",
                "get application"
            ],
            "Service Configuration": [
                "configure service",
                "setup server",
                "configure settings",
                "change configuration",
                "modify service",
                "service settings"
            ],
            "Account Creation": [
                "create account",
                "sign up",
                "register",
                "new user",
                "create profile",
                "set up account"
            ]
        }
        
        # Encode category phrases
        self.category_embeddings = {}
        for category, phrases in self.categories.items():
            embeddings = self.model.encode(phrases)
            self.category_embeddings[category] = np.mean(embeddings, axis=0)
    
    def classify_action(self, description: str) -> tuple[str, float]:
        """
        Classify an action based on its description.
        Returns a tuple of (category, confidence).
        """
        # Encode the description
        desc_embedding = self.model.encode([description])[0]
        
        # Calculate similarity to each category
        best_category = "Other"
        best_similarity = 0.0
        
        for category, category_embedding in self.category_embeddings.items():
            similarity = np.dot(desc_embedding, category_embedding) / (
                np.linalg.norm(desc_embedding) * np.linalg.norm(category_embedding)
            )
            if similarity > best_similarity:
                best_similarity = similarity
                best_category = category
        
        return best_category, float(best_similarity)


class PuppeteerController:
    """Controls Puppeteer for browser automation and action recording"""
    
    def __init__(self):
        self.browser = None
        self.current_page = None
        self.is_recording = False
        self.session_id = None
        self.action_db = ActionDatabase()
        self.action_classifier = ActionClassifier()
        self.recorded_actions = []
    
    async def start_browser(self):
        """Start the Puppeteer browser instance"""
        self.browser = await launch(headless=False, args=['--no-sandbox', '--disable-setuid-sandbox'])
        self.current_page = await self.browser.newPage()
        return self.current_page
    
    async def start_recording(self, session_id: str = None):
        """Start recording user actions"""
        if not self.browser:
            await self.start_browser()
        
        self.session_id = session_id or f"session_{int(time.time())}"
        self.is_recording = True
        
        # Add listeners to track user interactions
        await self.current_page.on('click', self._on_click)
        await self.current_page.on('change', self._on_change)
        await self.current_page.on('load', self._on_load)
        
        logger.info(f"Started recording session: {self.session_id}")
    
    async def stop_recording(self):
        """Stop recording user actions"""
        self.is_recording = False
        logger.info(f"Stopped recording session: {self.session_id}")
    
    async def _on_click(self, element):
        """Handle click events"""
        if not self.is_recording:
            return
        
        try:
            # Get element information
            tag_name = await element.getProperty('tagName')
            class_name = await element.getProperty('className')
            text_content = await element.getProperty('textContent')
            
            tag_name_val = await tag_name.jsonValue()
            class_name_val = await class_name.jsonValue() if class_name else ""
            text_content_val = await text_content.jsonValue() if text_content else ""
            
            # Create action description
            description = f"Clicked on {tag_name_val} element"
            if class_name_val:
                description += f" with class '{class_name_val}'"
            if text_content_val.strip():
                description += f" containing '{text_content_val.strip()[:50]}...'"
            
            # Determine action type based on context
            url = await self.current_page.url()
            action_type = self._determine_action_type(description, url)
            
            # Classify the action
            category, confidence = self.action_classifier.classify_action(description)
            
            # Record the action
            action = RecordedAction(
                id=None,
                action_type=action_type,
                timestamp=datetime.now(),
                description=description,
                url=url,
                selector=None,  # TODO: extract actual CSS selector
                data={
                    "tag_name": tag_name_val,
                    "class_name": class_name_val,
                    "text_content": text_content_val
                },
                session_id=self.session_id,
                step_group=category if confidence > 0.5 else None,
                confidence=confidence
            )
            
            action_id = self.action_db.insert_action(action)
            action.id = action_id
            
            self.recorded_actions.append(action)
            logger.info(f"Recorded action: {description} (confidence: {confidence:.2f})")
        except Exception as e:
            logger.error(f"Error recording click action: {e}")
    
    async def _on_change(self, element):
        """Handle change events (form inputs, etc.)"""
        if not self.is_recording:
            return
        
        try:
            # Get element information
            tag_name = await element.getProperty('tagName')
            name = await element.getProperty('name')
            value = await element.getProperty('value')
            
            tag_name_val = await tag_name.jsonValue()
            name_val = await name.jsonValue() if name else ""
            value_val = await value.jsonValue() if value else ""
            
            description = f"Changed {tag_name_val}"
            if name_val:
                description += f" with name '{name_val}'"
            if value_val:
                description += f" to '{value_val[:30]}...'"
            
            # Determine action type
            url = await self.current_page.url()
            action_type = self._determine_action_type(description, url)
            
            # Classify the action
            category, confidence = self.action_classifier.classify_action(description)
            
            # Record the action
            action = RecordedAction(
                id=None,
                action_type=action_type,
                timestamp=datetime.now(),
                description=description,
                url=url,
                selector=None,
                data={
                    "tag_name": tag_name_val,
                    "name": name_val,
                    "value": value_val
                },
                session_id=self.session_id,
                step_group=category if confidence > 0.5 else None,
                confidence=confidence
            )
            
            action_id = self.action_db.insert_action(action)
            action.id = action_id
            
            self.recorded_actions.append(action)
            logger.info(f"Recorded change action: {description} (confidence: {confidence:.2f})")
        except Exception as e:
            logger.error(f"Error recording change action: {e}")
    
    async def _on_load(self, frame):
        """Handle page load events"""
        if not self.is_recording:
            return
        
        try:
            url = await self.current_page.url()
            title = await self.current_page.title()
            
            description = f"Page loaded: {title} ({url})"
            
            # Record the action
            action = RecordedAction(
                id=None,
                action_type=ActionType.OTHER,
                timestamp=datetime.now(),
                description=description,
                url=url,
                selector=None,
                data={
                    "title": title
                },
                session_id=self.session_id,
                step_group=None,
                confidence=0.0
            )
            
            action_id = self.action_db.insert_action(action)
            action.id = action_id
            
            self.recorded_actions.append(action)
            logger.info(f"Recorded page load: {description}")
        except Exception as e:
            logger.error(f"Error recording load action: {e}")
    
    def _determine_action_type(self, description: str, url: str) -> ActionType:
        """Determine the action type based on description and URL"""
        desc_lower = description.lower()
        url_lower = url.lower()
        
        # Check for software installation actions
        if any(keyword in desc_lower for keyword in ["install", "download", "package", "setup"]):
            return ActionType.INSTALL_SOFTWARE
        
        # Check for API key creation
        if any(keyword in desc_lower for keyword in ["api key", "token", "credential", "auth"]):
            return ActionType.CREATE_API_KEY
        
        # Check for service configuration
        if any(keyword in desc_lower for keyword in ["configure", "setting", "config", "service"]):
            return ActionType.CONFIGURE_SERVICE
        
        # Check for repository addition
        if any(keyword in desc_lower for keyword in ["repo", "repository", "source", "add"]):
            return ActionType.ADD_REPOSITORY
        
        # Default to other
        return ActionType.OTHER


class ConfigEditorAPI:
    """API for the configuration editor"""
    
    def __init__(self):
        self.app = FastAPI(title="CloudCurio Config Editor API")
        self.db = ActionDatabase()
        self.puppeteer_controller = PuppeteerController()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def read_root():
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>CloudCurio Config Editor</title>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100">
                <div class="container mx-auto px-4 py-8">
                    <h1 class="text-3xl font-bold text-center mb-8">CloudCurio Config Editor</h1>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Service Management -->
                        <div class="bg-white p-6 rounded-lg shadow">
                            <h2 class="text-xl font-semibold mb-4">Service Management</h2>
                            <div id="services-list" class="space-y-2">
                                <!-- Services will be loaded here -->
                            </div>
                            <button id="scan-ports-btn" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded">Scan Active Ports</button>
                        </div>
                        
                        <!-- Program Management -->
                        <div class="bg-white p-6 rounded-lg shadow">
                            <h2 class="text-xl font-semibold mb-4">Program Management</h2>
                            <div id="programs-list" class="space-y-2">
                                <!-- Programs will be loaded here -->
                            </div>
                            <button id="scan-programs-btn" class="mt-4 bg-green-500 text-white px-4 py-2 rounded">Scan Installed Programs</button>
                        </div>
                        
                        <!-- Action Recording -->
                        <div class="bg-white p-6 rounded-lg shadow">
                            <h2 class="text-xl font-semibold mb-4">Action Recording</h2>
                            <div class="flex space-x-2">
                                <button id="start-recording-btn" class="flex-1 bg-yellow-500 text-white px-4 py-2 rounded">Start Recording</button>
                                <button id="stop-recording-btn" class="flex-1 bg-red-500 text-white px-4 py-2 rounded">Stop Recording</button>
                            </div>
                            <div id="recording-status" class="mt-4 p-2 bg-gray-200 rounded hidden">
                                Recording... Session: <span id="session-id"></span>
                            </div>
                            <div class="mt-4">
                                <h3 class="font-medium mb-2">Recent Actions:</h3>
                                <div id="recent-actions" class="space-y-1 max-h-40 overflow-y-auto"></div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Step Groups -->
                    <div class="mt-8 bg-white p-6 rounded-lg shadow">
                        <h2 class="text-xl font-semibold mb-4">Step Groups</h2>
                        <div id="step-groups" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            <!-- Step groups will be loaded here -->
                        </div>
                    </div>
                    
                    <script>
                        // Function to scan active ports
                        async function scanActivePorts() {
                            try {
                                const response = await fetch('/api/ports');
                                const ports = await response.json();
                                const servicesList = document.getElementById('services-list');
                                servicesList.innerHTML = '';
                                
                                ports.forEach(port => {
                                    const div = document.createElement('div');
                                    div.className = 'p-2 bg-gray-100 rounded';
                                    div.textContent = `${port.service} (${port.port}) - ${port.status}`;
                                    servicesList.appendChild(div);
                                });
                            } catch (error) {
                                console.error('Error scanning ports:', error);
                            }
                        }
                        
                        // Function to scan installed programs
                        async function scanInstalledPrograms() {
                            try {
                                const response = await fetch('/api/programs');
                                const programs = await response.json();
                                const programsList = document.getElementById('programs-list');
                                programsList.innerHTML = '';
                                
                                programs.forEach(program => {
                                    const div = document.createElement('div');
                                    div.className = 'p-2 bg-gray-100 rounded';
                                    div.textContent = `${program.name} - ${program.version}`;
                                    programsList.appendChild(div);
                                });
                            } catch (error) {
                                console.error('Error scanning programs:', error);
                            }
                        }
                        
                        // Function to start recording
                        async function startRecording() {
                            try {
                                const response = await fetch('/api/recording/start', { method: 'POST' });
                                const result = await response.json();
                                
                                if (result.success) {
                                    document.getElementById('recording-status').classList.remove('hidden');
                                    document.getElementById('session-id').textContent = result.session_id;
                                    document.getElementById('start-recording-btn').disabled = true;
                                    document.getElementById('stop-recording-btn').disabled = false;
                                }
                            } catch (error) {
                                console.error('Error starting recording:', error);
                            }
                        }
                        
                        // Function to stop recording
                        async function stopRecording() {
                            try {
                                const response = await fetch('/api/recording/stop', { method: 'POST' });
                                const result = await response.json();
                                
                                if (result.success) {
                                    document.getElementById('recording-status').classList.add('hidden');
                                    document.getElementById('start-recording-btn').disabled = false;
                                    document.getElementById('stop-recording-btn').disabled = true;
                                }
                            } catch (error) {
                                console.error('Error stopping recording:', error);
                            }
                        }
                        
                        // Function to load recent actions
                        async function loadRecentActions() {
                            try {
                                const response = await fetch('/api/actions');
                                const actions = await response.json();
                                const actionsList = document.getElementById('recent-actions');
                                actionsList.innerHTML = '';
                                
                                actions.slice(0, 10).forEach(action => {
                                    const div = document.createElement('div');
                                    div.className = 'text-sm p-1 bg-gray-100 rounded';
                                    div.textContent = `[${new Date(action.timestamp).toLocaleTimeString()}] ${action.description}`;
                                    actionsList.appendChild(div);
                                });
                            } catch (error) {
                                console.error('Error loading recent actions:', error);
                            }
                        }
                        
                        // Function to load step groups
                        async function loadStepGroups() {
                            try {
                                const response = await fetch('/api/step_groups');
                                const groups = await response.json();
                                const groupsContainer = document.getElementById('step-groups');
                                groupsContainer.innerHTML = '';
                                
                                groups.forEach(group => {
                                    const div = document.createElement('div');
                                    div.className = 'p-3 bg-blue-50 rounded border';
                                    div.innerHTML = `
                                        <h3 class="font-medium">${group.name}</h3>
                                        <p class="text-sm text-gray-600">${group.description}</p>
                                        <p class="text-xs text-gray-500">${group.category} - ${new Date(group.timestamp).toLocaleDateString()}</p>
                                    `;
                                    groupsContainer.appendChild(div);
                                });
                            } catch (error) {
                                console.error('Error loading step groups:', error);
                            }
                        }
                        
                        // Set up event listeners
                        document.getElementById('scan-ports-btn').addEventListener('click', scanActivePorts);
                        document.getElementById('scan-programs-btn').addEventListener('click', scanInstalledPrograms);
                        document.getElementById('start-recording-btn').addEventListener('click', startRecording);
                        document.getElementById('stop-recording-btn').addEventListener('click', stopRecording);
                        
                        // Load initial data
                        scanActivePorts();
                        scanInstalledPrograms();
                        loadRecentActions();
                        loadStepGroups();
                        
                        // Refresh recent actions every 5 seconds
                        setInterval(loadRecentActions, 5000);
                    </script>
                </div>
            </body>
            </html>
            """
        
        @self.app.get("/api/ports")
        async def get_active_ports():
            """Get a list of active ports and associated services"""
            try:
                # Use ss or netstat to get listening ports
                result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
                if result.returncode != 0:
                    # Fallback to netstat
                    result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
                
                ports = []
                if result.returncode == 0:
                    for line in result.stdout.split('\n')[1:]:  # Skip header
                        if 'LISTEN' in line:
                            parts = line.split()
                            if len(parts) >= 5:
                                address = parts[4]
                                ip, port = address.split(':')
                                ports.append({
                                    "port": port,
                                    "address": ip,
                                    "status": "LISTENING"
                                })
                
                # Try to identify services for common ports
                common_services = {
                    "22": "SSH",
                    "80": "HTTP",
                    "443": "HTTPS", 
                    "3000": "Web App (Common)",
                    "8000": "Web App (Common)",
                    "8080": "Web App (Common)",
                    "5432": "PostgreSQL",
                    "3306": "MySQL",
                    "6379": "Redis",
                    "27017": "MongoDB"
                }
                
                for port in ports:
                    service_name = common_services.get(port["port"], f"Port {port['port']}")
                    port["service"] = service_name
                
                return ports
            except Exception as e:
                logger.error(f"Error getting active ports: {e}")
                return []
        
        @self.app.get("/api/programs")
        async def get_installed_programs():
            """Get a list of installed programs"""
            programs = []
            
            try:
                # Try apt (Debian/Ubuntu)
                result = subprocess.run(['dpkg', '--get-selections'], 
                                      capture_output=True, text=True, check=True)
                for line in result.stdout.split('\n'):
                    if '\tinstall' in line:
                        package = line.split()[0]
                        if ':' in package:
                            package = package.split(':')[0]
                        programs.append({"name": package, "version": "unknown", "manager": "apt"})
            except subprocess.CalledProcessError:
                pass  # Continue to try other package managers
            
            try:
                # Try rpm (Red Hat/CentOS/Fedora)
                result = subprocess.run(['rpm', '-qa'], 
                                      capture_output=True, text=True, check=True)
                for pkg in result.stdout.strip().split('\n'):
                    if pkg:
                        programs.append({"name": pkg, "version": "unknown", "manager": "rpm"})
            except subprocess.CalledProcessError:
                pass
            
            try:
                # Try pacman (Arch Linux)
                result = subprocess.run(['pacman', '-Q'], 
                                      capture_output=True, text=True, check=True)
                for line in result.stdout.split('\n'):
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            programs.append({"name": parts[0], "version": parts[1], "manager": "pacman"})
            except subprocess.CalledProcessError:
                pass
            
            try:
                # Try pip
                result = subprocess.run(['pip', 'list', '--format', 'freeze'], 
                                      capture_output=True, text=True, check=True)
                for line in result.stdout.strip().split('\n'):
                    if line and not line.startswith('#'):
                        if '==' in line:
                            name, version = line.split('==', 1)
                            programs.append({"name": name, "version": version, "manager": "pip"})
            except subprocess.CalledProcessError:
                pass
            
            return programs[:50]  # Limit to first 50 programs
        
        @self.app.post("/api/recording/start")
        async def start_recording():
            """Start action recording"""
            try:
                session_id = f"session_{int(time.time())}"
                await self.puppeteer_controller.start_recording(session_id)
                return {"success": True, "session_id": session_id}
            except Exception as e:
                logger.error(f"Error starting recording: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.post("/api/recording/stop")
        async def stop_recording():
            """Stop action recording"""
            try:
                await self.puppeteer_controller.stop_recording()
                return {"success": True}
            except Exception as e:
                logger.error(f"Error stopping recording: {e}")
                return {"success": False, "error": str(e)}
        
        @self.app.get("/api/actions")
        async def get_recent_actions():
            """Get recent recorded actions"""
            try:
                actions = self.db.get_actions(limit=20)
                return [asdict(action) for action in actions]
            except Exception as e:
                logger.error(f"Error getting recent actions: {e}")
                return []
        
        @self.app.get("/api/step_groups")
        async def get_step_groups():
            """Get all step groups"""
            try:
                return self.db.get_step_groups()
            except Exception as e:
                logger.error(f"Error getting step groups: {e}")
                return []
    
    def run(self, host: str = "0.0.0.0", port: int = 8081):
        """Run the API server"""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)


# Example usage
if __name__ == "__main__":
    print("Starting CloudCurio Config Editor...")
    
    # Initialize and run the API
    api = ConfigEditorAPI()
    
    print("CloudCurio Config Editor is running on http://localhost:8081")
    print("Features:")
    print("- Web interface for service and program management")
    print("- Action recording with Puppeteer")
    print("- AI-powered action categorization")
    print("- Step group management")
    
    api.run()