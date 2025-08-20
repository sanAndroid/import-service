package com.example.importservice.consumer;

import com.example.importservice.service.AbstractTransformationService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.Message;
import org.springframework.beans.factory.annotation.Autowired;

public abstract class AbstractConsumer<I,O> {

    protected final Class<I> type;
    protected final AbstractTransformationService<I,O> abstractTransformationService;
    protected final ObjectMapper objectMapper;

    @Autowired
    public AbstractConsumer(Class<I> type, AbstractTransformationService<I,O> abstractTransformationService, ObjectMapper objectMapper) {
        this.type = type;
        this.abstractTransformationService = abstractTransformationService;
        this.objectMapper = objectMapper;
    }

    abstract public void receiveMessage(Message message);

    protected void processMessage(String message) {
        I deserializedMessage = null;
        try {
            deserializedMessage = objectMapper.readValue(message, type);
        } catch (JsonProcessingException e) {
            // log.error("...")
        } finally {
            abstractTransformationService.transformAndSend(deserializedMessage);
        }
    }
}
