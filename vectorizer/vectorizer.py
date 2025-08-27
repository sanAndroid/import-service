from concurrent import futures
import grpc
from sentence_transformers import SentenceTransformer

import vectorize_pb2 as pb
import vectorize_pb2_grpc as pbg

# Load once, reuse
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim

def join_winery_fields(req: pb.WineryVectorizeRequest) -> str:
    # Simple concatenation; tune as needed
    parts = [req.name, req.address, req.region, req.country]
    return " | ".join(p for p in parts if p)

def join_wine_fields(req: pb.WineVectorizeRequest) -> str:
    # Simple concatenation; tune as needed
    parts = [req.name, req.type, req.winery]
    if req.grapes:
        parts.extend(req.grapes)
    return " | ".join(p for p in parts if p)

class VectorizeService(pbg.VectorizeServiceServicer):
    def GetWineryEmbeddingVector(self, request: pb.WineryVectorizeRequest, context):
        text = join_winery_fields(request)
        vec = model.encode(text)  # np.ndarray shape (384,)
        # Ensure python floats (not numpy types)
        embedding = [float(x) for x in vec.tolist()]
        return pb.VectorizeResponse(embedding=embedding, dim=len(embedding))

    def GetWineEmbeddingVector(self, request: pb.WineVectorizeRequest, context):
        text = join_wine_fields(request)
        vec = model.encode(text)  # np.ndarray shape (384,)
        # Ensure python floats (not numpy types)
        embedding = [float(x) for x in vec.tolist()]
        return pb.VectorizeResponse(embedding=embedding, dim=len(embedding))

def serve(host="0.0.0.0", port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pbg.add_VectorizeServiceServicer_to_server(VectorizeService(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"gRPC server listening on {host}:{port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
