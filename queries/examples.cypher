// 1) Essential (high-score) neighbors of MYC in AML
MATCH (g:Gene {symbol:'MYC'})- [e:CRISPR_DEPENDS_ON {context:'AML'}] -> (h:Gene)
WHERE e.score >= 0.6
RETURN h.symbol AS gene, e.score AS score
ORDER BY score DESC;

// 2) Genes in MAPK signaling
MATCH (g:Gene)-[:IN_PATHWAY]->(p:Pathway {name:'MAPK signaling'})
RETURN g.symbol AS gene
ORDER BY gene;

// 3) Pathway-centric ranking by CRISPR degree
MATCH (g:Gene)-[:IN_PATHWAY]->(p:Pathway)
OPTIONAL MATCH (g)-[e:CRISPR_DEPENDS_ON]->(:Gene)
WITH p.name AS pathway, g.symbol AS gene, count(e) AS crispr_degree
RETURN pathway, gene, crispr_degree
ORDER BY crispr_degree DESC;

// 4) Two-hop “similar genes” via shared pathways
MATCH (g:Gene {symbol:'BRAF'})-[:IN_PATHWAY]->(p)<-[:IN_PATHWAY]-(other:Gene)
WHERE other <> g
RETURN other.symbol AS similar, collect(DISTINCT p.name) AS shared_pathways
ORDER BY size(shared_pathways) DESC, similar;
