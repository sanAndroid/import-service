package com.github.sanandroid.importservice.consumer;

import com.github.sanandroid.importservice.client.VectorizeClient;
import com.github.sanandroid.importservice.model.VdpWinery;
import com.github.sanandroid.importservice.repository.WineryRepository;
import org.junit.jupiter.api.Test;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.containers.RabbitMQContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@SpringBootTest
@Testcontainers
@ActiveProfiles("test")
class VdpWineryConsumerIT {

    @Container
    static RabbitMQContainer rabbitMqContainer = new RabbitMQContainer("rabbitmq:3.13-management");
    @Container
    static PostgreSQLContainer<?> postgreSQLContainer = new PostgreSQLContainer<>("pgvector/pgvector:pg16");

    @DynamicPropertySource
    static void configure(DynamicPropertyRegistry registry) {
        registry.add("spring.rabbitmq.host", rabbitMqContainer::getHost);
        registry.add("spring.rabbitmq.port", rabbitMqContainer::getAmqpPort);
        registry.add("spring.rabbitmq.username", rabbitMqContainer::getAdminUsername);
        registry.add("spring.rabbitmq.password", rabbitMqContainer::getAdminPassword);
        registry.add("spring.datasource.url", postgreSQLContainer::getJdbcUrl);
        registry.add("spring.datasource.username", postgreSQLContainer::getUsername);
        registry.add("spring.datasource.password", postgreSQLContainer::getPassword);
    }

    @Autowired
    private RabbitTemplate rabbitTemplate;
    @Autowired
    private WineryRepository wineryRepository;
    @MockBean
    private VectorizeClient vectorizeClient;

    @Test
    void shouldConsumeMessageAndTransform() {
        float[] embedding = new float[384];
        when(vectorizeClient.getEmbedding(any(String.class), any(String.class), any(String.class), any(String.class))).thenReturn(embedding);
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
            var wineries = wineryRepository.findAll();
            assertThat(wineries).hasSize(1);
            var winery = wineries.get(0);
            assertThat(winery.getName()).isEqualTo("test winery");
        });
    }
}