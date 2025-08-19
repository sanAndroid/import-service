package com.example.transformerservice.consumer;

import com.example.transformerservice.producer.AbstractRabbitMqProducer;
import com.example.transformerservice.service.AbstractTransformationService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;

public abstract class AbstractConsumer<I,O> {

    protected final AbstractTransformationService<I,O> abstractTransformationService;
    protected final AbstractRabbitMqProducer<O> rabbitMqProducer;
    protected final ObjectMapper objectMapper;

    @Autowired
    public AbstractConsumer(AbstractTransformationService abstractTransformationService, AbstractRabbitMqProducer rabbitMqProducer, ObjectMapper objectMapper) {
        this.abstractTransformationService = abstractTransformationService;
        this.rabbitMqProducer = rabbitMqProducer;
        this.objectMapper = objectMapper;
    }

    @RabbitListener(queues = "${app.rabbitmq.vdp-wineries-queue}")
    public void receiveMessage(String message) {
        processMessage(message);
    }

    protected abstract void processMessage(String message);
}
