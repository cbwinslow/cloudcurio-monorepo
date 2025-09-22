from agents.base import Agent
from agents.dashboard import dashboard_manager
from typing import Dict, Any

class DashboardAgent(Agent):
    \"\"\"Agent responsible for creating and managing dashboards\"\"\"
    
    def run(self, task: str) -> str:
        \"\"\"Run the dashboard agent\"\"\"
        result = f\"Dashboard agent running task: {task}\\n\\n\"
        
        # Parse the task to determine what action to take
        if \"create dashboard\" in task.lower():
            # Extract dashboard type from task
            if \"osint\" in task.lower():
                template_name = \"osint_dashboard\"
            elif \"threat\" in task.lower():
                template_name = \"threat_intel_dashboard\"
            else:
                template_name = \"osint_dashboard\"  # default
            
            try:
                # Load the dashboard template
                dashboard_config = dashboard_manager.load_dashboard_template(template_name)
                
                # Create the dashboard
                dashboard_result = dashboard_manager.create_grafana_dashboard(dashboard_config)
                result += f\"Successfully created dashboard: {dashboard_result}\\n\"
            except Exception as e:
                result += f\"Failed to create dashboard: {str(e)}\\n\"
        
        elif \"list dashboards\" in task.lower():
            try:
                dashboards = dashboard_manager.get_grafana_dashboards()
                result += f\"Found {len(dashboards)} dashboards:\\n\"
                for dashboard in dashboards:
                    result += f\"  - {dashboard.get('title', 'Untitled')}\\n\"
            except Exception as e:
                result += f\"Failed to list dashboards: {str(e)}\\n\"
        
        elif \"search dashboards\" in task.lower():
            # Extract search query
            query = task.split(\"search dashboards\")[-1].strip()
            try:
                dashboards = dashboard_manager.search_dashboards(query)
                result += f\"Search results for '{query}':\\n\"
                for dashboard in dashboards:
                    result += f\"  - {dashboard.get('title', 'Untitled')}\\n\"
            except Exception as e:
                result += f\"Failed to search dashboards: {str(e)}\\n\"
        
        else:
            result += \"Available actions: create dashboard, list dashboards, search dashboards\\n\"
        
        return result