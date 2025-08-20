package com.example.importservice.consumer;

import com.example.importservice.model.VdpWinery;
import com.example.importservice.model.Winery;
import com.example.importservice.producer.WineryProducer;
import org.junit.jupiter.api.Test;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.RabbitMQContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.util.concurrent.TimeUnit;

import static org.awaitility.Awaitility.await;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;

@SpringBootTest
@Testcontainers
@ActiveProfiles("test")
class VdpWineryConsumerIT {

    @Container
    static RabbitMQContainer rabbitMqContainer = new RabbitMQContainer("rabbitmq:3.13-management");

    @DynamicPropertySource
    static void configure(DynamicPropertyRegistry registry) {
        registry.add("spring.rabbitmq.host", rabbitMqContainer::getHost);
        registry.add("spring.rabbitmq.port", rabbitMqContainer::getAmqpPort);
        registry.add("spring.rabbitmq.username", rabbitMqContainer::getAdminUsername);
        registry.add("spring.rabbitmq.password", rabbitMqContainer::getAdminPassword);
    }

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @MockBean
    private WineryProducer wineryProducer;

    @Test
    void shouldConsumeMessageAndTransform() {
        VdpWinery vdpWinery = new VdpWinery(
                "test winery",
                "test street",
                "test city",
                "12345",
                "test@test.com",
                "http://test.com",
                "always",
                "test owner",
                "test master",
                "10",
                "test variety",
                "test geology",
                "test region",
                "test features",
                "yes",
                "test membership",
                "test cert",
                "test cert",
                "test lagen",
                "http://test.com"
        );

        rabbitTemplate.convertAndSend("vdp_wineries", vdpWinery);

        await().atMost(5, TimeUnit.SECONDS).untilAsserted(() -> {
            verify(wineryProducer).sendMessage(any(Winery.class));
        });
    }
}