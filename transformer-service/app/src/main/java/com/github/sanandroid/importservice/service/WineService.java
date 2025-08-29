package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.model.winery.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.repository.WineRepository;
import com.github.sanandroid.importservice.transformer.WineTransformer;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

@Service
public class WineService extends AbstractService<WineDto, WineEntity, WineRepository, WineTransformer> {

    WineryService<?> wineryService;

    public WineService(WineryService<?> wineryService, WineRepository wineRepository, WineTransformer transformer) {
        super(wineRepository, transformer);
        this.wineryService = wineryService;
    }

    @Transactional
    @Override
    public void persistDto(WineDto input) {
        var wineEntity = transformer.transformToEntity(input);
        var wineryEntity = wineryService.findOrCreatePlaceholder(input.getWineryWebsite());
        wineEntity.setWinery(wineryEntity);
        // TODO: I want an upsert here
        repository.save(wineEntity);
    }
}
