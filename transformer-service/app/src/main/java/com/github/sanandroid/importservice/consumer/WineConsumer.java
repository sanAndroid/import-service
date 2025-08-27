package com.github.sanandroid.importservice.consumer;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.service.WineTransformationService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;

@Service
public class WineConsumer extends AbstractConsumer<Wine> {

    private static final Logger log = LoggerFactory.getLogger(WineConsumer.class);
    private final WineTransformationService transformationService;

    public WineConsumer(ObjectMapper objectMapper, WineTransformationService transformationService) {
        super(objectMapper);
        this.transformationService = transformationService;
    }

    @Override
    @RabbitListener(queues = "${app.rabbitmq.wines-queue}")
    public void receiveMessage(String message) {
        log.info("Received message on wines queue");
        try {
            Wine wine = convertMessage(message, Wine.class);
            transformationService.transformAndSave(wine);
        } catch (Exception e) {
            log.error("Error processing message from wines queue", e);
        }
    }
}
