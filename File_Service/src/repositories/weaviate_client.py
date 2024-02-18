import logging

import weaviate
import weaviate.classes.config as wvcc
from weaviate.collections.classes.grpc import Move


class WeaviateClient:
    def __init__(self, host, port, grpc_port):
        self.client = weaviate.connect_to_local(host, port, grpc_port)
        self._setup_collection()
        self.paragraph_collection = self.client.collections.get(name="Paragraphs")
        logging.debug(
            f"Connected to Weaviate at {host}:{port} on gRPC port {grpc_port}!"
        )

    def _setup_collection(self):
        if not self.client.collections.exists("Paragraphs"):
            self.client.collections.delete_all()
            self.client.collections.create(
                name="Paragraphs",
                vectorizer_config=wvcc.Configure.Vectorizer.text2vec_transformers(),
                properties=[
                    wvcc.Property(name="text", data_type=wvcc.DataType.TEXT),
                    wvcc.Property(
                        name="object_key",
                        data_type=wvcc.DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    wvcc.Property(
                        name="bucket_name",
                        data_type=wvcc.DataType.TEXT,
                        skip_vectorization=True,
                    ),
                    wvcc.Property(
                        name="position",
                        data_type=wvcc.DataType.INT,
                        skip_vectorization=True,
                    ),
                ],
            )

    def add_paragraph(self, text, object_key, bucket_name, position):
        self.paragraph_collection.data.insert(
            {
                "text": text,
                "object_key": object_key,
                "bucket_name": bucket_name,
                "position": position,
            }
        )

    def search_similar_paragraphs(
        self,
        query_concepts: list,
        move_towards_concepts: list,
        move_away_concepts: list,
        limit=15,
    ):
        print(
            query_concepts, move_towards_concepts, move_away_concepts, limit, flush=True
        )
        # check if move_towards_concepts and move_away_concepts are empty lists or a list with an empty string
        if (
            move_towards_concepts == [""]
            or move_away_concepts == [""]
            or (not move_towards_concepts or not move_away_concepts)
        ):
            print("MAKING PARTIAL QUERY", flush=True)
            response = self.paragraph_collection.query.near_text(
                query=query_concepts, limit=limit
            )
        else:
            print("MAKING FULL QUERY", flush=True)
            response = self.paragraph_collection.query.near_text(
                query=query_concepts,
                move_to=Move(force=0.3, concepts=move_towards_concepts),
                move_away=Move(force=0.3, concepts=move_away_concepts),
                limit=limit,
            )

        similar_paragraphs = []
        for response_object in response.objects:
            similar_paragraphs.append(response_object.properties["text"])

        return similar_paragraphs

    def close(self):
        self.client.close()
