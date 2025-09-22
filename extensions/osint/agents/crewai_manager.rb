#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

require 'yaml'
require 'crew'

module BeEF
  module Extension
    module Osint
      module Agents
        class CrewAIManager
          
          def initialize
            @config = load_config
            @crews = {}
          end
          
          # Load CrewAI configuration
          def load_config
            config_path = "#{BeEF.root}/extensions/osint/config/crewai_config.yaml"
            YAML.load_file(config_path) if File.exist?(config_path)
          end
          
          # Create researcher crew
          def create_researcher_crew
            return nil unless @config
            
            researcher_config = @config['researcher_crew']
            agents_config = researcher_config['agents']
            
            agents = agents_config.map do |agent_config|
              Crew::Agent.new(
                role: agent_config['role'],
                goal: agent_config['goal'],
                backstory: agent_config['backstory'],
                tools: agent_config['tools'],
                allow_delegation: agent_config['allow_delegation'],
                verbose: agent_config['verbose']
              )
            end
            
            crew = Crew::Crew.new(
              name: researcher_config['name'],
              description: researcher_config['description'],
              agents: agents
            )
            
            @crews[:researcher] = crew
            crew
          end
          
          # Create analysis crew
          def create_analysis_crew
            return nil unless @config
            
            analysis_config = @config['analysis_crew']
            agents_config = analysis_config['agents']
            
            agents = agents_config.map do |agent_config|
              Crew::Agent.new(
                role: agent_config['role'],
                goal: agent_config['goal'],
                backstory: agent_config['backstory'],
                tools: agent_config['tools'],
                allow_delegation: agent_config['allow_delegation'],
                verbose: agent_config['verbose']
              )
            end
            
            crew = Crew::Crew.new(
              name: analysis_config['name'],
              description: analysis_config['description'],
              agents: agents
            )
            
            @crews[:analysis] = crew
            crew
          end
          
          # Create reporting crew
          def create_reporting_crew
            return nil unless @config
            
            reporting_config = @config['reporting_crew']
            agents_config = reporting_config['agents']
            
            agents = agents_config.map do |agent_config|
              Crew::Agent.new(
                role: agent_config['role'],
                goal: agent_config['goal'],
                backstory: agent_config['backstory'],
                tools: agent_config['tools'],
                allow_delegation: agent_config['allow_delegation'],
                verbose: agent_config['verbose']
              )
            end
            
            crew = Crew::Crew.new(
              name: reporting_config['name'],
              description: reporting_config['description'],
              agents: agents
            )
            
            @crews[:reporting] = crew
            crew
          end
          
          # Get a specific crew
          def get_crew(crew_name)
            @crews[crew_name]
          end
          
          # Run a specific crew with tasks
          def run_crew(crew_name, tasks)
            crew = @crews[crew_name]
            return nil unless crew
            
            # Assign tasks to the crew
            tasks.each do |task_config|
              task = Crew::Task.new(
                name: task_config['name'],
                description: task_config['description'],
                expected_output: task_config['expected_output'],
                agent: crew.agents.find { |a| a.role == task_config['agent'] }
              )
              crew.add_task(task)
            end
            
            # Execute the crew
            result = crew.kickoff
            result
          end
          
        end
      end
    end
  end
end