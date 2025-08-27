package com.github.sanandroid.importservice.client;

import com.github.sanandroid.importservice.grpc.vectorize.VectorizeRequest;
import com.github.sanandroid.importservice.grpc.vectorize.VectorizeResponse;
import com.github.sanandroid.importservice.grpc.vectorize.VectorizeServiceGrpc;
import com.google.common.primitives.Floats;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class VectorizeClient {

    private final VectorizeServiceGrpc.VectorizeServiceBlockingStub stub;

    public float[] getEmbeddingForWinery(String name, String address, String region, String country) {
        VectorizeRequest req = VectorizeRequest.newBuilder()
                .setName(name == null ? "" : name)
                .setAddress(address == null ? "" : address)
                .setRegion(region == null ? "" : region)
                .setCountry(country == null ? "" : country)
                .build();
        VectorizeResponse resp = stub.getEmbeddingVector(req);
        return Floats.toArray(resp.getEmbeddingList());
    }

    // TODO: define a reasonable embeeding for wine
    public float[] getEmbeddingForWine(String name, String variety, String vintage, String region) {
        VectorizeRequest req = VectorizeRequest.newBuilder()
                .setName(name == null ? "" : name)
                .setAddress(variety == null ? "" : variety)
                .setRegion(vintage == null ? "" : vintage)
                .setCountry(region == null ? "" : region)
                .build();
        VectorizeResponse resp = stub.getEmbeddingVector(req);
        return Floats.toArray(resp.getEmbeddingList());
    }

}