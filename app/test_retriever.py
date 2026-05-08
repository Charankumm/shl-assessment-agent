from app.retriever import SHLRetriever

retriever = SHLRetriever()

results = retriever.search(
    "Java developer with stakeholder communication",
    top_k=5
)

for r in results:
    print(r)