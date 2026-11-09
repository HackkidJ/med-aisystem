package com.med.medsystem.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class PythonServerConfig {
    
    @Bean
    @ConfigurationProperties(prefix = "ai.python-server")
    public PythonServerProperties PythonServerProperties(){
        return new PythonServerProperties();
    }

    @Bean
    public RestTemplate pythonRestTemplate() {
        return new RestTemplate();
    }
}
