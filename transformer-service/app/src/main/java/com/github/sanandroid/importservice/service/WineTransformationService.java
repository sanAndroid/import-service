package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.model.wine.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.repository.WineRepository;
import com.github.sanandroid.importservice.transformer.WineTransformer;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

@Service
public class WineTransformationService extends AbstractTransformationService<WineDto, WineEntity, WineRepository, WineTransformer> {


    public WineTransformationService(WineRepository repository, WineTransformer transformer) {
        super(repository,transformer);
    }

    @Transactional
    public void persistDto(WineDto input) {
        WineEntity entity = transformer.transformToEntity(input);
        repository.upsert(entity);
    }
}
