#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

module BeEF
  module Extension
    module Osint
      module Reports
        
        class ReportSpecialist
          
          def initialize
            @constructor = ReportConstructor.new
            @ollama = BeEF::Extension::Osint::Agents::OllamaIntegration.new
          end
          
          # Create an executive summary from research data
          def create_executive_summary(research_data)
            # Use Ollama to generate a summary if available
            if @ollama.health_check
              summary_prompt = "Create an executive summary from the following OSINT research data. Focus on key findings, risks, and recommendations:\n\n#{research_data.to_json}"
              ai_summary = @ollama.generate(summary_prompt)
            end
            
            # Structure the data for the report
            report_data = {
              'findings' => research_data['findings'] || [],
              'recommendations' => research_data['recommendations'] || [],
              'summary' => ai_summary || "No AI-generated summary available"
            }
            
            # Generate the report
            @constructor.generate_report(report_data, 'executive')
          end
          
          # Create a technical report from research data
          def create_technical_report(research_data)
            # Use Ollama to analyze technical data if available
            if @ollama.health_check
              tech_prompt = "Analyze the following technical OSINT data and organize it into a structured format with findings, evidence, and severity assessments:\n\n#{research_data.to_json}"
              ai_analysis = @ollama.generate(tech_prompt)
            end
            
            # Structure the data for the report
            report_data = {
              'target' => research_data['target'] || {},
              'technical_findings' => research_data['technical_findings'] || [],
              'sources' => research_data['sources'] || [],
              'analysis' => ai_analysis || "No AI-generated analysis available"
            }
            
            # Generate the report
            @constructor.generate_report(report_data, 'technical')
          end
          
          # Create an investigative report from research data
          def create_investigative_report(research_data)
            # Structure the data for the report
            report_data = {
              'timeline' => research_data['timeline'] || [],
              'connections' => research_data['connections'] || [],
              'leads' => research_data['leads'] || [],
              'evidence' => research_data['evidence'] || []
            }
            
            # Generate the report
            @constructor.generate_report(report_data, 'investigative')
          end
          
          # Generate all report types from research data
          def generate_all_reports(research_data)
            {
              'executive' => create_executive_summary(research_data),
              'technical' => create_technical_report(research_data),
              'investigative' => create_investigative_report(research_data)
            }
          end
          
          # Save all reports
          def save_all_reports(reports, base_filename = nil)
            base_filename ||= "osint_report_#{Time.now.strftime('%Y%m%d_%H%M%S')}"
            
            saved_paths = {}
            
            reports.each do |type, report|
              next unless report
              
              filename = "#{base_filename}_#{type}"
              saved_path = @constructor.save_report(report, filename)
              saved_paths[type] = saved_path
            end
            
            saved_paths
          end
          
        end
      end
    end
  end
end