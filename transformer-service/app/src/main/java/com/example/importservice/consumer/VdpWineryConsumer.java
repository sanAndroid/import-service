package com.example.importservice.consumer;

import com.example.importservice.model.VdpWinery;
import com.example.importservice.service.VdpWineryTransformationService;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;

@Service
public class VdpWineryConsumer extends AbstractWineryConsumer<VdpWinery> {

    @Value("${app.rabbitmq.vdp-wineries-queue}")
    private String queueName;


    @PostConstruct
    void checkQueueName() {
        System.out.println("Listening to queue: " + queueName);
    }

    @Autowired
    public VdpWineryConsumer(VdpWineryTransformationService abstractTransformationService, ObjectMapper objectMapper) {
        super(VdpWinery.class, abstractTransformationService, objectMapper);
    }

    @Override
    @RabbitListener(queues = "${app.rabbitmq.vdp-wineries-queue}")
    public void receiveMessage(Message message) {
        String body = new String(message.getBody(), StandardCharsets.UTF_8);
        processMessage(body);
    }
}
