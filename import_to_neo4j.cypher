// Clear the database
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
