package com.example.importservice.config;

import org.springframework.amqp.core.Queue;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMqVdpConfig {

    @Value("${app.rabbitmq.vdp-wineries-queue}")
    private String vdpWineriesQueue;

    @Value("${app.rabbitmq.wineries-queue}")
    private String wineriesQueue;

    @Bean
    public Queue vdpWineriesQueue() {
        return new Queue(vdpWineriesQueue, true);
    }

    @Bean
    public Queue wineriesQueue() {
        return new Queue(wineriesQueue, true);
    }
}
