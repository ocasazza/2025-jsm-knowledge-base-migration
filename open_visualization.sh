#!/bin/bash

# Check if Neo4j container is running
if ! docker ps | grep -q neo4j-kg; then
  echo "Neo4j container is not running. Starting it now..."
  
  # Start with Graph Data Science Library for enhanced visualizations
  ./export_and_setup_neo4j.sh --with-gds
  
  # Wait for Neo4j to start
  echo "Waiting for Neo4j to start..."
  sleep 20
  
  # Verify Neo4j is running
  if ! docker ps | grep -q neo4j-kg; then
    echo "Error: Failed to start Neo4j container. Please check the logs with 'docker logs neo4j-kg'."
    exit 1
  fi
  
  echo "Neo4j started successfully with username 'neo4j' and password 'password'."
else
  echo "Neo4j container is already running."
fi

# Open the visualization in the default browser
echo "Opening Neovis.js visualization in the browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  open neovis_visualization.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # Linux
  xdg-open neovis_visualization.html
else
  # Windows
  start neovis_visualization.html
fi

echo ""
echo "Visualization opened in browser."
echo "Connection details:"
echo "  URL: bolt://localhost:7687"
echo "  Username: neo4j"
echo "  Password: password"
echo ""
echo "If you encounter connection errors:"
echo "1. Make sure Neo4j is running: docker ps | grep neo4j-kg"
echo "2. Check Neo4j logs: docker logs neo4j-kg"
echo "3. Restart Neo4j if needed: docker restart neo4j-kg"
