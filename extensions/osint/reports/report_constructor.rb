#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

require 'erb'
require 'json'

module BeEF
  module Extension
    module Osint
      module Reports
        
        class ReportConstructor
          
          def initialize
            @template_dir = "#{BeEF.root}/extensions/osint/reports/templates"
          end
          
          # Generate a report based on research data
          def generate_report(research_data, report_type = 'executive')
            template_file = case report_type
                           when 'executive'
                             'executive_summary.erb'
                           when 'technical'
                             'technical_report.erb'
                           when 'investigative'
                             'investigative_report.erb'
                           else
                             'general_report.erb'
                           end
            
            template_path = "#{@template_dir}/#{template_file}"
            return nil unless File.exist?(template_path)
            
            # Load and render the template
            template = File.read(template_path)
            renderer = ERB.new(template)
            
            # Make research data available to the template
            binding.local_variable_set(:research_data, research_data)
            
            # Render the report
            report_content = renderer.result(binding)
            
            {
              type: report_type,
              content: report_content,
              generated_at: Time.now.iso8601
            }
          end
          
          # Generate a JSON report
          def generate_json_report(research_data)
            {
              metadata: {
                generated_at: Time.now.iso8601,
                report_type: 'json',
                version: '1.0'
              },
              data: research_data
            }.to_json
          end
          
          # Generate a PDF report
          def generate_pdf_report(research_data, report_type = 'executive')
            # This would use a PDF generation library like Prawn
            # For now, we'll return a placeholder
            {
              type: 'pdf',
              content: "PDF report generation would be implemented here",
              generated_at: Time.now.iso8601
            }
          end
          
          # Save report to file
          def save_report(report, filename = nil)
            filename ||= "osint_report_#{Time.now.strftime('%Y%m%d_%H%M%S')}"
            
            case report[:type]
            when 'pdf'
              file_path = "#{BeEF.root}/extensions/osint/reports/saved/#{filename}.pdf"
            when 'json'
              file_path = "#{BeEF.root}/extensions/osint/reports/saved/#{filename}.json"
            else
              file_path = "#{BeEF.root}/extensions/osint/reports/saved/#{filename}.html"
            end
            
            # Ensure the directory exists
            FileUtils.mkdir_p(File.dirname(file_path))
            
            # Write the report to file
            File.write(file_path, report[:content])
            
            file_path
          end
          
          # List saved reports
          def list_saved_reports
            reports_dir = "#{BeEF.root}/extensions/osint/reports/saved"
            return [] unless Dir.exist?(reports_dir)
            
            Dir.glob("#{reports_dir}/*").map do |file|
              {
                name: File.basename(file),
                path: file,
                size: File.size(file),
                modified: File.mtime(file).iso8601
              }
            end
          end
          
        end
      end
    end
  end
end