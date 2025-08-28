package com.github.sanandroid.importservice.consumer;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.model.wine.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.repository.WineRepository;
import com.github.sanandroid.importservice.service.WineTransformationService;
import com.github.sanandroid.importservice.transformer.WineTransformer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;

@Service
public class WineConsumer extends AbstractConsumer<WineDto, WineEntity, WineRepository, WineTransformer> {

    private static final Logger log = LoggerFactory.getLogger(WineConsumer.class);

    public WineConsumer(WineTransformationService transformationService, ObjectMapper objectMapper) {
        super(WineDto.class, transformationService, objectMapper);
    }

    @Override
    @RabbitListener(queues = "${app.rabbitmq.wines-queue}")
    public void receiveMessage(Message message) {
        log.info("Received message on wines queue");
        String body = new String(message.getBody(), StandardCharsets.UTF_8);
        processMessage(body);
    }
}
