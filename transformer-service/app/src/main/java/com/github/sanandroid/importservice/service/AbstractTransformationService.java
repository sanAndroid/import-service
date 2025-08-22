package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.transformer.AbstractTransformer;
import lombok.AllArgsConstructor;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

@AllArgsConstructor
public abstract class AbstractTransformationService<I, E> {

    // TODO: Not sure about the UUID here
    protected final JpaRepository<E, UUID> repository;
    protected final AbstractTransformer<I, E> transformer;

    public void transformAndSend(I input) {
        E result = transformer.transform(input);
        repository.save(result);
    }
}