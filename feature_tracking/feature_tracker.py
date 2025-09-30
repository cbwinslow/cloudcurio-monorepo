"""
CloudCurio Feature Tracking Library

A comprehensive library for tracking feature usage, performance, 
and effectiveness across the platform.
"""

import time
import functools
import json
import uuid
from datetime import datetime
from typing import Any, Dict, Callable, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import threading
from pathlib import Path


class FeatureStatus(Enum):
    """Status of a feature execution"""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    TIMEOUT = "timeout"


class FeatureCategory(Enum):
    """Categories of features to track"""
    AI_PROVIDER = "ai_provider"
    MCP_SERVER = "mcp_server"
    SYSMON = "sysmon"
    CONFIG_EDITOR = "config_editor"
    AGENT_PLATFORM = "agentic_platform"
    WEB_INTERFACE = "web_interface"
    TERMINAL_TOOL = "terminal_tool"
    FILE_OPERATION = "file_operation"
    DATABASE_OPERATION = "database_operation"
    OTHER = "other"


@dataclass
class FeatureUsageRecord:
    """Represents a single feature usage record"""
    record_id: str
    feature_name: str
    category: FeatureCategory
    status: FeatureStatus
    duration: float  # in seconds
    start_time: datetime
    end_time: datetime
    input_size: int
    output_size: int
    metadata: Dict[str, Any]
    user_id: Optional[str]
    session_id: str
    error_message: Optional[str] = None
    efficiency_score: Optional[float] = None  # 0-1 scale
    iterations: int = 1  # Number of iterations in the feature execution


class FeatureTrackerDB:
    """Database manager for feature tracking"""
    
    def __init__(self, db_path: str = "~/.cloudcurio/feature_tracking.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_db()
    
    def _init_db(self):
        """Initialize the tracking database"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create feature usage table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS feature_usage (
                        id TEXT PRIMARY KEY,
                        feature_name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        status TEXT NOT NULL,
                        duration REAL NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT NOT NULL,
                        input_size INTEGER DEFAULT 0,
                        output_size INTEGER DEFAULT 0,
                        metadata TEXT,  -- JSON string
                        user_id TEXT,
                        session_id TEXT NOT NULL,
                        error_message TEXT,
                        efficiency_score REAL,
                        iterations INTEGER DEFAULT 1
                    )
                ''')
                
                # Create indexes for faster queries
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_feature_name ON feature_usage(feature_name)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON feature_usage(category)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_start_time ON feature_usage(start_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON feature_usage(user_id)')
                
                conn.commit()
    
    def insert_record(self, record: FeatureUsageRecord):
        """Insert a feature usage record"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO feature_usage (
                        id, feature_name, category, status, duration, 
                        start_time, end_time, input_size, output_size, 
                        metadata, user_id, session_id, error_message, 
                        efficiency_score, iterations
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record.record_id,
                    record.feature_name,
                    record.category.value,
                    record.status.value,
                    record.duration,
                    record.start_time.isoformat(),
                    record.end_time.isoformat(),
                    record.input_size,
                    record.output_size,
                    json.dumps(record.metadata),
                    record.user_id,
                    record.session_id,
                    record.error_message,
                    record.efficiency_score,
                    record.iterations
                ))
                
                conn.commit()
    
    def get_records(self, 
                   feature_name: Optional[str] = None,
                   category: Optional[FeatureCategory] = None,
                   user_id: Optional[str] = None,
                   limit: int = 100) -> List[FeatureUsageRecord]:
        """Retrieve feature usage records"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM feature_usage WHERE 1=1"
                params = []
                
                if feature_name:
                    query += " AND feature_name = ?"
                    params.append(feature_name)
                
                if category:
                    query += " AND category = ?"
                    params.append(category.value)
                
                if user_id:
                    query += " AND user_id = ?"
                    params.append(user_id)
                
                query += " ORDER BY start_time DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                
                records = []
                for row in cursor.fetchall():
                    record = FeatureUsageRecord(
                        record_id=row[0],
                        feature_name=row[1],
                        category=FeatureCategory(row[2]),
                        status=FeatureStatus(row[3]),
                        duration=row[4],
                        start_time=datetime.fromisoformat(row[5]),
                        end_time=datetime.fromisoformat(row[6]),
                        input_size=row[7],
                        output_size=row[8],
                        metadata=json.loads(row[9]) if row[9] else {},
                        user_id=row[10],
                        session_id=row[11],
                        error_message=row[12],
                        efficiency_score=row[13],
                        iterations=row[14]
                    )
                    records.append(record)
                
                return records
    
    def get_usage_stats(self, 
                       feature_name: Optional[str] = None,
                       category: Optional[FeatureCategory] = None) -> Dict[str, Any]:
        """Get usage statistics for features"""
        with self._lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT 
                        COUNT(*) as total_calls,
                        AVG(duration) as avg_duration,
                        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
                        SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failure_count,
                        AVG(efficiency_score) as avg_efficiency
                    FROM feature_usage
                    WHERE 1=1
                """
                params = []
                
                if feature_name:
                    query += " AND feature_name = ?"
                    params.append(feature_name)
                
                if category:
                    query += " AND category = ?"
                    params.append(category.value)
                
                cursor.execute(query, params)
                result = cursor.fetchone()
                
                return {
                    'total_calls': result[0] or 0,
                    'avg_duration': result[1] or 0,
                    'success_count': result[2] or 0,
                    'failure_count': result[3] or 0,
                    'avg_efficiency': result[4] or 0,
                    'success_rate': (result[2] or 0) / (result[0] or 1) * 100
                }


