package com.github.sanandroid.importservice.consumer;

import com.github.sanandroid.importservice.model.ImportedWinery;
import com.github.sanandroid.importservice.model.WineryEntity;
import com.github.sanandroid.importservice.service.AbstractWineryTransformationService;
import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class AbstractWineryConsumer<I extends ImportedWinery> extends AbstractConsumer<I, WineryEntity> {

    public AbstractWineryConsumer(Class<I> type, AbstractWineryTransformationService<I> abstractTransformationService, ObjectMapper objectMapper) {
        super(type, abstractTransformationService, objectMapper);
    }
}