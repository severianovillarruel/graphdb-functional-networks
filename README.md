# Graph Database for Target Discovery

## Background & Slide Deck

Example Neo4j project showing how CRISPR screen signals + pathway knowledge form a
gene-function network. Uses tiny CSVs you can load locally or on Neo4j Aura.

The work showcased:

**Slide Deck**
- [GraphDB Presentation](https://docs.google.com/presentation/d/1jEPNx5okzBY6yFYrrXUXGa6a3MDJX1tNxsX03oNLOBM/edit?usp=sharing)

## Contents
- `data/genes.csv` — gene nodes
- `data/pathways.csv` — pathway nodes
- `data/gene_pathways.csv` — gene–pathway edges
- `data/crispr_edges.csv` — gene–gene edges (dependency/similarity)
- `src/neo4j_loader.py` — CSV → Neo4j loader
- `queries/examples.cypher` — starter queries

## Quickstart
```bash
pip install -r requirements.txt
# set env vars (see .env.sample) then:
python src/neo4j_loader.py
```
