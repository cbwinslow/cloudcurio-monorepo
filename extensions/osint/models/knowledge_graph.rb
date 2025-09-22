#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

require 'neo4j-core'

module BeEF
  module Extension
    module Osint
      module Models
        class KnowledgeGraph
          
          def initialize
            @config = BeEF::Core::Configuration.instance.get('beef.extension.osint.neo4j')
            @session = nil
          end
          
          # Establish connection to Neo4j database
          def connect
            begin
              @session = Neo4j::Session.open(:server_db, 
                "http://#{@config['host']}:#{@config['port']}", 
                username: @config['username'], 
                password: @config['password'],
                database: @config['database']
              )
              BeEF::Core::Logger.instance.register('Osint', "Connected to Neo4j at #{@config['host']}:#{@config['port']}")
              return true
            rescue => e
              BeEF::Core::Logger.instance.register('Osint', "Failed to connect to Neo4j: #{e.message}")
              return false
            end
          end
          
          # Close connection to Neo4j database
          def disconnect
            @session.close if @session
          end
          
          # Create a person node
          def create_person(properties)
            query = "CREATE (p:Person {props}) RETURN p"
            result = @session.query(query, props: properties.merge({
              id: SecureRandom.uuid,
              created_at: DateTime.now,
              updated_at: DateTime.now
            }))
            result.first&.p
          end
          
          # Create an email node
          def create_email(properties)
            query = "CREATE (e:Email {props}) RETURN e"
            result = @session.query(query, props: properties.merge({
              id: SecureRandom.uuid,
              created_at: DateTime.now,
              updated_at: DateTime.now
            }))
            result.first&.e
          end
          
          # Create a domain node
          def create_domain(properties)
            query = "CREATE (d:Domain {props}) RETURN d"
            result = @session.query(query, props: properties.merge({
              id: SecureRandom.uuid,
              created_at: DateTime.now,
              updated_at: DateTime.now
            }))
            result.first&.d
          end
          
          # Create an IP address node
          def create_ip_address(properties)
            query = "CREATE (ip:IPAddress {props}) RETURN ip"
            result = @session.query(query, props: properties.merge({
              id: SecureRandom.uuid,
              created_at: DateTime.now,
              updated_at: DateTime.now
            }))
            result.first&.ip
          end
          
          # Create a social profile node
          def create_social_profile(properties)
            query = "CREATE (sp:SocialProfile {props}) RETURN sp"
            result = @session.query(query, props: properties.merge({
              id: SecureRandom.uuid,
              created_at: DateTime.now,
              updated_at: DateTime.now
            }))
            result.first&.sp
          end
          
          # Create a phone number node
          def create_phone_number(properties)
            query = "CREATE (pn:PhoneNumber {props}) RETURN pn"
            result = @session.query(query, props: properties.merge({
              id: SecureRandom.uuid,
              created_at: DateTime.now,
              updated_at: DateTime.now
            }))
            result.first&.pn
          end
          
          # Create an organization node
          def create_organization(properties)
            query = "CREATE (o:Organization {props}) RETURN o"
            result = @session.query(query, props: properties.merge({
              id: SecureRandom.uuid,
              created_at: DateTime.now,
              updated_at: DateTime.now
            }))
            result.first&.o
          end
          
          # Create a relationship between nodes
          def create_relationship(from_node, to_node, rel_type, properties = {})
            query = "MATCH (a), (b) WHERE a.id = $from_id AND b.id = $to_id CREATE (a)-[r:#{rel_type} {props}]->(b) RETURN r"
            result = @session.query(query, 
              from_id: from_node[:id], 
              to_id: to_node[:id], 
              props: properties.merge({created_at: DateTime.now})
            )
            result.first&.r
          end
          
          # Find person by email
          def find_person_by_email(email)
            query = "MATCH (p:Person)-[:EMAIL_ASSOCIATED_WITH]->(e:Email {address: $email}) RETURN p"
            result = @session.query(query, email: email)
            result.map(&:p)
          end
          
          # Find domains associated with IP
          def find_domains_by_ip(ip_address)
            query = "MATCH (d:Domain)-[:DOMAIN_HOSTED_ON]->(ip:IPAddress {address: $ip}) RETURN d"
            result = @session.query(query, ip: ip_address)
            result.map(&:d)
          end
          
          # Get all relationships for a node
          def get_node_relationships(node_id)
            query = "MATCH (n)-[r]->(m) WHERE n.id = $node_id RETURN n, r, m"
            result = @session.query(query, node_id: node_id)
            result.map { |row| { from: row.n, relationship: row.r, to: row.m } }
          end
          
        end
      end
    end
  end
end