package com.github.sanandroid.importservice.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.github.sanandroid.importservice.client.VectorizeClient;
import com.github.sanandroid.importservice.model.winery.VdpWineryDto;
import com.github.sanandroid.importservice.model.winery.WineryMessage;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.producer.WineryProducer;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.VdpWineryTransformer;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformationService extends AbstractWineryTransformationService<VdpWineryDto> {

    final private VectorizeClient vectorizeClient;
    final private WineryProducer wineryProducer;
    private static final Logger log = LoggerFactory.getLogger(VdpWineryTransformationService.class);

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

    @Transactional
    public void persistDto(VdpWineryDto input) {
        float[] embedding = vectorizeClient.getEmbeddingForWinery(input.name(),input.postalCity(),input.region(),"germany");
        WineryEntity entity = transformer.transformToEntity(input);
        entity.setEmbedding(embedding);
        repository.upsert(entity);
        WineryMessage record = transformer.transformToMessage(input);
        try {
            log.info("Sending Message to rabbit");
            wineryProducer.sendMessage(record);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}