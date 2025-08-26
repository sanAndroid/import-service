package com.github.sanandroid.importservice.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.github.sanandroid.importservice.client.VectorizeClient;
import com.github.sanandroid.importservice.model.VdpWinery;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.producer.WineryProducer;
import com.github.sanandroid.importservice.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.VdpWineryTransformer;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformationService extends AbstractWineryTransformationService<VdpWinery> {

    final private VectorizeClient vectorizeClient;
    final private WineryProducer wineryProducer;

    protected VdpWineryTransformationService(
            WineryRepository repository,
            VdpWineryTransformer transformer,
            VectorizeClient vectorizeClient,
            WineryProducer wineryProducer
    ) {
        super(repository, transformer);
        this.vectorizeClient = vectorizeClient;
        this.wineryProducer = wineryProducer;
    }

    public void transformAndSend(VdpWinery input) {
        float[] embedding = vectorizeClient.getEmbedding(input.name(),input.postalCity(),input.region(),"germany");
        WineryEntity result = transformer.transform(input);
        result.setEmbedding(embedding);
        repository.save(result);
        try {
            wineryProducer.sendMessage(result);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}