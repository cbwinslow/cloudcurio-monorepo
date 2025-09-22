#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

module BeEF
  module Extension
    module Osint
      module Docs
        
        class KnowledgeBaseResearcher
          
          def initialize
            @ollama = BeEF::Extension::Osint::Agents::OllamaIntegration.new
          end
          
          # Research a topic using Ollama
          def research_topic(topic)
            return nil unless @ollama.health_check
            
            prompt = "Research and provide comprehensive information about the following OSINT topic: #{topic}. Include key concepts, methodologies, tools, and best practices."
            
            result = @ollama.generate(prompt)
            
            {
              topic: topic,
              research: result,
              timestamp: Time.now.iso8601
            }
          end
          
          # Get information about an OSINT tool
          def get_tool_info(tool_name)
            return nil unless @ollama.health_check
            
            prompt = "Provide detailed information about the OSINT tool: #{tool_name}. Include description, usage examples, strengths, limitations, and alternatives."
            
            result = @ollama.generate(prompt)
            
            {
              tool: tool_name,
              info: result,
              timestamp: Time.now.iso8601
            }
          end
          
          # Compare OSINT methodologies
          def compare_methodologies(method_a, method_b)
            return nil unless @ollama.health_check
            
            prompt = "Compare and contrast two OSINT methodologies: #{method_a} and #{method_b}. Include strengths, weaknesses, use cases, and effectiveness."
            
            result = @ollama.generate(prompt)
            
            {
              method_a: method_a,
              method_b: method_b,
              comparison: result,
              timestamp: Time.now.iso8601
            }
          end
          
          # Get best practices for an OSINT domain
          def get_best_practices(domain)
            return nil unless @ollama.health_check
            
            prompt = "Provide best practices for #{domain} in OSINT research. Include ethical considerations, legal compliance, accuracy verification, and risk mitigation."
            
            result = @ollama.generate(prompt)
            
            {
              domain: domain,
              best_practices: result,
              timestamp: Time.now.iso8601
            }
          end
          
          # Save research to knowledge base
          def save_research(research_data, filename = nil)
            filename ||= "kb_research_#{Time.now.strftime('%Y%m%d_%H%M%S')}.json"
            file_path = "#{BeEF.root}/extensions/osint/docs/knowledge_base/#{filename}"
            
            # Ensure the directory exists
            FileUtils.mkdir_p(File.dirname(file_path))
            
            # Write the research data to file
            File.write(file_path, research_data.to_json)
            
            file_path
          end
          
          # Load research from knowledge base
          def load_research(filename)
            file_path = "#{BeEF.root}/extensions/osint/docs/knowledge_base/#{filename}"
            return nil unless File.exist?(file_path)
            
            JSON.parse(File.read(file_path))
          end
          
          # List saved research documents
          def list_saved_research
            kb_dir = "#{BeEF.root}/extensions/osint/docs/knowledge_base"
            return [] unless Dir.exist?(kb_dir)
            
            Dir.glob("#{kb_dir}/*.json").map do |file|
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