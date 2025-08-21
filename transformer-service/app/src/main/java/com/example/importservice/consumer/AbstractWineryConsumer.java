package com.example.importservice.consumer;

import com.example.importservice.model.ImportedWinery;
import com.example.importservice.model.Winery;
import com.example.importservice.model.WineryEntity;
import com.example.importservice.service.AbstractWineryTransformationService;
import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class AbstractWineryConsumer<I extends ImportedWinery> extends AbstractConsumer<I, WineryEntity> {

    public AbstractWineryConsumer(Class<I> type, AbstractWineryTransformationService<I> abstractTransformationService, ObjectMapper objectMapper) {
        super(type, abstractTransformationService, objectMapper);
    }
}