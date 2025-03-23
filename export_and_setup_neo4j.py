#!/usr/bin/env python3
"""
Script to export knowledge graph data from memory MCP to Neo4j.
This is a Python alternative to the bash script.
"""

import json
import os
import subprocess
import time
import sys

def run_command(command, shell=False):
    """Run a shell command and print output"""
    print(f"Running: {command if isinstance(command, str) else ' '.join(command)}")
    try:
        if shell:
            process = subprocess.run(command, shell=True, check=True, text=True)
        else:
            process = subprocess.run(command, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def export_json():
    """Export JSON data from memory MCP file"""
    print("Exporting JSON data from memory MCP file...")
    
    try:
        # Read the source JSON file line by line to handle potential JSONL format
        data = []
        with open('/Users/casazza/Documents/Cline/MCP/servers/src/memory/data/confluence_kb.json', 'r') as f:
            content = f.read()
            # Try to parse as a single JSON object first
            try:
                data = json.loads(content)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                # If that fails, try to parse as JSONL (one JSON object per line)
                lines = content.strip().split('\n')
                for line in lines:
                    if line.strip():
                        try:
                            item = json.loads(line)
                            data.append(item)
                        except json.JSONDecodeError as e:
                            print(f"Warning: Could not parse line: {line[:50]}... Error: {e}")
        
        print(f"Loaded {len(data)} items from the JSON file")
        
        # Filter and transform the data
        result = {
            "entities": [
                {"name": item["name"], "entityType": item["entityType"], "observations": item["observations"]}
                for item in data if item.get("type") == "entity"
            ],
            "relations": [
                {"from": item["from"], "to": item["to"], "relationType": item["relationType"]}
                for item in data if item.get("type") == "relation"
            ]
        }
        
        print(f"Extracted {len(result['entities'])} entities and {len(result['relations'])} relations")
        
        # Write the transformed data to kb.json
        with open('kb.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print("JSON data exported to kb.json")
        return True
    except Exception as e:
        print(f"Error exporting JSON: {e}")
        return False

def create_cypher_script():
    """Create Neo4j Cypher import script"""
    print("Creating Neo4j Cypher import script...")
    
    cypher_script = """// Clear the database
MATCH (n) DETACH DELETE n;

// Create constraints
CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;

// Load entities
CALL apoc.load.json("file:///import/kb.json") YIELD value
UNWIND value.entities AS entity
MERGE (e:Entity {name: entity.name})
SET e.entityType = entity.entityType
SET e.observations = entity.observations;

// Load relations
CALL apoc.load.json("file:///import/kb.json") YIELD value
UNWIND value.relations AS relation
MATCH (from:Entity {name: relation.from})
MATCH (to:Entity {name: relation.to})
CALL apoc.create.relationship(from, relation.relationType, {}, to) YIELD rel
RETURN rel;
"""
    
    try:
        with open('import_to_neo4j.cypher', 'w') as f:
            f.write(cypher_script)
        print("Cypher commands created in import_to_neo4j.cypher")
        return True
    except Exception as e:
        print(f"Error creating Cypher script: {e}")
        return False

def setup_neo4j(with_gds=False):
    """Start Neo4j Docker container"""
    print("Setting up Neo4j Docker container...")
    
    # Stop and remove existing container if it exists
    run_command("docker stop neo4j-kg 2>/dev/null || true", shell=True)
    run_command("docker rm neo4j-kg 2>/dev/null || true", shell=True)
    
    # Get current directory for volume mounting
    current_dir = os.getcwd()
    
    # Base Docker command
    docker_command = [
        "docker", "run", "-d",
        "--name", "neo4j-kg",
        "-p", "7474:7474", "-p", "7687:7687",
        "-v", f"{current_dir}/kb.json:/import/kb.json",
        "-v", f"{current_dir}/import_to_neo4j.cypher:/import/import_to_neo4j.cypher",
        "-e", "NEO4J_AUTH=neo4j/password",
        "-e", "NEO4J_apoc_export_file_enabled=true",
        "-e", "NEO4J_apoc_import_file_enabled=true",
        "-e", "NEO4J_apoc_import_file_use__neo4j__config=true",
    ]
    
    # Add GDS if requested
    if with_gds:
        print("Including Graph Data Science Library for enhanced visualizations...")
        docker_command.extend([
            "-e", "NEO4J_dbms_memory_heap_max__size=4G",
            "-e", "NEO4JLABS_PLUGINS=[\"apoc\", \"graph-data-science\"]",
        ])
    else:
        docker_command.extend([
            "-e", "NEO4JLABS_PLUGINS=[\"apoc\"]",
        ])
    
    # Add Neo4j image
    docker_command.append("neo4j:latest")
    
    if not run_command(docker_command):
        return False
    
    print("Waiting for Neo4j to start...")
    time.sleep(15)  # Wait for Neo4j to initialize
    return True

def import_data():
    """Import data into Neo4j"""
    print("Importing data into Neo4j...")
    
    import_command = [
        "docker", "exec", "neo4j-kg",
        "cypher-shell", "-u", "neo4j", "-p", "password",
        "-f", "/import/import_to_neo4j.cypher"
    ]
    
    if run_command(import_command):
        print("\nData import complete!")
        print("Neo4j browser is available at http://localhost:7474/")
        print("Username: neo4j")
        print("Password: password")
        print("\nSample Cypher queries to try:")
        print("1. View all entities: MATCH (n:Entity) RETURN n LIMIT 25")
        print("2. View all relations: MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25")
        print("3. Find entities by type: MATCH (n:Entity) WHERE n.entityType = 'ContentSection' RETURN n")
        print("4. Find relations by type: MATCH (n)-[r]->(m) WHERE type(r) = 'contains' RETURN n, r, m")
        return True
    return False

def main():
    """Main function to run the export and setup process"""
    print("Starting knowledge graph export and Neo4j setup...")
    
    # Parse command line arguments
    with_gds = False
    if len(sys.argv) > 1 and sys.argv[1] == "--with-gds":
        with_gds = True
        print("Graph Data Science Library will be included for enhanced visualizations.")
    
    # Check for Docker
    if not run_command(["docker", "--version"]):
        print("Docker is required but not available. Please install Docker and try again.")
        sys.exit(1)
    
    # Execute each step
    if not export_json():
        sys.exit(1)
    
    if not create_cypher_script():
        sys.exit(1)
    
    if not setup_neo4j(with_gds):
        sys.exit(1)
    
    if not import_data():
        sys.exit(1)
    
    print("\nProcess completed successfully!")
    
    if with_gds:
        print("\nGraph Data Science Library is included. You can use algorithms like PageRank and community detection.")
        print("See neo4j_visualization_plugins.md for example queries using these algorithms.")
    else:
        print("\nTip: Run with --with-gds flag to include Graph Data Science Library for enhanced visualizations:")
        print("     ./export_and_setup_neo4j.py --with-gds")

if __name__ == "__main__":
    main()
