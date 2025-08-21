package com.example.importservice.client;

import com.example.importservice.grpc.vectorize.VectorizeRequest;
import com.example.importservice.grpc.vectorize.VectorizeResponse;
import com.example.importservice.grpc.vectorize.VectorizeServiceGrpc;
import com.google.common.primitives.Floats;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class VectorizeClient {

    private final VectorizeServiceGrpc.VectorizeServiceBlockingStub stub;

    public float[] getEmbedding(String name, String address, String region, String country) {
        VectorizeRequest req = VectorizeRequest.newBuilder()
                .setName(name == null ? "" : name)
                .setAddress(address == null ? "" : address)
                .setRegion(region == null ? "" : region)
                .setCountry(country == null ? "" : country)
                .build();

        VectorizeResponse resp = stub.getEmbeddingVector(req);
        return Floats.toArray(resp.getEmbeddingList());
    }
}