package com.codecrafters.msadminusers.controller;


import com.codecrafters.msadminusers.dao.request.SignUpRequest;
import com.codecrafters.msadminusers.dao.request.SigninRequest;
import com.codecrafters.msadminusers.dao.response.JwtAuthenticationResponse;

import com.codecrafters.msadminusers.service.AuthenticationService;
import lombok.RequiredArgsConstructor;

import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.Optional;

@RestController
@RequestMapping("/users/auth")
@RequiredArgsConstructor
public class AuthController {
    private final AuthenticationService authenticationService;

    @PostMapping("/login")
    public ResponseEntity<JwtAuthenticationResponse> signup(@RequestBody SignUpRequest request) {
        return ResponseEntity.ok(authenticationService.signup(request));
    }

    @PostMapping("/register")
    public ResponseEntity<JwtAuthenticationResponse> signin(@RequestBody SigninRequest request) {
        return ResponseEntity.ok(authenticationService.signin(request));
    }
}
