package com.github.sanandroid.importservice.consumer;

import com.github.sanandroid.importservice.model.winery.WineryDto;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import com.github.sanandroid.importservice.service.AbstractTransformationService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.sanandroid.importservice.transformer.AbstractWineryTransformer;

public abstract class AbstractWineryConsumer<I extends WineryDto> extends AbstractConsumer<I, WineryEntity, WineryRepository, AbstractWineryTransformer<I>> {

    public AbstractWineryConsumer(Class<I> type, AbstractTransformationService<I, WineryEntity, WineryRepository, AbstractWineryTransformer<I>> abstractTransformationService, ObjectMapper objectMapper) {
        super(type, abstractTransformationService, objectMapper);
    }
}