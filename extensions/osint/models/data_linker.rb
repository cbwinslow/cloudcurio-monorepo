#
# Copyright (c) 2006-2025 Wade Alcorn - wade@bindshell.net
# Browser Exploitation Framework (BeEF) - https://beefproject.com
# See the file 'doc/COPYING' for copying permission
#

module BeEF
  module Extension
    module Osint
      module Models
        
        class DataLinker
          
          def initialize
            @knowledge_graph = KnowledgeGraph.new
          end
          
          # Link a person to an email address
          def link_person_to_email(person_id, email_address, confidence = 0.8)
            # Create or find the email node
            email_node = @knowledge_graph.create_email({ address: email_address })
            
            # Find the person node
            # This is a placeholder - in reality, you'd query the graph for the person
            person_node = { id: person_id }
            
            # Create the relationship
            relationship = @knowledge_graph.create_relationship(
              person_node, 
              email_node, 
              'EMAIL_ASSOCIATED_WITH',
              { confidence: confidence }
            )
            
            relationship
          end
          
          # Link a domain to a person/organization
          def link_domain_to_entity(domain_name, entity_id, entity_type, confidence = 0.9)
            # Create or find the domain node
            domain_node = @knowledge_graph.create_domain({ name: domain_name })
            
            # Find the entity node
            # This is a placeholder - in reality, you'd query the graph for the entity
            entity_node = { id: entity_id }
            
            # Create the relationship
            relationship_type = entity_type == 'organization' ? 'DOMAIN_REGISTERED_BY' : 'DOMAIN_OWNED_BY'
            relationship = @knowledge_graph.create_relationship(
              domain_node, 
              entity_node, 
              relationship_type,
              { confidence: confidence }
            )
            
            relationship
          end
          
          # Link an IP address to a domain
          def link_ip_to_domain(ip_address, domain_name, confidence = 0.95)
            # Create or find the IP node
            ip_node = @knowledge_graph.create_ip_address({ address: ip_address })
            
            # Create or find the domain node
            domain_node = @knowledge_graph.create_domain({ name: domain_name })
            
            # Create the relationship
            relationship = @knowledge_graph.create_relationship(
              domain_node, 
              ip_node, 
              'DOMAIN_HOSTED_ON',
              { confidence: confidence }
            )
            
            relationship
          end
          
          # Link two people together
          def link_people(person_id_1, person_id_2, relationship_type, confidence = 0.7)
            # Find both person nodes
            # This is a placeholder - in reality, you'd query the graph for the people
            person_node_1 = { id: person_id_1 }
            person_node_2 = { id: person_id_2 }
            
            # Create the relationship
            relationship = @knowledge_graph.create_relationship(
              person_node_1, 
              person_node_2, 
              'PERSON_ASSOCIATED_WITH',
              { relationship_type: relationship_type, confidence: confidence }
            )
            
            relationship
          end
          
          # Link a person to a social profile
          def link_person_to_social_profile(person_id, platform, username, profile_url, confidence = 0.85)
            # Create the social profile node
            social_profile_node = @knowledge_graph.create_social_profile({
              platform: platform,
              username: username,
              url: profile_url
            })
            
            # Find the person node
            person_node = { id: person_id }
            
            # Create the relationship
            relationship = @knowledge_graph.create_relationship(
              person_node, 
              social_profile_node, 
              'PERSON_HAS_SOCIAL_PROFILE',
              { confidence: confidence }
            )
            
            relationship
          end
          
          # Link a person to a phone number
          def link_person_to_phone(person_id, phone_number, country_code, phone_type, confidence = 0.9)
            # Create the phone number node
            phone_node = @knowledge_graph.create_phone_number({
              number: phone_number,
              country_code: country_code,
              type: phone_type
            })
            
            # Find the person node
            person_node = { id: person_id }
            
            # Create the relationship
            relationship = @knowledge_graph.create_relationship(
              person_node, 
              phone_node, 
              'PERSON_HAS_PHONE',
              { confidence: confidence }
            )
            
            relationship
          end
          
          # Link an organization to a person (employment)
          def link_organization_to_person(org_id, person_id, title, department, start_date = nil, end_date = nil, confidence = 0.9)
            # Find both nodes
            org_node = { id: org_id }
            person_node = { id: person_id }
            
            # Create the relationship
            relationship = @knowledge_graph.create_relationship(
              org_node, 
              person_node, 
              'ORGANIZATION_EMPLOYS',
              {
                title: title,
                department: department,
                start_date: start_date,
                end_date: end_date,
                confidence: confidence
              }
            )
            
            relationship
          end
          
          # Link two IP addresses
          def link_ips(ip_address_1, ip_address_2, connection_type, confidence = 0.8)
            # Create or find the IP nodes
            ip_node_1 = @knowledge_graph.create_ip_address({ address: ip_address_1 })
            ip_node_2 = @knowledge_graph.create_ip_address({ address: ip_address_2 })
            
            # Create the relationship
            relationship = @knowledge_graph.create_relationship(
              ip_node_1, 
              ip_node_2, 
              'IP_CONNECTED_TO',
              { connection_type: connection_type, confidence: confidence }
            )
            
            relationship
          end
          
          # Find all connections for a person
          def find_person_connections(person_id)
            @knowledge_graph.get_node_relationships(person_id)
          end
          
          # Find all connections for a domain
          def find_domain_connections(domain_name)
            # First, find the domain node
            # This is a placeholder - in reality, you'd query the graph for the domain
            domain_node = { id: "domain_#{domain_name}" }
            @knowledge_graph.get_node_relationships(domain_node[:id])
          end
          
          # Find all connections for an IP
          def find_ip_connections(ip_address)
            # First, find the IP node
            # This is a placeholder - in reality, you'd query the graph for the IP
            ip_node = { id: "ip_#{ip_address.gsub('.', '_')}" }
            @knowledge_graph.get_node_relationships(ip_node[:id])
          end
          
          # Find all connections for an email
          def find_email_connections(email_address)
            # First, find the email node
            # This is a placeholder - in reality, you'd query the graph for the email
            email_node = { id: "email_#{email_address.gsub('@', '_').gsub('.', '_')}" }
            @knowledge_graph.get_node_relationships(email_node[:id])
          end
          
        end
      end
    end
  end
end