class FeatureTracker:
    """Main feature tracking system"""
    
    def __init__(self, db_path: str = "~/.cloudcurio/feature_tracking.db"):
        self.db = FeatureTrackerDB(db_path)
        self.current_session_id = str(uuid.uuid4())
        
        # Thread-local storage for tracking context
        self._local = threading.local()
    
    def _calculate_efficiency(self, duration: float, output_size: int, iterations: int) -> float:
        """Calculate efficiency score based on performance metrics"""
        # Simple efficiency calculation - can be enhanced based on specific requirements
        # Factors: duration (inversely), output size (directly), iterations (inversely)
        if duration <= 0:
            return 1.0  # Perfect efficiency for instantaneous operations
        
        # Normalize the values (example implementation)
        # This is a basic formula, can be made more sophisticated
        duration_factor = max(0, min(1, 1.0 / (duration * 0.1)))  # Faster is better
        output_factor = min(1, output_size / 1000)  # Larger output may mean more value
        iteration_factor = max(0, min(1, 1.0 / iterations))  # Fewer iterations may mean more efficiency
        
        efficiency = (duration_factor * 0.5 + output_factor * 0.3 + iteration_factor * 0.2)
        return min(1.0, max(0.0, efficiency))
    
    def track_feature(self, 
                     feature_name: str,
                     category: FeatureCategory,
                     user_id: Optional[str] = None,
                     input_data: Optional[Any] = None,
                     output_data: Optional[Any] = None) -> Callable:
        """
        Decorator to track feature usage.
        Usage: @tracker.track_feature("feature_name", FeatureCategory.AI_PROVIDER)
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_datetime = datetime.now()
                
                # Prepare metadata
                metadata = {
                    'function_args': [repr(arg) for arg in args],
                    'function_kwargs': {k: repr(v) for k, v in kwargs.items()},
                    'thread_id': threading.get_ident(),
                    'function_name': func.__name__
                }
                
                input_size = len(str(input_data)) if input_data is not None else 0
                iterations = 1  # Default, can be overridden by the function if needed
                
                record_id = str(uuid.uuid4())
                session_id = getattr(self._local, 'session_id', self.current_session_id)
                
                try:
                    result = func(*args, **kwargs)
                    
                    end_time = time.time()
                    duration = end_time - start_time
                    end_datetime = datetime.now()
                    
                    status = FeatureStatus.SUCCESS
                    error_message = None
                    output_size = len(str(result)) if result is not None else 0
                    
                    # Calculate efficiency
                    efficiency_score = self._calculate_efficiency(duration, output_size, iterations)
                    
                    # Create and store the record
                    record = FeatureUsageRecord(
                        record_id=record_id,
                        feature_name=feature_name,
                        category=category,
                        status=status,
                        duration=duration,
                        start_time=start_datetime,
                        end_time=end_datetime,
                        input_size=input_size,
                        output_size=output_size,
                        metadata=metadata,
                        user_id=user_id,
                        session_id=session_id,
                        error_message=error_message,
                        efficiency_score=efficiency_score,
                        iterations=iterations
                    )
                    
                    self.db.insert_record(record)
                    
                    return result
                    
                except Exception as e:
                    end_time = time.time()
                    duration = end_time - start_time
                    end_datetime = datetime.now()
                    
                    status = FeatureStatus.FAILED
                    error_message = str(e)
                    output_size = 0
                    
                    # Even for failures, calculate efficiency (likely low)
                    efficiency_score = self._calculate_efficiency(duration, output_size, iterations)
                    
                    # Create and store the record
                    record = FeatureUsageRecord(
                        record_id=record_id,
                        feature_name=feature_name,
                        category=category,
                        status=status,
                        duration=duration,
                        start_time=start_datetime,
                        end_time=end_datetime,
                        input_size=input_size,
                        output_size=output_size,
                        metadata=metadata,
                        user_id=user_id,
                        session_id=session_id,
                        error_message=error_message,
                        efficiency_score=efficiency_score,
                        iterations=iterations
                    )
                    
                    self.db.insert_record(record)
                    
                    # Re-raise the exception
                    raise e
            
            return wrapper
        return decorator
    
    def start_custom_tracking(self, 
                             feature_name: str,
                             category: FeatureCategory,
                             user_id: Optional[str] = None,
                             metadata: Optional[Dict[str, Any]] = None) -> str:
        """Start custom tracking for complex operations"""
        record_id = str(uuid.uuid4())
        session_id = getattr(self._local, 'session_id', self.current_session_id)
        
        # Store tracking context for later completion
        tracking_context = {
            'record_id': record_id,
            'feature_name': feature_name,
            'category': category,
            'user_id': user_id,
            'session_id': session_id,
            'start_time': datetime.now(),
            'start_timestamp': time.time(),
            'metadata': metadata or {}
        }
        
        setattr(self._local, f'tracking_{record_id}', tracking_context)
        return record_id
    
    def complete_custom_tracking(self, 
                                record_id: str,
                                status: FeatureStatus,
                                input_size: int = 0,
                                output_size: int = 0,
                                error_message: Optional[str] = None,
                                efficiency_score: Optional[float] = None,
                                iterations: int = 1):
        """Complete custom tracking for complex operations"""
        tracking_context = getattr(self._local, f'tracking_{record_id}', None)
        
        if not tracking_context:
            raise ValueError(f"No tracking context found for ID: {record_id}")
        
        start_time = tracking_context['start_timestamp']
        end_time = time.time()
        duration = end_time - start_time
        
        # Calculate efficiency if not provided
        if efficiency_score is None:
            efficiency_score = self._calculate_efficiency(duration, output_size, iterations)
        
        # Create and store the record
        record = FeatureUsageRecord(
            record_id=record_id,
            feature_name=tracking_context['feature_name'],
            category=tracking_context['category'],
            status=status,
            duration=duration,
            start_time=tracking_context['start_time'],
            end_time=datetime.now(),
            input_size=input_size,
            output_size=output_size,
            metadata=tracking_context['metadata'],
            user_id=tracking_context['user_id'],
            session_id=tracking_context['session_id'],
            error_message=error_message,
            efficiency_score=efficiency_score,
            iterations=iterations
        )
        
        self.db.insert_record(record)
        
        # Clean up the tracking context
        delattr(self._local, f'tracking_{record_id}')
    
    def get_feature_stats(self,  # Get statistics for a feature
                         feature_name: str,
                         category: Optional[FeatureCategory] = None) -> Dict[str, Any]:
        """Get statistics for a specific feature"""
        return self.db.get_usage_stats(feature_name, category)
    
    def get_all_records(self, 
                       feature_name: Optional[str] = None,
                       category: Optional[FeatureCategory] = None,
                       user_id: Optional[str] = None,
                       limit: int = 100) -> List[FeatureUsageRecord]:
        """Get all feature usage records"""
        return self.db.get_records(feature_name, category, user_id, limit)
    
    def get_top_features(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top features by usage count"""
        with self.db._lock:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT 
                        feature_name,
                        category,
                        COUNT(*) as usage_count,
                        AVG(duration) as avg_duration,
                        AVG(efficiency_score) as avg_efficiency,
                        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count
                    FROM feature_usage
                    GROUP BY feature_name, category
                    ORDER BY usage_count DESC
                    LIMIT ?
                """
                
                cursor.execute(query, (limit,))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'feature_name': row[0],
                        'category': row[1],
                        'usage_count': row[2],
                        'avg_duration': row[3],
                        'avg_efficiency': row[4],
                        'success_count': row[5],
                        'success_rate': (row[5] / row[2]) * 100 if row[2] > 0 else 0
                    })
                
                return results


# Global feature tracker instance
feature_tracker = FeatureTracker()


# Convenience decorator for easy use
def track_feature(feature_name: str, 
                category: FeatureCategory,
                user_id: Optional[str] = None,
                input_data: Optional[Any] = None,
                output_data: Optional[Any] = None):
    """
    Decorator to track feature usage.
    
    Usage:
    @track_feature("my_feature", FeatureCategory.AI_PROVIDER)
    def my_function():
        pass
    """
    return feature_tracker.track_feature(feature_name, category, user_id, input_data, output_data)


# Example usage of the feature tracking system
if __name__ == "__main__":
    print("CloudCurio Feature Tracking Library")
    print("==================================")
    
    # Example 1: Decorator usage
    @track_feature("example_function", FeatureCategory.AI_PROVIDER)
    def example_function(x, y):
        time.sleep(0.1)  # Simulate work
        return x + y
    
    # Call the tracked function
    result = example_function(5, 3)
    print(f"Function result: {result}")
    
    # Example 2: Manual tracking for complex operations
    tracker = FeatureTracker()
    
    # Start tracking
    record_id = tracker.start_custom_tracking(
        "complex_operation", 
        FeatureCategory.SYSMON,
        user_id="user123",
        metadata={"operation_type": "config_analysis"}
    )
    
    # Simulate a complex operation
    time.sleep(0.2)
    success = True
    
    # Complete tracking
    if success:
        tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.SUCCESS,
            input_size=1000,
            output_size=500,
            iterations=1
        )
    else:
        tracker.complete_custom_tracking(
            record_id,
            FeatureStatus.FAILED,
            error_message="Operation failed due to timeout"
        )
    
    # Get statistics
    stats = tracker.get_feature_stats("example_function")
    print(f"Feature stats: {stats}")
    
    # Get top features
    top_features = tracker.get_top_features(5)
    print(f"Top features: {top_features}")
    
    print("Feature tracking is ready to use across the CloudCurio platform!")