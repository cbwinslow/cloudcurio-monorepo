# 📘 Project Best Practices

## 1. Project Purpose
A containerized OSINT (Open Source Intelligence) platform that integrates 20+ services for collection, analysis, storage, visualization, and management. The repository combines:
- BeEF (Browser Exploitation Framework) Ruby application and ecosystem (Sinatra/Thin/EventMachine, ActiveRecord)
- Python-based AI agents (Pydantic models/tools) for automated collection/analysis/reporting/alerting
- Node.js utilities (Express-based link shortener)
- Deployment, configuration, and docs for a microservices stack (Traefik, Kong, Supabase, Neo4j, SearXNG, LocalAI, Grafana, Prometheus, RabbitMQ, etc.)

## 2. Project Structure
- core/ — BeEF Ruby core (APIs, bootstrap, loader, settings, logging, modules/extensions wiring)
- extensions/, modules/ — BeEF extensions and modules
- spec/ — RSpec tests (unit and feature), Capybara/Selenium browser-driven tests, helpers
- test/ — Test::Unit integration tests (end-to-end flows exercising BeEF server/APIs)
- ai-agents/ — Python agents
  - agents/ — base classes (Agent/Tool) and concrete implementations
  - tools/ — tool implementations (SearXNG search, analysis/reporting/alerting stubs)
  - config/agents.yaml — agent+tool configuration (env-var aware placeholders like ${VAR})
  - main.py — entry point demo
  - requirements.txt — Python deps
  - Dockerfile — containerization entrypoint
- link_shortener.js, package.json — Node.js Express link shortener utility
- config/, beef-config/ — platform and BeEF configs (YAML), including master-config.yaml and osint-platform-config.yaml
- deployment/, scripts/ — orchestration (Ansible, Docker, local/remote), helper scripts
- docs/, doc/ — architecture and guide docs, BeEF docs
- docker-compose.yml, Dockerfile* — container orchestration/build
- .rubocop.yml — Ruby style rules
- .trunk/trunk.yaml — multi-language linting/formatting configuration (Ruby, Python, Node, YAML, Markdown, Shell)

