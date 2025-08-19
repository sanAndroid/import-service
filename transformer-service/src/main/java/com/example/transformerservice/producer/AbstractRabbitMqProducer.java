package com.example.transformerservice.producer;

import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AbstractRabbitMqProducer<O> {

    private final RabbitTemplate rabbitTemplate;
    private final Queue queue;

    @Autowired
    public AbstractRabbitMqProducer(RabbitTemplate rabbitTemplate, Queue queue) {
        this.rabbitTemplate = rabbitTemplate;
        this.queue = queue;
    }

    public void sendMessage(O output) {
        rabbitTemplate.convertAndSend(queue.getName(), output);
    }
}
