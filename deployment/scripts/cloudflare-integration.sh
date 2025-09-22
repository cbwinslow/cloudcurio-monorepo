#!/bin/bash

# Cloudflare Integration Script for OSINT Platform

# Configuration
CLOUDFLARE_EMAIL=""
CLOUDFLARE_API_KEY=""
CLOUDFLARE_ZONE_ID=""
SERVER_IP=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to load configuration
load_config() {
    if [ -f "deployment/config/cloudflare.yml" ]; then
        # In a real implementation, we would parse the YAML file
        # For now, we'll just check if it exists
        print_status "Cloudflare configuration file found"
    else
        print_warning "Cloudflare configuration file not found"
    fi
}

# Function to validate Cloudflare credentials
validate_credentials() {
    print_status "Validating Cloudflare credentials..."
    
    if [ -z "$CLOUDFLARE_EMAIL" ] || [ -z "$CLOUDFLARE_API_KEY" ] || [ -z "$CLOUDFLARE_ZONE_ID" ]; then
        print_error "Cloudflare credentials not set"
        print_error "Please set CLOUDFLARE_EMAIL, CLOUDFLARE_API_KEY, and CLOUDFLARE_ZONE_ID environment variables"
        exit 1
    fi
    
    # Test API access
    response=$(curl -s -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
        -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
        -H "Content-Type: application/json")
    
    if echo "$response" | grep -q '"success":true'; then
        print_status "Cloudflare API credentials validated successfully"
    else
        print_error "Failed to validate Cloudflare API credentials"
        exit 1
    fi
}

# Function to get zone information
get_zone_info() {
    print_status "Getting zone information..."
    
    response=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID" \
        -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
        -H "Content-Type: application/json")
    
    if echo "$response" | grep -q '"success":true'; then
        zone_name=$(echo "$response" | jq -r '.result.name')
        print_status "Zone: $zone_name"
    else
        print_error "Failed to get zone information"
        exit 1
    fi
}

# Function to create DNS records
create_dns_records() {
    print_status "Creating DNS records..."
    
    # Create A record for main domain
    if [ -n "$SERVER_IP" ]; then
        response=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
            -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
            -H "Content-Type: application/json" \
            --data '{
                "type":"A",
                "name":"@",
                "content":"'"$SERVER_IP"'",
                "ttl":1,
                "proxied":true
            }')
        
        if echo "$response" | grep -q '"success":true'; then
            print_status "Created A record for @ -> $SERVER_IP"
        else
            print_warning "Failed to create A record for @ -> $SERVER_IP"
        fi
        
        # Create subdomain records
        subdomains=("www" "api" "traefik" "portainer" "grafana" "kibana")
        for subdomain in "${subdomains[@]}"; do
            response=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
                -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
                -H "Content-Type: application/json" \
                --data '{
                    "type":"A",
                    "name":"'"$subdomain"'",
                    "content":"'"$SERVER_IP"'",
                    "ttl":1,
                    "proxied":true
                }')
            
            if echo "$response" | grep -q '"success":true'; then
                print_status "Created A record for $subdomain -> $SERVER_IP"
            else
                print_warning "Failed to create A record for $subdomain -> $SERVER_IP"
            fi
        done
    else
        print_warning "SERVER_IP not set, skipping DNS record creation"
    fi
}

# Function to configure SSL settings
configure_ssl() {
    print_status "Configuring SSL settings..."
    
    # Enable Universal SSL
    response=$(curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID" \
        -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
        -H "Content-Type: application/json" \
        --data '{
            "universal_ssl":true
        }')
    
    if echo "$response" | grep -q '"success":true'; then
        print_status "Enabled Universal SSL"
    else
        print_warning "Failed to enable Universal SSL"
    fi
    
    # Set minimum TLS version
    response=$(curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/min_tls_version" \
        -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
        -H "Content-Type: application/json" \
        --data '{
            "value":"1.2"
        }')
    
    if echo "$response" | grep -q '"success":true'; then
        print_status "Set minimum TLS version to 1.2"
    else
        print_warning "Failed to set minimum TLS version"
    fi
}

# Function to configure firewall settings
configure_firewall() {
    print_status "Configuring firewall settings..."
    
    # Set security level
    response=$(curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/security_level" \
        -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
        -H "Content-Type: application/json" \
        --data '{
            "value":"medium"
        }')
    
    if echo "$response" | grep -q '"success":true'; then
        print_status "Set security level to medium"
    else
        print_warning "Failed to set security level"
    fi
    
    # Enable browser check
    response=$(curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/settings/browser_check" \
        -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
        -H "Content-Type: application/json" \
        --data '{
            "value":"on"
        }')
    
    if echo "$response" | grep -q '"success":true'; then
        print_status "Enabled browser check"
    else
        print_warning "Failed to enable browser check"
    fi
}

# Function to create page rules
create_page_rules() {
    print_status "Creating page rules..."
    
    # Create rule for API endpoints
    response=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/pagerules" \
        -H "Authorization: Bearer $CLOUDFLARE_API_KEY" \
        -H "Content-Type: application/json" \
        --data '{
            "targets":[
                {
                    "target":"url",
                    "constraint":{
                        "operator":"matches",
                        "value":"*osint-platform.com/api/*"
                    }
                }
            ],
            "actions":[
                {
                    "id":"security_level",
                    "value":"high"
                },
                {
                    "id":"browser_check",
                    "value":"on"
                }
            ],
            "priority":1,
            "status":"active"
        }')
    
    if echo "$response" | grep -q '"success":true'; then
        print_status "Created page rule for API endpoints"
    else
        print_warning "Failed to create page rule for API endpoints"
    fi
}

# Function to show completion message
show_completion() {
    print_status "=========================================="
    print_status "Cloudflare Integration Completed!"
    print_status "=========================================="
    echo ""
    print_status "Next steps:"
    print_status "1. Verify DNS records in Cloudflare dashboard"
    print_status "2. Check SSL certificate status"
    print_status "3. Review firewall and security settings"
    print_status "4. Monitor analytics and logs"
    echo ""
    print_status "Management commands:"
    print_status "- Re-run this script to update configuration"
    print_status "- Check Cloudflare dashboard for status"
    print_status "=========================================="
}

# Main integration process
print_status "Starting Cloudflare Integration..."

# Load configuration
load_config

# Validate credentials
validate_credentials

# Get zone information
get_zone_info

# Create DNS records
create_dns_records

# Configure SSL settings
configure_ssl

# Configure firewall settings
configure_firewall

# Create page rules
create_page_rules

# Show completion message
show_completion

print_status "Cloudflare integration script completed successfully!"