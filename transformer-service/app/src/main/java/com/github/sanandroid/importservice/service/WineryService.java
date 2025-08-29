package com.github.sanandroid.importservice.service;

// TODO: See how to implement that later import com.github.sanandroid.importservice.model.winery.WineryDto;

import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.AbstractWineryTransformer;
import jakarta.persistence.EntityNotFoundException;

public class WineryService<I>
        extends AbstractService<
        I,
        WineryEntity,
        WineryRepository,
        AbstractWineryTransformer<I>
        > {

    protected WineryService(
            WineryRepository repository,
            AbstractWineryTransformer<I> transformer
    ) {
        super(repository, transformer);
    }

    WineryEntity findOrCreatePlaceholder(String website) {
        return repository.findByWebsite(website).orElseGet(() -> {
            var entity = new WineryEntity();
            entity.setWebsite(website);
            entity.setName("placeholder");
            entity.setEmbedding(new float[384]);
            repository.insertIfNotExists(entity);
            return repository.findByWebsite(website)
                    .orElseThrow(() -> new EntityNotFoundException(STR."Just created an Winery with website \{website}. Entity should exist"));
        });

    }
}