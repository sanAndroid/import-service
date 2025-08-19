package com.example.transformerservice.consumer;

import com.example.transformerservice.model.VdpWinery;
import com.example.transformerservice.model.Winery;
import com.example.transformerservice.producer.AbstractRabbitMqProducer;
import com.example.transformerservice.service.AbstractTransformationService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryConsumer extends AbstractWineryConsumer<VdpWinery, Winery> {

    @Autowired
    public VdpWineryConsumer(AbstractTransformationService<VdpWinery, Winery> abstractTransformationService, AbstractRabbitMqProducer<Winery> rabbitMqProducer, ObjectMapper objectMapper) {
        super(abstractTransformationService, rabbitMqProducer, objectMapper);
    }

    @Override
    @RabbitListener(queues = "${app.rabbitmq.vdp-wineries-queue}")
    protected void processMessage(String message) {
        try {
            VdpWinery vdpWinery = objectMapper.readValue(message, VdpWinery.class);
            Winery winery = abstractTransformationService.transform(vdpWinery);
            rabbitMqProducer.sendMessage(winery);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
