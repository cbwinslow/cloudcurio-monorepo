#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

require 'net/http'
require 'json'
require 'uri'

module BeEF
  module Extension
    module Osint
      module Agents
        class OllamaIntegration
          
          def initialize
            @config = BeEF::Core::Configuration.instance.get('beef.extension.osint.ollama')
            @base_url = "http://#{@config['host']}:#{@config['port']}"
          end
          
          # Check if Ollama is running
          def health_check
            begin
              uri = URI("#{@base_url}/api/tags")
              response = Net::HTTP.get_response(uri)
              response.code == '200'
            rescue => e
              BeEF::Core::Logger.instance.register('Osint', "Ollama health check failed: #{e.message}")
              false
            end
          end
          
          # List available models
          def list_models
            begin
              uri = URI("#{@base_url}/api/tags")
              response = Net::HTTP.get_response(uri)
              if response.code == '200'
                data = JSON.parse(response.body)
                data['models'] || []
              else
                []
              end
            rescue => e
              BeEF::Core::Logger.instance.register('Osint', "Failed to list Ollama models: #{e.message}")
              []
            end
          end
          
          # Pull a model
          def pull_model(model_name)
            begin
              uri = URI("#{@base_url}/api/pull")
              request = Net::HTTP::Post.new(uri)
              request['Content-Type'] = 'application/json'
              request.body = { name: model_name }.to_json
              
              response = Net::HTTP.start(uri.hostname, uri.port) do |http|
                http.request(request)
              end
              
              response.code == '200'
            rescue => e
              BeEF::Core::Logger.instance.register('Osint', "Failed to pull Ollama model #{model_name}: #{e.message}")
              false
            end
          end
          
          # Generate text using a model
          def generate(prompt, options = {})
            begin
              uri = URI("#{@base_url}/api/generate")
              request = Net::HTTP::Post.new(uri)
              request['Content-Type'] = 'application/json'
              
              payload = {
                model: @config['model'],
                prompt: prompt,
                stream: false
              }.merge(options)
              
              request.body = payload.to_json
              
              response = Net::HTTP.start(uri.hostname, uri.port) do |http|
                http.request(request)
              end
              
              if response.code == '200'
                data = JSON.parse(response.body)
                data['response']
              else
                nil
              end
            rescue => e
              BeEF::Core::Logger.instance.register('Osint', "Failed to generate text with Ollama: #{e.message}")
              nil
            end
          end
          
          # Chat with a model
          def chat(messages, options = {})
            begin
              uri = URI("#{@base_url}/api/chat")
              request = Net::HTTP::Post.new(uri)
              request['Content-Type'] = 'application/json'
              
              payload = {
                model: @config['model'],
                messages: messages,
                stream: false
              }.merge(options)
              
              request.body = payload.to_json
              
              response = Net::HTTP.start(uri.hostname, uri.port) do |http|
                http.request(request)
              end
              
              if response.code == '200'
                data = JSON.parse(response.body)
                data['message']
              else
                nil
              end
            rescue => e
              BeEF::Core::Logger.instance.register('Osint', "Failed to chat with Ollama: #{e.message}")
              nil
            end
          end
          
          # Embed text using a model
          def embed(text, options = {})
            begin
              uri = URI("#{@base_url}/api/embeddings")
              request = Net::HTTP::Post.new(uri)
              request['Content-Type'] = 'application/json'
              
              payload = {
                model: @config['model'],
                prompt: text
              }.merge(options)
              
              request.body = payload.to_json
              
              response = Net::HTTP.start(uri.hostname, uri.port) do |http|
                http.request(request)
              end
              
              if response.code == '200'
                data = JSON.parse(response.body)
                data['embedding']
              else
                nil
              end
            rescue => e
              BeEF::Core::Logger.instance.register('Osint', "Failed to embed text with Ollama: #{e.message}")
              nil
            end
          end
          
          # Analyze OSINT data using Ollama
          def analyze_osint_data(data, analysis_type = "general")
            prompt = case analysis_type
                    when "person"
                      "Analyze the following person data and extract key information, relationships, and potential risks:\n\n#{data}"
                    when "domain"
                      "Analyze the following domain information and identify potential security concerns, ownership details, and related infrastructure:\n\n#{data}"
                    when "ip"
                      "Analyze the following IP address information and identify associated domains, services, and potential security risks:\n\n#{data}"
                    when "email"
                      "Analyze the following email information and identify potential social engineering risks and associated accounts:\n\n#{data}"
                    else
                      "Analyze the following OSINT data and provide insights, patterns, and potential security implications:\n\n#{data}"
                    end
            
            generate(prompt, { temperature: 0.7 })
          end
          
          # Generate OSINT report using Ollama
          def generate_report(data, report_type = "executive")
            prompt = case report_type
                    when "executive"
                      "Create an executive summary report from the following OSINT data. Focus on key findings, risks, and recommendations:\n\n#{data}"
                    when "technical"
                      "Create a technical OSINT report from the following data. Include detailed findings, methodologies, and evidence:\n\n#{data}"
                    when "investigative"
                      "Create an investigative OSINT report from the following data. Focus on connections, timelines, and potential leads:\n\n#{data}"
                    else
                      "Create a comprehensive OSINT report from the following data:\n\n#{data}"
                    end
            
            generate(prompt, { temperature: 0.5 })
          end
          
        end
      end
    end
  end
end