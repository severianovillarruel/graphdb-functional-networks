import os
from pathlib import Path
import pandas as pd
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PWD  = os.getenv("NEO4J_PASSWORD", "neo4j")

root = Path(__file__).resolve().parents[1]
data = root / "data"

driver = GraphDatabase.driver(URI, auth=(USER, PWD))

def run(tx, query, params=None):
    return tx.run(query, params or {})

def main():
    genes = pd.read_csv(data / "genes.csv")
    paths = pd.read_csv(data / "pathways.csv")
    g2p   = pd.read_csv(data / "gene_pathways.csv")
    crispr = pd.read_csv(data / "crispr_edges.csv")

    with driver.session() as s:
        # constraints
        s.execute_write(run, "CREATE CONSTRAINT gene_id IF NOT EXISTS FOR (g:Gene) REQUIRE g.id IS UNIQUE;")
        s.execute_write(run, "CREATE CONSTRAINT path_id IF NOT EXISTS FOR (p:Pathway) REQUIRE p.id IS UNIQUE;")

        # genes
        for _, r in genes.iterrows():
            s.execute_write(
                run,
                "MERGE (g:Gene {id:$id}) "
                "SET g.symbol=$sym;",
                {"id": r["gene_id"], "sym": r["gene_symbol"]}
            )

        # pathways
        for _, r in paths.iterrows():
            s.execute_write(
                run,
                "MERGE (p:Pathway {id:$id}) "
                "SET p.name=$name;",
                {"id": r["pathway_id"], "name": r["name"]}
            )

        # gene–pathway
        for _, r in g2p.iterrows():
            s.execute_write(
                run,
                "MATCH (g:Gene {id:$gid}), (p:Pathway {id:$pid}) "
                "MERGE (g)-[:IN_PATHWAY]->(p);",
                {"gid": r["gene_id"], "pid": r["pathway_id"]}
            )

        # CRISPR edges (weighted, directed here; flip to undirected if you prefer)
        for _, r in crispr.iterrows():
            s.execute_write(
                run,
                "MATCH (a:Gene {id:$src}), (b:Gene {id:$dst}) "
                "MERGE (a)-[e:CRISPR_DEPENDS_ON]->(b) "
                "SET e.score=$score, e.context=$ctx;",
                {"src": r["src_gene_id"], "dst": r["dst_gene_id"], "score": float(r["score"]), "ctx": r["context"]}
            )

    driver.close()
    print("✅ Loaded: genes, pathways, gene–pathway edges, CRISPR edges.")

if __name__ == "__main__":
    main()
