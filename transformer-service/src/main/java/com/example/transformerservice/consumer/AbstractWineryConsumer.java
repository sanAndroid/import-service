package com.example.transformerservice.consumer;

import com.example.transformerservice.model.ImportedWinery;
import com.example.transformerservice.model.Winery;
import com.example.transformerservice.service.AbstractWineryTransformationService;
import com.fasterxml.jackson.databind.ObjectMapper;

public abstract class AbstractWineryConsumer<I extends ImportedWinery> extends AbstractConsumer<I, Winery> {

    public AbstractWineryConsumer(Class<I> type, AbstractWineryTransformationService<I> abstractTransformationService, ObjectMapper objectMapper) {
        super(type, abstractTransformationService, objectMapper);
    }
}