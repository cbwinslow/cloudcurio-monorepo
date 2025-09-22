#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

module BeEF
  module Extension
    module Osint
      
      extend BeEF::API::Extension
      
      @short_name = 'osint'
      @full_name = 'Open Source Intelligence Analysis'
      @description = 'OSINT gathering and analysis with knowledge graph linking'
      
      def self.pre_load
        # Add any pre-load operations here
      end

      def self.load
        # Register API paths
        BeEF::Core::Server.instance.add_api_path('/api/osint', "#{BeEF.root}/extensions/osint/api")
        
        # Register controllers
        BeEF::Core::Server.instance.mount('/ui/osint', BeEF::Extension::Osint::Controllers::MainController)
      end

      def self.post_load
        # Add any post-load operations here
      end

      def self.unload
        # Add any unload operations here
      end

      # Check if the extension is running
      def self.running
        true
      end
      
    end
  end
end