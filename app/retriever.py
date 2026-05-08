import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


class SHLRetriever:

    def __init__(self):

        with open(
            "data/shl_catalog.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.catalog = json.load(f)

        self.index = None
        self.embeddings = None

        self.build_index()

    def build_index(self):

        documents = []

        for item in self.catalog:

            text = f"""
            Assessment Name:
            {item.get('name', '')}

            Description:
            {item.get('description', '')}

            Test Type:
            {item.get('test_type', '')}

            URL:
            {item.get('url', '')}
            """

            documents.append(text)

        print("Creating embeddings...")

        embeddings = model.encode(
            documents,
            show_progress_bar=True
        )

        embeddings = np.array(
            embeddings
        ).astype("float32")

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)

        index.add(embeddings)

        self.index = index
        self.embeddings = embeddings

        print(f"Indexed {len(documents)} assessments")

    def search(self, query, top_k=5):

        expanded_query = f"""
        Role requirements:
        {query}

        Relevant skills:
        coding
        technical
        communication
        stakeholder management
        leadership
        personality
        software engineering
        collaboration
        problem solving
        teamwork
        """

        query_embedding = model.encode(
            [expanded_query]
        )

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx < len(self.catalog):

                results.append({
                    **self.catalog[idx],
                    "score": float(distance)
                })

        return results