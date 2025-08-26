package com.github.sanandroid.importservice.config;

import org.springframework.amqp.core.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMqVdpConfig {

    @Value("${app.rabbitmq.vdp-wineries-queue}")
    private String vdpWineriesQueue;

    @Value("${app.rabbitmq.wineries-queue}")
    private String wineriesQueue;

    @Value("${app.rabbitmq.wineries-exchange}")
    private String wineriesExchange;

    @Value("${app.rabbitmq.wineries-routing-key}")
    private String wineriesRoutingKey;

    @Bean
    public Queue vdpWineriesQueue() {
        return new Queue(vdpWineriesQueue, true);
    }

    @Bean
    public Queue wineriesQueue() {
            return QueueBuilder.durable(wineriesQueue).build(); // durable = true
    }


    @Bean
    public TopicExchange wineriesExchange() {
        return ExchangeBuilder.topicExchange(wineriesExchange).durable(true).build();
    }

    @Bean
    public Binding wineriesBinding(Queue wineriesQueue, TopicExchange wineriesExchange) {
        return BindingBuilder.bind(wineriesQueue)
                .to(wineriesExchange)
                .with(wineriesRoutingKey);
    }
}
