import logging
import weaviate
import weaviate.classes.config as wvcc


class WeaviateClient:
    def __init__(self, host, port, grpc_port):
        self.client = weaviate.connect_to_local(host, port, grpc_port)
        self._setup_collection()
        self.paragraph_collection = self.client.collections.get(name="Paragraphs")
        logging.debug(f"Connected to Weaviate at {host}:{port} on gRPC port {grpc_port}!")

    def _setup_collection(self):
        # Define the schema for paragraphs collection
        self.client.collections.delete_all()
        self.client.collections.create(
            name="Paragraphs",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_transformers(),
            properties=[
                wvcc.Property(
                    name="text",
                    data_type=wvcc.DataType.TEXT
                ),
                wvcc.Property(
                    name="object_key",
                    data_type=wvcc.DataType.TEXT,
                    skip_vectorization=True
                ),
                wvcc.Property(
                    name="bucket_name",
                    data_type=wvcc.DataType.TEXT,
                    skip_vectorization=True
                ),
                wvcc.Property(
                    name="position",
                    data_type=wvcc.DataType.INT,
                    skip_vectorization=True
                ),
            ]
        )

    def add_paragraph(self, text, object_key, bucket_name, position):
        self.paragraph_collection.data.insert({
            "text": text,
            "object_key": object_key,
            "bucket_name": bucket_name,
            "position": position
        })

    def search_similar_paragraphs(self, query_text, limit=5):
        # Perform a similarity search for paragraphs
        response = self.paragraph_collection.query.search(
            query=query_text,
            limit=limit
        )
        return response

    def close(self):
        self.client.close()
