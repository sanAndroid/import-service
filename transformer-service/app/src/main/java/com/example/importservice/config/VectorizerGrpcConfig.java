package com.example.importservice.config;

import com.example.importservice.grpc.vectorize.VectorizeServiceGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(VectorizerGrpcProperties.class)
public class VectorizerGrpcConfig {

    @Bean(destroyMethod = "shutdownNow")
    public ManagedChannel vectorizerChannel(VectorizerGrpcProperties p) {
        ManagedChannelBuilder<?> b = ManagedChannelBuilder.forAddress(p.getHost(), p.getPort());
        if (p.isPlaintext()) b.usePlaintext();
        return b.build();
    }

    @Bean
    public VectorizeServiceGrpc.VectorizeServiceBlockingStub vectorizeBlockingStub(ManagedChannel ch) {
        return VectorizeServiceGrpc.newBlockingStub(ch);
    }
}