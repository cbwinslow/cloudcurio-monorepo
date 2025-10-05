# CloudCurio Project Roadmap

This document outlines the strategic roadmap for the CloudCurio project. It serves as the single source of truth for all development efforts, merging the long-term "Sentient Homelab" vision with the concrete tasks required to enhance the platform.

## Guiding Principles
*   **Phased Approach:** We build from the ground up, ensuring each new layer has a solid foundation.
*   **Leverage, Then Build:** We will enhance and integrate our existing tools (`sysmon`, `crew`) before building entirely new components.
*   **Vision-Oriented:** Every task, no matter how small, should be a step towards the goal of a self-managing, AI-driven system.

---

## Phase 1: Configuration as Code & System Baselining

**Goal:** Enhance our ability to discover, document, and reproduce system configurations. This phase is about perfecting the "Configuration as Code" pillar.

| ID | Task | Domain | Priority | Status | Notes |
|----|------|--------|----------|--------|-------|
| **1.1** | **Ansible Integration for `sysmon`** | `SysMon` | Critical | Not Started | Enhance `sysmon` to not only generate shell scripts but also produce idempotent Ansible playbooks for system reproduction. |
| **1.2**| **Expand Package Manager Support** | `SysMon` | High | Not Started | Add robust support for `bun`, `pnpm`, `uv`, and Homebrew to ensure all software is tracked. Validate install versions. |
| **1.3** | **Bash History Ingestion & Analysis** | `SysMon` | High | Not Started | Create a service that continuously ingests `.bash_history` from all nodes, categorizes commands using a local AI model, and generates initial configuration discovery reports (e.g., identifying manually cloned git repos). |
| **1.4** | **Initial Dotfiles Management** | `Platform` | Medium | Not Started | Develop a basic Ansible role for deploying and managing a user's dotfiles across multiple systems. |
| **1.5** | **Windows Compatibility for `sysmon`** | `SysMon` | Medium | Blocked | Establish a testing environment to begin adapting `sysmon` for Windows systems, tracking Chocolatey/Winget packages and PowerShell history. |

---

## Phase 2: Monitoring Stack & Knowledge Base

**Goal:** Deploy a comprehensive, centralized monitoring stack and build the infrastructure for a queryable, AI-powered knowledge base. This phase establishes "Continuous System Awareness."

| ID | Task | Domain | Priority | Status | Notes |
|----|------|--------|----------|--------|-------|
| **2.1**| **Deploy Core Monitoring Stack** | `Infra` | Critical | Not Started | Use Docker Compose to deploy Prometheus, Grafana, and Loki. Create initial dashboards for system metrics. |
| **2.2**| **Federated Log & Metric Shipping** | `Infra` | Critical | Not Started | Configure Promtail and Node Exporter on all nodes to ship logs and metrics to the central stack. |
| **2.3**| **Secure Networking with Tailscale** | `Infra` | High | Not Started | Create an Ansible role to install and configure Tailscale on all nodes, ensuring the monitoring stack is only accessible over the secure tailnet. |
| **2.4**| **Vector DB & Ingestion Pipeline** | `AI` | High | Not Started | Set up a vector database (e.g., Qdrant). Develop a pipeline to ingest Markdown docs, PDFs, and web articles, embedding them for semantic search. |
| **2.5**| **Knowledge Base Web UI** | `Platform` | High | Not Started | Build a simple but functional website (using Astro or Next.js) to search and display content from the vector database. |
| **2.6**| **Persistent Time-Series Database** | `Infra` | Medium | Not Started | Set up PostgreSQL with TimescaleDB or InfluxDB for long-term storage of Prometheus metrics. |

---

## Phase 3: AI Orchestration & Automation

**Goal:** Develop the "master brain" of the system. This phase connects the data from Phase 2 with the AI agent framework from Phase 1 to enable intelligent, automated actions.

| ID | Task | Domain | Priority | Status | Notes |
|----|------|--------|----------|--------|-------|
| **3.1**| **Develop AI Orchestrator Service** | `AI` | Critical | Not Started | Create the core Python application for the AI orchestrator. It will connect to Loki (logs) and Prometheus (alerts) as its primary data inputs. |
| **3.2**| **"Chain of Thought" Logging** | `AI` | Critical | Not Started | Implement a persistent, append-only log for the AI's reasoning process (`observe -> orient -> decide -> act`). This is crucial for transparency and debugging. |
| **3.3**| **Action Delegation to Ansible** | `AI` | High | Not Started | Give the orchestrator the ability to trigger Ansible playbooks as its primary "act" mechanism. Start with simple tasks like restarting a service. |
| **3.4**| **Knowledge Base Integration** | `AI` | High | Not Started | Provide the orchestrator with an API to query the vector database, allowing it to use the knowledge base to inform its decisions (e.g., looking up error messages). |
| **3.5**| **Real-time Updates via WebSockets** | `MCP` | Medium | Not Started | Implement WebSocket support in the MCP server to provide real-time updates on crew status and AI thought processes to any connected UIs. |
| **3.6**| **Self-Healing Capabilities** | `AI` | Medium | Not Started | Develop the first self-healing loop: The AI detects a failed service via a Prometheus alert, finds the relevant playbook in its knowledge base, and executes it to restart the service. |

---

## Phase 4: Refinement & Self-Improvement

**Goal:** Close the feedback loop, enabling the system to learn from its actions and become more autonomous over time.

*This phase is more conceptual and will be broken down into concrete tasks as the project matures.*

*   **Automated Task Generation:** The AI should be able to propose new tasks for this roadmap based on its analysis of system performance or recurring issues.
*   **Playbook Optimization:** The AI could suggest improvements to Ansible playbooks based on the outcomes of its actions.
*   **Proactive Maintenance:** Move from reactive fixes to proactive maintenance, such as scheduling updates, cleaning caches, and optimizing configurations based on observed patterns.
*   **Advanced UI/Dashboards:** Create a unified dashboard that visualizes the AI's thought process alongside system metrics, providing a single pane of glass into the entire ecosystem.