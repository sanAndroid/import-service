package com.github.sanandroid.importservice.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.amqp.core.*;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(RabbitMQConfig.Props.class)
public class RabbitMQConfig {

    // -------- Inbound (consumed by this service) --------
    @Bean
    public Queue vdpWineriesInboundQueue(Props p) {
        // Upstream can publish via default ("") exchange using routingKey=vdp_wineries
        return QueueBuilder.durable(p.getVdpWineriesQueue()).build();
    }

    @Bean
    public Queue winesInboundQueue(Props p) {
        // Upstream can publish via default ("") exchange using routingKey=wines
        return QueueBuilder.durable(p.getWinesQueue()).build();
    }

    // -------- Outbound (this service publishes) --------
    @Bean
    public TopicExchange wineriesMessageExchange(Props p) {
        return ExchangeBuilder.topicExchange(p.getWineriesExchange()).durable(true).build();
    }

    @Bean
    public Queue wineriesMessageQueue(Props p) {
        return QueueBuilder.durable(p.getWineriesOutboundQueue()).build();
    }

    @Bean
    public Binding wineriesMessageBinding(Queue wineriesMessageQueue,
                                          TopicExchange wineriesMessageExchange,
                                          Props p) {
        return BindingBuilder.bind(wineriesMessageQueue)
                .to(wineriesMessageExchange)
                .with(p.getWineriesRoutingKey());
    }

    // -------- Properties holder --------
    @Getter
    @Setter
    @ConfigurationProperties(prefix = "app.rabbitmq")
    public static class Props {
        // inbound queues
        private String vdpWineriesQueue;   // app.rabbitmq.vdp-wineries-queue
        private String winesQueue;         // app.rabbitmq.wines-queue

        // outbound exchange/queue/rk (all named "wineries_message")
        private String wineriesExchange;       // app.rabbitmq.wineries-exchange
        private String wineriesOutboundQueue;  // app.rabbitmq.wineries-outbound-queue
        private String wineriesRoutingKey;     // app.rabbitmq.wineries-routing-key

    }
}