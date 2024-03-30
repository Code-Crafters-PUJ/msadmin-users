package com.codecrafters.msadminusers.service.impl;

import com.codecrafters.msadminusers.dao.request.SignUpRequest;
import com.codecrafters.msadminusers.dao.request.SigninRequest;
import com.codecrafters.msadminusers.dao.response.JwtAuthenticationResponse;
import com.codecrafters.msadminusers.repository.RoleRepository;
import com.codecrafters.msadminusers.repository.UserRepository;
import com.codecrafters.msadminusers.service.AuthenticationService;
import com.codecrafters.msadminusers.service.JwtService;

import com.codecrafters.msadminusers.domain.Account;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Collections;

@Service
@RequiredArgsConstructor
public class AuthenticationServiceImpl implements AuthenticationService {
    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    @Override
    public JwtAuthenticationResponse signup(SignUpRequest request) {
        var role = roleRepository.findByName(request.getRole());
        var user = Account.builder().firstName(request.getName()).last_name(request.getLast_name())
                .email(request.getEmail()).password(passwordEncoder.encode(request.getPassword()))

                .rol(role).build();
        userRepository.save(user);
        var jwt = jwtService.generateToken((UserDetails) user);
        return JwtAuthenticationResponse.builder().token(jwt).build();
    }

    @Override
    public JwtAuthenticationResponse signin(SigninRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword()));
        var user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password."));
        var jwt = jwtService.generateToken((UserDetails) user);
        return JwtAuthenticationResponse.builder().token(jwt).build();
    }
}
