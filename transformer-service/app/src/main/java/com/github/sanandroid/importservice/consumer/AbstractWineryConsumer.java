package com.github.sanandroid.importservice.consumer;

import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import com.github.sanandroid.importservice.service.AbstractService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.sanandroid.importservice.transformer.AbstractWineryTransformer;
// TODO: extends WineryDto -> Implement this later when generilization happens on the python side
public abstract class AbstractWineryConsumer<I > extends AbstractConsumer<I, WineryEntity, WineryRepository, AbstractWineryTransformer<I>> {

    public AbstractWineryConsumer(Class<I> type, AbstractService<I, WineryEntity, WineryRepository, AbstractWineryTransformer<I>> abstractService, ObjectMapper objectMapper) {
        super(type, abstractService, objectMapper);
    }
}