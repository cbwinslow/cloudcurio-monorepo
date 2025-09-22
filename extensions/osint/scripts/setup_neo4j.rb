#!/usr/bin/env ruby
#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

# Neo4j Schema Setup Script for OSINT Extension
# This script initializes the Neo4j database with the required schema

require 'neo4j-core'

class Neo4jSchemaSetup
  
  def initialize
    @config = {
      host: 'localhost',
      port: 7687,
      username: 'neo4j',
      password: 'password'
    }
    
    # Try to load config from BeEF if available
    if defined?(BeEF) && BeEF::Core::Configuration.instance
      osint_config = BeEF::Core::Configuration.instance.get('beef.extension.osint.neo4j')
      @config.merge!(osint_config) if osint_config
    end
    
    @session = nil
  end
  
  # Establish connection to Neo4j database
  def connect
    begin
      @session = Neo4j::Session.open(:server_db, 
        "http://#{@config[:host]}:#{@config[:port]}", 
        username: @config[:username], 
        password: @config[:password]
      )
      puts "Connected to Neo4j at #{@config[:host]}:#{@config[:port]}"
      true
    rescue => e
      puts "Failed to connect to Neo4j: #{e.message}"
      false
    end
  end
  
  # Close connection to Neo4j database
  def disconnect
    @session.close if @session
  end
  
  # Create indexes
  def create_indexes
    puts "Creating indexes..."
    
    indexes = [
      "CREATE INDEX ON :Person(username)",
      "CREATE INDEX ON :Person(email)",
      "CREATE INDEX ON :Email(address)",
      "CREATE INDEX ON :Domain(name)",
      "CREATE INDEX ON :IPAddress(address)",
      "CREATE INDEX ON :SocialProfile(platform, username)",
      "CREATE INDEX ON :PhoneNumber(number)",
      "CREATE INDEX ON :Organization(name)"
    ]
    
    indexes.each do |index_query|
      begin
        @session.query(index_query)
        puts "  Created index: #{index_query}"
      rescue => e
        puts "  Failed to create index: #{index_query} - #{e.message}"
      end
    end
  end
  
  # Create constraints
  def create_constraints
    puts "Creating constraints..."
    
    constraints = [
      "CREATE CONSTRAINT ON (p:Person) ASSERT p.id IS UNIQUE",
      "CREATE CONSTRAINT ON (e:Email) ASSERT e.address IS UNIQUE",
      "CREATE CONSTRAINT ON (d:Domain) ASSERT d.name IS UNIQUE",
      "CREATE CONSTRAINT ON (ip:IPAddress) ASSERT ip.address IS UNIQUE",
      "CREATE CONSTRAINT ON (sp:SocialProfile) ASSERT sp.profile_id IS UNIQUE",
      "CREATE CONSTRAINT ON (pn:PhoneNumber) ASSERT pn.number IS UNIQUE",
      "CREATE CONSTRAINT ON (o:Organization) ASSERT o.name IS UNIQUE"
    ]
    
    constraints.each do |constraint_query|
      begin
        @session.query(constraint_query)
        puts "  Created constraint: #{constraint_query}"
      rescue => e
        puts "  Failed to create constraint: #{constraint_query} - #{e.message}"
      end
    end
  end
  
  # Setup the complete schema
  def setup_schema
    return false unless connect
    
    create_indexes
    create_constraints
    
    disconnect
    true
  end
end

# Run the setup if this script is executed directly
if __FILE__ == $0
  setup = Neo4jSchemaSetup.new
  if setup.setup_schema
    puts "Neo4j schema setup completed successfully!"
  else
    puts "Neo4j schema setup failed!"
    exit 1
  end
end