package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.model.winery.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineRepository;
import com.github.sanandroid.importservice.persistence.repository.WineryTransformationService;
import com.github.sanandroid.importservice.transformer.WineTransformer;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

@Service
public class WineTransformationService extends AbstractTransformationService<WineDto, WineEntity, WineRepository, WineTransformer> {

    WineryTransformationService wineryService;

    public WineTransformationService(WineryTransformationService wineryTransformationService, WineRepository wineRepository, WineTransformer transformer) {
        super(wineRepository,transformer);
    }

    @Transactional
    public void persistDto(WineDto input) {
        WineEntity entity = transformer.transformToEntity(input);
        WineryEntity winery = wineryService.findOrCreatePlaceholder(dto.website(), dto.sourceUrl());
        repository.upsert(entity);
    }
}
