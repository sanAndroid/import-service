package com.example.importservice.client;

import com.example.importservice.grpc.vectorize.VectorizeRequest;
import com.example.importservice.grpc.vectorize.VectorizeResponse;
import com.example.importservice.grpc.vectorize.VectorizeServiceGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import com.google.common.primitives.Floats;


public class VectorizeClient implements AutoCloseable {
    private final ManagedChannel channel;
    private final VectorizeServiceGrpc.VectorizeServiceBlockingStub stub;

    // e.g. "localhost", 50051
    public VectorizeClient(String host, int port) {
        this.channel = ManagedChannelBuilder.forAddress(host, port)
                .usePlaintext()            // dev only; use TLS in prod
                .build();
        this.stub = VectorizeServiceGrpc.newBlockingStub(channel);
    }

    /** Sends input and returns VectorizeResponse.message */
    public float[] getEmbeddingVector(String name, String address, String region, String country) {
        VectorizeRequest req = VectorizeRequest.newBuilder()
                .setName(name)             // rename in proto if you prefer 'message'
                .setAddress(address)
                .setRegion(region)
                .setCountry(country)
                .build();

        VectorizeResponse resp = stub.getEmbeddingVector(req);

        float[] vec = Floats.toArray(resp.getEmbeddingList());
        if (resp.getDim() != 0 && resp.getDim() != vec.length) {
            throw new IllegalStateException("Unexpected embedding size: " + vec.length);
        }
        return vec;
    }

    @Override public void close() {
        channel.shutdownNow();
    }
}