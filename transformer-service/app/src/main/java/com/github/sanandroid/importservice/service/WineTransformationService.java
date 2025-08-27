package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.client.VectorizeClient;
import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.model.wine.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.repository.WineRepository;
import com.github.sanandroid.importservice.transformer.WineTransformer;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class WineTransformationService extends AbstractTransformationService<WineDto, WineEntity, WineRepository, WineTransformer> {

    final private VectorizeClient vectorizeClient;
    private static final Logger log = LoggerFactory.getLogger(WineTransformationService.class);

    protected WineTransformationService(
            WineRepository repository,
            WineTransformer transformer,
            VectorizeClient vectorizeClient
    ) {
        super(repository, transformer);
        this.vectorizeClient = vectorizeClient;
    }

    @Transactional
    public void transformAndSend(WineDto input) {
        float[] embedding = vectorizeClient.getEmbeddingForWine(input.name(), input.grapeVarieties().toString(), input.vintage().toString(), input.region());
        WineEntity entity = transformer.transformToEntity(input);
        entity.setEmbedding(embedding);
        repository.upsert(entity);
    }
}