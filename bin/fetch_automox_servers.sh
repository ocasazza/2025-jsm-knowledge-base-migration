#!/bin/bash

# Script to fetch all servers from Automox API across all available pages
# Usage: ./fetch_automox_servers.sh

# Configuration
AUTH_TOKEN="b8cf1bc2-c8cc-47cf-8d96-3754a6d085b8"
ORG_ID="35645"
BASE_URL="https://console.automox.com/api/servers"
LIMIT=25
SORT_DIR="asc"
SORT_BY="display_name"
OS_FILTER="5,417,9"
COLUMNS="status,os_family,display_name,is_compatible,last_disconnect_time,server_group_id,tags,ip_addrs,os_version,pending_patches,agent_version,actions,id,last_logged_in_user,disconnected_for,organizational_unit,serial_number,create_time,patches,signing_certificate_status"
OUTPUT_DIR="./automox_data"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Initialize page counter and flag to track when to stop
page=1
has_more_data=true

echo "Starting to fetch Automox server data..."

while $has_more_data; do
    output_file="${OUTPUT_DIR}/machines_page_${page}.json"
    
    echo "Fetching page $page..."
    
    # Make the API call
    response=$(curl -s "${BASE_URL}?o=${ORG_ID}&limit=${LIMIT}&sort_dir=${SORT_DIR}&sort_by=${SORT_BY}&page=${page}&os=${OS_FILTER}&columns=${COLUMNS}" \
        -H "Authorization: Bearer ${AUTH_TOKEN}")
    
    # Check if the response is valid JSON and has data
    if echo "$response" | jq -e 'length > 0' > /dev/null 2>&1; then
        # Save the response to the output file
        echo "$response" > "$output_file"
        echo "Saved data to $output_file"
        
        # Check if we received fewer items than the limit, which indicates last page
        items_count=$(echo "$response" | jq 'length')
        if [ "$items_count" -lt "$LIMIT" ]; then
            echo "Received $items_count items (less than limit of $LIMIT). This is the last page."
            has_more_data=false
        fi
    else
        echo "No more data or invalid response. Stopping."
        has_more_data=false
    fi
    
    # Increment the page counter
    ((page++))
    
    # Optional: Add a small delay to avoid rate limiting
    sleep 1
done

echo "Completed fetching all Automox server data."
echo "Total pages fetched: $((page-1))"
echo "Data saved to the $OUTPUT_DIR directory."
