package com.github.sanandroid.importservice.consumer;

import com.github.sanandroid.importservice.model.winery.VdpWineryDto;
import com.github.sanandroid.importservice.service.VdpWineryTransformationService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.amqp.core.Message;

import java.nio.charset.StandardCharsets;

import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class VdpWineryConsumerTest {

    @Mock
    private VdpWineryTransformationService transformationService;

    @Mock
    private ObjectMapper objectMapper;

    @InjectMocks
    private VdpWineryConsumer consumer;

    @Test
    void receiveMessage_shouldProcessMessage() throws JsonProcessingException {
        String json = "{\"name\":\"testName\"}";
        VdpWineryDto vdpWineryDto = new VdpWineryDto("testName", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null);
        Message message = new Message(json.getBytes(StandardCharsets.UTF_8));

        when(objectMapper.readValue(json, VdpWineryDto.class)).thenReturn(vdpWineryDto);

        consumer.receiveMessage(message);

        verify(transformationService).persistDto(vdpWineryDto);
    }
}
