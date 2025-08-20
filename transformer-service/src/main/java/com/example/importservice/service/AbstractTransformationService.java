package com.example.importservice.service;

import com.example.importservice.producer.AbstractRabbitMqProducer;
import com.example.importservice.transformer.AbstractTransformer;

public abstract class AbstractTransformationService<I, O> {

    protected final AbstractRabbitMqProducer<O> producer;
    protected final AbstractTransformer<I, O> transformer;

    protected AbstractTransformationService(
            AbstractRabbitMqProducer<O> producer,
            AbstractTransformer<I, O> transformer
    ) {
        this.producer = producer;
        this.transformer = transformer;
    }

    public void transformAndSend(I input) {
        O result = transformer.transform(input);
        producer.sendMessage(result);
    }
}