#!/usr/bin/env ruby
#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

# Ollama Model Initialization Script for OSINT Extension
# This script ensures the required Ollama models are available

require 'net/http'
require 'json'
require 'uri'

class OllamaModelInitializer
  
  def initialize(host = 'localhost', port = 11434)
    @base_url = "http://#{host}:#{port}"
    @required_models = [
      'dolphin-llama3',
      'dolphin-mistral',
      'dolphin-phi'
    ]
  end
  
  # Check if Ollama is running
  def health_check
    begin
      uri = URI("#{@base_url}/api/tags")
      response = Net::HTTP.get_response(uri)
      response.code == '200'
    rescue => e
      puts "Ollama health check failed: #{e.message}"
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
      puts "Failed to list Ollama models: #{e.message}"
      []
    end
  end
  
  # Pull a model
  def pull_model(model_name)
    puts "Pulling model: #{model_name}"
    begin
      uri = URI("#{@base_url}/api/pull")
      request = Net::HTTP::Post.new(uri)
      request['Content-Type'] = 'application/json'
      request.body = { name: model_name }.to_json
      
      response = Net::HTTP.start(uri.hostname, uri.port) do |http|
        http.request(request)
      end
      
      if response.code == '200'
        puts "Successfully pulled model: #{model_name}"
        true
      else
        puts "Failed to pull model: #{model_name} (HTTP #{response.code})"
        false
      end
    rescue => e
      puts "Failed to pull model #{model_name}: #{e.message}"
      false
    end
  end
  
  # Initialize required models
  def initialize_models
    unless health_check
      puts "Ollama is not running. Please start Ollama service first."
      return false
    end
    
    available_models = list_models.map { |m| m['name'] }
    puts "Available models: #{available_models.join(', ')}"
    
    missing_models = @required_models - available_models
    
    if missing_models.empty?
      puts "All required models are already available."
      return true
    end
    
    puts "Missing models: #{missing_models.join(', ')}"
    
    missing_models.each do |model|
      pull_model(model)
    end
    
    true
  end
end

# Run the initializer if this script is executed directly
if __FILE__ == $0
  initializer = OllamaModelInitializer.new
  initializer.initialize_models
end