# CloudCurio: The Sentient Homelab Project

Welcome to CloudCurio, a project dedicated to creating a self-managing, self-documenting, and self-improving personal computing ecosystem. This repository is the central nervous system for a **Sentient Homelab**, an ambitious initiative to blend advanced AI, robust system monitoring, and comprehensive configuration management into a single, cohesive platform.

Our vision is to transform how we interact with our digital environments. Instead of manually configuring systems, managing packages, and debugging issues, CloudCurio empowers an AI-driven orchestrator to handle these tasks autonomously. This is **Configuration as Code (CaC)** evolved—a living, intelligent system that understands its own state and acts to maintain and enhance it.

For a deeper dive into the philosophy and long-term goals of this project, please read our [**PROJECT_VISION.md**](PROJECT_VISION.md).

## 🚀 The Grand Plan: A Unified Roadmap

We have a clear, phased approach to achieving this vision. Our roadmap outlines the journey from enhancing our current tools to deploying a fully autonomous AI orchestrator. Key phases include:

1.  **Integration & Enhancement:** Fortifying our system discovery tools to generate robust, version-controlled configuration templates (e.g., Ansible playbooks).
2.  **Monitoring & Knowledge:** Deploying a comprehensive monitoring stack (Prometheus, Grafana, Loki) and building a centralized, queryable knowledge base.
3.  **AI Orchestration:** Developing the "master brain" that ingests system data, reasons about it, and dispatches AI agents to perform tasks.

For a detailed breakdown of all upcoming features, tasks, and priorities, please see our master [**ROADMAP.md**](ROADMAP.md).

## Core Components

CloudCurio is a monorepo containing a suite of powerful, integrated tools that form the building blocks of the Sentient Homelab.

### 🧠 AI & Crew Management (`/crew`, `/ai_tools`)

The core intelligence of the platform.
*   **AI Provider Integration:** A multi-provider framework supporting dozens of models from OpenAI, Google, Anthropic, and local instances via Ollama.
*   **CrewAI Framework:** Orchestrates teams of specialized AI agents to perform complex tasks like code analysis, documentation, and automated debugging.
*   **MCP Server:** A central server for managing and deploying AI crews via a REST API.

### 🖥️ System Monitoring & CaC (`/sysmon`)

The system's "digital twin," providing continuous awareness of its state.
*   **System State Discovery:** `sysmon` automatically tracks package installations (`apt`, `pip`, `npm`, Homebrew), service changes, and configuration file modifications.
*   **Reproducibility:** It can generate snapshots of the system's state and create shell scripts or (in the future) Ansible playbooks to replicate the configuration elsewhere.
*   **Continuous Monitoring:** Designed to run as a `systemd` service, providing a constant stream of data for the AI orchestrator.

### 🛠️ Configuration & Management (`/config_editor`, `/open_webui`)

Tools for interacting with and managing the platform.
*   **Web-Based Config Editor:** A UI for visually managing system configurations and services.
*   **Open WebUI Integration:** Provides a chat interface for interacting directly with the underlying AI models.
*   **Terminal Tools:** Includes a pre-configured Tabby terminal setup for an enhanced development workflow.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cbwinslow/cloudcurio.git
    cd cloudcurio
    ```

2.  **Run the complete setup:**
    This script will guide you through installing dependencies, setting up configurations, and preparing the environment.
    ```bash
    ./complete_setup.sh
    ```

3.  **Explore the Components:**
    Each component directory (e.g., `/sysmon`, `/crew`) contains its own `README.md` with detailed instructions.

## Contributing

This is a living project, and we welcome contributions. Whether it's by improving the code, enhancing the documentation, or suggesting new features, your input is valuable. Please see our [**CONTRIBUTING.md**](CONTRIBUTING.md) to get started.

---

## 🛠️ For Developers & Advanced Users

This `README.md` provides a high-level overview of the project's vision and components. For detailed technical information, including installation options, build instructions, API usage, and advanced configuration, please refer to our comprehensive:

### 📖 [**DEVELOPER_GUIDE.md**](./DEVELOPER_GUIDE.md)

The developer guide covers everything you need to know to contribute to the project, set up a full development environment, and use the advanced features of the CloudCurio platform.