package com.github.sanandroid.importservice.consumer;

import com.github.sanandroid.importservice.service.AbstractService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.sanandroid.importservice.transformer.AbstractTransformer;
import org.springframework.amqp.core.Message;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public abstract class AbstractConsumer<I, E, REPO extends JpaRepository<E,UUID>, TRANS extends AbstractTransformer<I,E>> {

    protected final Class<I> type;
    protected final AbstractService<I, E, REPO, TRANS > abstractService;
    protected final ObjectMapper objectMapper;

    @Autowired
    public AbstractConsumer(Class<I> type, AbstractService<I, E, REPO, TRANS> abstractService, ObjectMapper objectMapper) {
        this.type = type;
        this.abstractService = abstractService;
        this.objectMapper = objectMapper;
    }

    abstract public void receiveMessage(Message message);

    protected void processMessage(String message) {
        try {
            I deserializedMessage = objectMapper.readValue(message, type);
            abstractService.persistDto(deserializedMessage);
        } catch (JsonProcessingException e) {
            System.err.println("Failed to deserialize message: " + message);
            e.printStackTrace();
        }
    }
}
