package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.client.VectorizeClient;
import com.github.sanandroid.importservice.model.VdpWinery;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.VdpWineryTransformer;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformationService extends AbstractWineryTransformationService<VdpWinery> {

    final private VectorizeClient vectorizeClient;

    protected VdpWineryTransformationService(
            WineryRepository repository,
            VdpWineryTransformer transformer,
            VectorizeClient vectorizeClient, VectorizeClient vectorizeClient1
    ) {
        super(repository, transformer);
        this.vectorizeClient = vectorizeClient1;
    }

    public void transformAndSend(VdpWinery input) {
        float[] embedding = vectorizeClient.getEmbedding(input.name(),input.postalCity(),input.region(),"germany");
        WineryEntity result = transformer.transform(input);
        result.setEmbedding(embedding);
        repository.save(result);
    }
}