package com.codecrafters.msadminusers.config;

import com.codecrafters.msadminusers.repository.UserRepository;
import com.codecrafters.msadminusers.service.UserService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    private UserService userServices;

    public SecurityConfig(UserService userService){
        this.userServices = userService;
    }

    @Bean
    public static PasswordEncoder passwordEncoder(){
        return new BCryptPasswordEncoder();
    }


    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration configuration) throws Exception {
        return configuration.getAuthenticationManager();
    }

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {

        return http
                // ... other configurations (if needed)

                .authorizeHttpRequests((authorize) -> authorize
                        // Allow GET requests to any endpoint under "/user/**"
                        .requestMatchers(HttpMethod.GET, "/user/**").permitAll()
                        // Allow all requests to endpoints under "/user/auth/**"
                        .requestMatchers("/user/auth/**").permitAll()
                        // Require authentication for all other requests
                        .anyRequest().authenticated()
                )
                .httpBasic(withDefaults())
                .build();
    }
}
