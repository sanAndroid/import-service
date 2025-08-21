package com.example.importservice.producer;

import com.example.importservice.model.Winery;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
public class WineryProducer extends AbstractRabbitMqProducer<Winery> {

    @Autowired
    public WineryProducer(RabbitTemplate rabbitTemplate, @Qualifier("wineriesQueue") Queue queue) {
        super(rabbitTemplate,queue);
    }
}
