#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

module BeEF
  module Extension
    module Osint
      module Controllers
        
        class MainController < BeEF::Core::Router::Router
          
          before do
            # Ensure user is authenticated
            error(401) unless session.present? && session['user_id'].present?
          end
          
          # Main OSINT dashboard
          get '/' do
            erb :'osint/dashboard', {}, :views => "#{$root_dir}/extensions/osint/views"
          end
          
          # Target research page
          get '/research/:target_type/:target_id' do
            @target_type = params[:target_type]
            @target_id = params[:target_id]
            erb :'osint/research', {}, :views => "#{$root_dir}/extensions/osint/views"
          end
          
          # Knowledge graph visualization
          get '/graph/:target_id' do
            @target_id = params[:target_id]
            erb :'osint/graph', {}, :views => "#{$root_dir}/extensions/osint/views"
          end
          
          # Reports page
          get '/reports' do
            erb :'osint/reports', {}, :views => "#{$root_dir}/extensions/osint/views"
          end
          
          # API endpoints for OSINT data
          # Get target information
          get '/api/target/:target_type/:target_id' do
            content_type :json
            
            # This would call the appropriate model to get target data
            {
              status: 'success',
              data: {
                target_type: params[:target_type],
                target_id: params[:target_id],
                # Placeholder data
                name: 'Sample Target',
                created_at: Time.now.iso8601
              }
            }.to_json
          end
          
          # Start research on a target
          post '/api/research/start' do
            content_type :json
            
            # Parse request data
            request_data = JSON.parse(request.body.read)
            
            # This would initiate the research process using CrewAI or LangChain
            {
              status: 'success',
              message: 'Research started',
              research_id: SecureRandom.uuid
            }.to_json
          end
          
          # Get research status
          get '/api/research/status/:research_id' do
            content_type :json
            
            # This would check the status of a research task
            {
              status: 'completed',
              research_id: params[:research_id],
              progress: 100,
              results: {
                # Placeholder results
                findings: 15,
                connections: 8
              }
            }.to_json
          end
          
          # Get knowledge graph data
          get '/api/graph/:target_id' do
            content_type :json
            
            # This would retrieve graph data from Neo4j
            {
              status: 'success',
              nodes: [
                { id: '1', label: 'Person', title: 'John Doe' },
                { id: '2', label: 'Email', title: 'john@example.com' },
                { id: '3', label: 'Domain', title: 'example.com' }
              ],
              edges: [
                { from: '1', to: '2', label: 'EMAIL_ASSOCIATED_WITH' },
                { from: '3', to: '1', label: 'DOMAIN_REGISTERED_BY' }
              ]
            }.to_json
          end
          
        end
      end
    end
  end
end