package com.github.sanandroid.importservice.producer;

import com.github.sanandroid.importservice.model.winery.WineryMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class WineryProducer {

    private final RabbitTemplate rabbitTemplate;
    private final ObjectMapper objectMapper;

    @Value("${app.rabbitmq.wineries-exchange}")
    private String exchange;

    @Value("${app.rabbitmq.wineries-routing-key}")
    private String routingKey;

    public WineryProducer(RabbitTemplate rabbitTemplate, ObjectMapper objectMapper) {
        this.rabbitTemplate = rabbitTemplate;
        this.objectMapper = objectMapper;
    }

    public void sendMessage(WineryMessage wineryMessage) throws JsonProcessingException {
        String message = objectMapper.writeValueAsString(wineryMessage);
        rabbitTemplate.convertAndSend(exchange, routingKey, message);
    }
}
