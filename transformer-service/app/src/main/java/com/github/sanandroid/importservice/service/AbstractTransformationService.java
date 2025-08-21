package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.transformer.AbstractTransformer;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public abstract class AbstractTransformationService<I, E> {

    // TODO: Not sure about the UUID here
    protected final JpaRepository<E, UUID> repository;
    protected final AbstractTransformer<I, E> transformer;

    protected AbstractTransformationService(
            JpaRepository<E,UUID> repository,
            AbstractTransformer<I, E> transformer
    ) {
        this.repository = repository;
        this.transformer = transformer;
    }

    public void transformAndSend(I input) {
        E result = transformer.transform(input);
        repository.save(result);
    }
}