Key entrypoints and configs:
- Ruby (BeEF): core/bootstrap.rb, core/api/*.rb, config.yaml
- Python (AI agents): ai-agents/main.py, ai-agents/config/agents.yaml
- Node (link shortener): link_shortener.js, package.json
- Orchestration: docker-compose.yml, deployment/*, scripts/*

## 3. Test Strategy
- Ruby
  - Frameworks: RSpec (spec/) with Capybara + Selenium for browser automation; Test::Unit for integration (test/integration)
  - Bootstrapping: spec/spec_helper.rb initializes BeEF, sets SQLite in-memory DB with OTR ActiveRecord, runs migrations, and manages server lifecycle for integration tests
  - Organization: 
    - spec/beef/** for unit/spec-level tests of core, api, modules, extensions
    - spec/features/** for feature/all-modules runs
    - test/integration/** for end-to-end REST/browser flows and API rate tests
  - Mocking/IO:
    - Prefer stubbing BeEF internals and boundary adapters for unit tests
    - For external HTTP, consider WebMock/VCR (not currently in Gemfile) to keep tests hermetic
  - Unit vs Integration:
    - Unit: pure Ruby logic, module functionality, filter behavior, error handling
    - Integration: server boot, REST endpoints, UI flows via Capybara/Selenium
- Python
  - No tests present; adopt pytest with tests/ mirroring ai-agents/ structure (e.g., tests/agents/, tests/tools/)
  - Use requests-mock or responses for HTTP; fixture-driven agent+tool wiring
  - Unit vs Integration:
    - Unit: Agent.run behavior, Tool.execute contracts, config loading and env expansion
    - Integration: end-to-end scenarios against real services via docker-compose
- Node
  - No tests present; use Vitest or Jest for unit tests of link_shortener.js; supertest for HTTP endpoints
- Coverage targets (suggested): >=80% for unit; keep integration tests targeted and stable

## 4. Code Style
- Ruby
  - Target Ruby 3.0 (per .rubocop.yml). Max line length 180. Many Metrics cops disabled—prefer clarity but avoid excessive complexity
  - Use snake_case for methods/variables, CamelCase for classes/modules
  - Avoid blocking operations on the EventMachine reactor thread; offload long-running IO
  - Logging: use BeEF::Core::Console or namespaced Console shims provided in spec_helper
  - ActiveRecord with OTR: ensure connections are managed across forks; follow patterns in spec_helper for migrations and connection lifecycles
  - Prefer explicit require paths under core/, avoid magic globals where possible
- Python (ai-agents)
  - Use type hints consistently; leverage Pydantic models for config/contracts
  - Keep Agent and Tool classes small, focused; Tool.execute should be side-effect aware and validate inputs
  - Isolate network calls; handle timeouts, retries, and structured error returns; don’t swallow exceptions silently in production paths
  - Expand ${VAR} in YAML configurations via environment variables at load time
  - Keep agents stateless; inject configuration and dependencies (endpoints, credentials)
- Node
  - Minimal Express endpoints; validate inputs; avoid synchronous filesystem or long blocking operations on request path
  - Centralize configuration via environment variables
- Documentation
  - Module/class docstrings (Ruby/YARD; Python docstrings) for public APIs; top-of-file purpose comments for scripts
- Error handling
  - Validate inputs and configuration at boundaries
  - Wrap external IO (HTTP/DB/FS) with retries and timeouts; return structured errors upward
  - Fail fast on misconfiguration; prefer explicit exceptions over silent fallbacks

## 5. Common Patterns
- Configuration-as-YAML with env placeholders (e.g., ${NEO4J_PASSWORD}); prefer runtime env resolution and avoid committing secrets
- Dependency injection for agents/tools: AgentManager wires tool instances by name; tools encapsulate external service access
- Sinatra + Thin + EventMachine for HTTP/WebSocket; keep EM event loop unblocked
- ActiveRecord + OTR for DB with runtime migrations; SQLite local, Postgres in Supabase for production
- Multi-language linting via Trunk: rubocop, ruff/black/isort, prettier, markdownlint, yamllint, shellcheck
- Browser automation for integration via Capybara/Selenium; optional BrowserStack configuration hooks present

## 6. Do's and Don'ts
- Do
  - Use environment variables for secrets and endpoints; keep defaults in YAML config templates only
  - Add unit tests for every new public method or tool; add integration tests only where behavior spans processes/services
  - Run linters/formatters (trunk check) before commits; conform to .rubocop.yml
  - Keep long-running/network-heavy work off the main event loop (Ruby EM)
  - Validate config at startup; log useful diagnostics
  - Use small, composable tools and agents; prefer explicit contracts (execute signatures)
  - Document new services/modules with a short README and example config
- Don't
  - Don’t commit secrets or tokens; don’t hardcode service URLs
  - Don’t introduce blocking IO in EventMachine handlers or Rack middlewares
  - Don’t couple agents directly to service SDKs inside business logic—wrap them in Tool classes
  - Don’t add global mutable state; avoid hidden singletons beyond existing BeEF core
  - Don’t add cross-language dependencies without containerizing or documenting local dev flow

## 7. Tools & Dependencies
- Ruby (Gemfile)
  - Web: sinatra, thin, eventmachine, em-websocket, rack, rack-protection
  - Assets/Utils: uglifier, mime-types, execjs
  - DB: activerecord, otr-activerecord, sqlite3
  - Testing: rspec, capybara, selenium-webdriver, curb, rest-client, websocket-client-simple
  - Linting: rubocop
  - Commands
    - bundle install
    - rspec (RSpec tests)
    - ruby test/integration/ts_integration.rb (integration suite)
- Python (ai-agents/requirements.txt)
  - pydantic, pydantic-ai, pyyaml, requests, docker, psycopg2-binary, neo4j
  - Commands
    - python3 -m venv .venv && source .venv/bin/activate
    - pip install -r ai-agents/requirements.txt
    - python ai-agents/main.py
- Node (package.json)
  - express
  - Commands
    - npm install
    - npm start (runs link_shortener.js)
- Orchestration
  - docker-compose up -d (bring up the stack)
  - Scripts under scripts/ and deployment/ manage lifecycle, backups, and remote deploys
- Linting & Formatting (via Trunk CLI)
  - trunk check (rubocop, ruff/black/isort, prettier, markdownlint, yamllint, shellcheck, hadolint, etc.)

## 8. Other Notes
- Security and Legal
  - BeEF is a browser exploitation framework; only use in controlled, authorized environments
  - Change defaults, enforce TLS, place sensitive services behind Kong and network policies
  - Centralize secrets in Bitwarden; never commit actual credentials
- LLM Code Generation Guidance
  - Ruby: follow Sinatra/BeEF patterns; place unit tests in spec/ matching the directory of the code being tested; use expect syntax
  - Python: implement new Tools in ai-agents/tools/impl.py and wire them via ai-agents/config/agents.yaml; keep execute signatures explicit and documented; prefer pytest for new tests
  - Node: keep utilities minimal and stateless; add tests with Vitest/Jest alongside code
  - Place new configs under config/ or ai-agents/config/, referencing environment variables
- Edge Cases / Constraints
  - Multi-language monorepo: keep language-specific tooling isolated; use containers for reproducibility
  - EventMachine constraints: avoid blocking calls; use async patterns or background workers
  - AI agents scaffolding is illustrative—use a registration map/factory to resolve agent names to concrete classes; avoid instantiating abstract base classes
  - Tests spin up BeEF; ensure ports are free and increase timeouts when running under CI or resource-constrained environments
