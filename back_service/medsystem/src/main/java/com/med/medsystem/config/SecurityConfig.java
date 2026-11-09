package com.med.medsystem.config;

import java.util.Arrays;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import static org.springframework.security.config.Customizer.withDefaults;
import com.med.medsystem.Security.JwtAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Autowired
    private JwtAuthenticationFilter jwtAutenticationFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception{
        http
        // 启用CORS，使用Lambda DSL风格 :cite[2]
        .cors(withDefaults()) // 这里写法不变，因为本身就是通过Lambda配置的
        // 禁用CSRF，使用Lambda DSL风格 :cite[3]
        .csrf(csrf -> csrf.disable()) 
        // 授权配置，此部分已是推荐的Lambda DSL写法 :cite[10]
        .authorizeHttpRequests(authz -> authz
            // 显式放行所有OPTIONS请求 :cite[2]
            .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll() 
            // 放行您的AI接口和认证接口
            .requestMatchers("/api/ai/**").permitAll() 
            .requestMatchers("/api/auth/**").permitAll()
            .requestMatchers("/medsystem/patient/**").permitAll()
            .requestMatchers("/medsystem/doctor/**").permitAll()
            .anyRequest().authenticated()
        )
        .addFilterBefore(jwtAutenticationFilter, UsernamePasswordAuthenticationFilter.class)
        ;
    return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        // 使用allowedOriginPatterns而非addAllowedOrigin，以避免与allowCredentials(true)的冲突:cite[5]
        configuration.setAllowedOriginPatterns(Arrays.asList("*")); 
        configuration.setAllowedMethods(Arrays.asList("GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        configuration.setAllowCredentials(true); // 如果前端请求携带凭证，此项必须为true
        configuration.setMaxAge(3600L); // 预检请求缓存时间
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

    @Bean
    public PasswordEncoder passwordEncoder(){
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration authenticationConfiguration) throws Exception {
        return authenticationConfiguration.getAuthenticationManager();
    }
}
