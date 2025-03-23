# Neo4j Visualization Plugins and Extensions

Neo4j offers several visualization plugins and extensions that can enhance your knowledge graph visualization experience. Here's a comprehensive overview of the available options:

## Neo4j Browser Extensions

### 1. **Graph Apps**

Graph Apps are Neo4j-built or third-party web applications that can be installed alongside Neo4j Desktop or accessed through Neo4j Browser.

#### How to Access:
- In Neo4j Browser, click on the "Graph Apps" icon in the left sidebar
- In Neo4j Desktop, click on "Graph Apps" in the left sidebar

#### Notable Graph Apps:

- **Neo4j Bloom** (Commercial, but free for limited use)
  - Purpose-built visualization tool for exploring and presenting graph data
  - Natural language search capabilities
  - Customizable visual styles and layouts
  - Scene-based visualizations for different perspectives on your data
  - [Learn more](https://neo4j.com/product/bloom/)

- **NeoDash** (Open Source)
  - Customizable dashboard builder for Neo4j
  - Create interactive dashboards with multiple visualization types
  - Supports tables, graphs, bar charts, line charts, and more
  - [GitHub Repository](https://github.com/neo4j-labs/neodash)
  - Installation: `docker run -it --rm -p 5005:5005 neo4jlabs/neodash:latest`

- **Graph Gallery** (Open Source)
  - Collection of graph visualization examples
  - Provides templates for common visualization patterns
  - [GitHub Repository](https://github.com/neo4j-contrib/graphgallery)

### 2. **Neo4j Browser Styling**

Neo4j Browser itself has built-in styling capabilities:

- **Grass Editor**
  - Built into Neo4j Browser
  - Access via the gear icon in the visualization panel
  - Create and save styling rules based on labels and properties
  - Export and import styles as Grass files (GraphStyle)

- **Browser Settings**
  - Customize visualization defaults
  - Change relationship thickness, arrow size, etc.
  - Adjust physics simulation parameters

## JavaScript Libraries with Neo4j Integration

These libraries can be used to build custom visualization applications:

### 1. **Neovis.js** (Open Source)
- Combines Neo4j with the vis.js visualization library
- Simple integration with Neo4j's Cypher queries
- Customizable styling and layouts
- [GitHub Repository](https://github.com/neo4j-contrib/neovis.js/)
- Example setup:
  ```html
  <div id="viz"></div>
  <script>
    const viz = new NeoVis.default({
      container_id: "viz",
      server_url: "bolt://localhost:7687",
      server_user: "neo4j",
      server_password: "password",
      labels: {
        Entity: {
          caption: "name",
          size: "pagerank",
          community: "entityType"
        }
      },
      relationships: {
        contains: {
          thickness: "count",
          caption: false
        }
      },
      initial_cypher: "MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 100"
    });
    viz.render();
  </script>
  ```

### 2. **Neo4jd3.js** (Open Source)
- Combines Neo4j with D3.js
- Highly customizable visualizations
- Support for custom styling and interactions
- [GitHub Repository](https://github.com/eisman/neo4jd3)

### 3. **Popoto.js** (Open Source)
- Visual query builder for Neo4j
- Interactive graph-based search interface
- [GitHub Repository](https://github.com/Nhogs/popoto)
- [Demo](https://www.popotojs.com/)

## Neo4j APOC and Graph Data Science Library

These Neo4j extensions provide algorithms that can enhance visualizations:

### 1. **APOC** (Awesome Procedures On Cypher)
- Already included in our setup
- Provides procedures for data preparation and transformation
- Useful for creating more meaningful visualizations
- [Documentation](https://neo4j.com/labs/apoc/)

### 2. **Graph Data Science Library** (GDS)
- Algorithms for community detection, centrality, and pathfinding
- Results can be used to influence visualization (node size, color, etc.)
- [Documentation](https://neo4j.com/docs/graph-data-science/current/)
- Installation in our Docker setup:
  ```bash
  # Update the Docker run command to include GDS
  docker run -d \
      --name neo4j-kg \
      -p 7474:7474 -p 7687:7687 \
      -v "$(pwd)/kb.json:/import/kb.json" \
      -v "$(pwd)/import_to_neo4j.cypher:/import/import_to_neo4j.cypher" \
      -e NEO4J_AUTH=neo4j/password \
      -e NEO4J_apoc_export_file_enabled=true \
      -e NEO4J_apoc_import_file_enabled=true \
      -e NEO4J_apoc_import_file_use__neo4j__config=true \
      -e NEO4JLABS_PLUGINS='["apoc", "graph-data-science"]' \
      neo4j:latest
  ```

## Setting Up Advanced Visualizations

### 1. Using Graph Algorithms for Better Visualizations

Add this to your Cypher script to enhance visualizations:

```cypher
// Calculate PageRank to determine node sizes
CALL gds.pageRank.write({
  nodeProjection: 'Entity',
  relationshipProjection: {
    RELATED: {
      type: '*',
      orientation: 'NATURAL',
      aggregation: 'NONE'
    }
  },
  writeProperty: 'pagerank'
})

// Detect communities to determine node colors
CALL gds.louvain.write({
  nodeProjection: 'Entity',
  relationshipProjection: {
    RELATED: {
      type: '*',
      orientation: 'NATURAL',
      aggregation: 'NONE'
    }
  },
  writeProperty: 'community'
})
```

### 2. Setting Up NeoDash

NeoDash is one of the most powerful open-source visualization tools for Neo4j:

1. Run NeoDash container:
   ```bash
   docker run -it --rm -p 5005:5005 neo4jlabs/neodash:latest
   ```

2. Connect to your Neo4j instance:
   - URL: `bolt://localhost:7687`
   - Username: `neo4j`
   - Password: `password`

3. Create dashboards with multiple visualizations:
   - Graph visualizations
   - Bar charts of entity types
   - Tables of related entities
   - Path visualizations

## Example Visualization Queries

Here are some example queries that produce interesting visualizations:

### 1. Entity Type Distribution
```cypher
MATCH (n:Entity)
RETURN n.entityType AS EntityType, count(*) AS Count
ORDER BY Count DESC
```

### 2. Most Connected Entities
```cypher
MATCH (n:Entity)-[r]-()
RETURN n.name AS Entity, count(r) AS Connections
ORDER BY Connections DESC
LIMIT 10
```

### 3. Relationship Type Distribution
```cypher
MATCH ()-[r]-()
RETURN type(r) AS RelationType, count(*) AS Count
ORDER BY Count DESC
```

### 4. Community Visualization
```cypher
// First run the community detection algorithm
CALL gds.louvain.write({
  nodeProjection: 'Entity',
  relationshipProjection: '*',
  writeProperty: 'community'
})

// Then visualize the communities
MATCH (n:Entity)
RETURN n.community AS Community, count(*) AS Size
ORDER BY Size DESC
```

## Conclusion

For your knowledge graph visualization needs, I recommend:

1. **Start with Neo4j Browser** - It's already set up and provides good basic visualization capabilities.

2. **Try NeoDash** - For more advanced dashboards and multiple visualization types.

3. **Consider Neovis.js** - If you want to build a custom web application with more tailored visualizations.

4. **Add Graph Data Science** - To enhance your visualizations with algorithm-based sizing, coloring, and clustering.

These tools will help you get the most out of your knowledge graph visualization and exploration.
