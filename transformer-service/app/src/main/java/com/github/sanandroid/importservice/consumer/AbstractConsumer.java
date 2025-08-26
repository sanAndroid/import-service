package com.github.sanandroid.importservice.consumer;

import com.github.sanandroid.importservice.service.AbstractTransformationService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.core.Message;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public abstract class AbstractConsumer<I, E,REPO extends JpaRepository<E,UUID>> {

    protected final Class<I> type;
    protected final AbstractTransformationService<I, E,REPO> abstractTransformationService;
    protected final ObjectMapper objectMapper;

    @Autowired
    public AbstractConsumer(Class<I> type, AbstractTransformationService<I, E, REPO> abstractTransformationService, ObjectMapper objectMapper) {
        this.type = type;
        this.abstractTransformationService = abstractTransformationService;
        this.objectMapper = objectMapper;
    }

    abstract public void receiveMessage(Message message);

    protected void processMessage(String message) {
        try {
            I deserializedMessage = objectMapper.readValue(message, type);
            abstractTransformationService.transformAndSend(deserializedMessage);
        } catch (JsonProcessingException e) {
            System.err.println("Failed to deserialize message: " + message);
            e.printStackTrace();
        }
    }
}
