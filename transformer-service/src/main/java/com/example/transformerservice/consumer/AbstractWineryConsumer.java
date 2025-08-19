package com.example.transformerservice.consumer;

import com.example.transformerservice.model.ImportedWinery;
import com.example.transformerservice.producer.WineryProducer;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.annotation.RabbitListener;

public abstract class AbstractWineryConsumer<I> extends AbstractConsumer<I, ImportedWinery> {

    public AbstractWineryConsumer(AbstractWinaryTransformationService abstractTransformationService, WineryProducer rabbitMqProducer, ObjectMapper objectMapper) {
        super(abstractTransformationService, rabbitMqProducer, objectMapper);
    }

    @RabbitListener(queues = "${app.rabbitmq.vdp-wineries-queue}")
    public void receiveMessage(String message) {
        processMessage(message);
    }

    protected abstract void processMessage(String message);
}
