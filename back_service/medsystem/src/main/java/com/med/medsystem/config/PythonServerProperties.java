package com.med.medsystem.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ai.python-server")
public class PythonServerProperties {
    private String baseUrl = "http://localhost:8082";
    private int connectTimeout = 5000;
    private int readTimeout = 300000;
    private int maxRetries = 3;

    public String getBaseUrl() {
        return this.baseUrl;
    }

    public void setBaseUrl(String url) {
        this.baseUrl = url;
    }

    public int getConnectTimeout(){
        return this.connectTimeout;
    }

    public void setConnectTimeout(int connectTimeout){
        this.connectTimeout = connectTimeout;
    }

    public int getReadTimeout(){
        return this.readTimeout;
    }

    public void setReadTimeout(int readTimeout){
        this.readTimeout = readTimeout;
    }

    public int getMaxRetries() {
        return this.maxRetries;
    }

    public void setMaxRetries(int maxRetries){
        this.maxRetries = maxRetries;
    }
}
