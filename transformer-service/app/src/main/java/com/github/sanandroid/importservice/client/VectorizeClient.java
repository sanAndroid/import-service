package com.github.sanandroid.importservice.client;

import com.github.sanandroid.importservice.grpc.vectorize.WineryVectorizeRequest;
import com.github.sanandroid.importservice.grpc.vectorize.WineVectorizeRequest;
import com.github.sanandroid.importservice.grpc.vectorize.WineryVectorizeResponse;
import com.github.sanandroid.importservice.grpc.vectorize.VectorizeServiceGrpc;
import com.google.common.primitives.Floats;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class VectorizeClient {

    private final VectorizeServiceGrpc.VectorizeServiceBlockingStub stub;

    public float[] getEmbeddingForWinery(String name, String address, String region, String country) {
        WineryVectorizeRequest req = WineryVectorizeRequest.newBuilder()
                .setName(name == null ? "" : name)
                .setAddress(address == null ? "" : address)
                .setRegion(region == null ? "" : region)
                .setCountry(country == null ? "" : country)
                .build();
        WineryVectorizeResponse resp = stub.getWineryEmbeddingVector(req);
        return Floats.toArray(resp.getEmbeddingList());
    }

    public float[] getEmbeddingForWine(String name, String type, String winery, java.util.List<String> grapes) {
        WineVectorizeRequest.Builder builder = WineVectorizeRequest.newBuilder()
                .setName(name == null ? "" : name)
                .setType(type == null ? "" : type)
                .setWinery(winery == null ? "" : winery);
        if (grapes != null) {
            builder.addAllGrapes(grapes);
        }
        WineVectorizeRequest req = builder.build();
        WineryVectorizeResponse resp = stub.getWineEmbeddingVector(req);
        return Floats.toArray(resp.getEmbeddingList());
    }

}