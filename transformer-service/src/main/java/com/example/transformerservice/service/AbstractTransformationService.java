package com.example.transformerservice.service;

import com.example.transformerservice.producer.AbstractRabbitMqProducer;
import com.example.transformerservice.transformer.AbstractTransformer;
import org.springframework.stereotype.Service;

@Service
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

    public O transformAndSend(I input) {
        O result = transformer.transform(input);
        producer.sendMessage(result);
        return result;
    }
}