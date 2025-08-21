package com.example.importservice.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "vectorizer.grpc")
public class VectorizerGrpcProperties {
    private String host = "localhost";
    private int port = 50051;
    private boolean plaintext = true;

    // getters/setters
    public String getHost() { return host; }
    public void setHost(String host) { this.host = host; }
    public int getPort() { return port; }
    public void setPort(int port) { this.port = port; }
    public boolean isPlaintext() { return plaintext; }
    public void setPlaintext(boolean plaintext) { this.plaintext = plaintext; }
}