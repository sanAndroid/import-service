package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.repository.WineRepository;
import com.github.sanandroid.importservice.transformer.WineTransformer;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

@Service
public class WineTransformationService extends AbstractTransformationService<Wine> {

    private final WineRepository repository;
    private final WineTransformer transformer;

    public WineTransformationService(WineRepository repository, WineTransformer transformer) {
        this.repository = repository;
        this.transformer = transformer;
    }

    @Transactional
    public void transformAndSave(Wine input) {
        WineEntity entity = transformer.transformToEntity(input);
        repository.upsert(entity);
    }
}
