#!/bin/bash

jq '{
  "entities": [.[] | select(.type == "entity") | {name: .name, entityType: .entityType, observations: .observations}],
  "relations": [.[] | select(.type == "relation") | {from: .from, to: .to, relationType: .relationType}]
}' temp_array.json > kb.json
