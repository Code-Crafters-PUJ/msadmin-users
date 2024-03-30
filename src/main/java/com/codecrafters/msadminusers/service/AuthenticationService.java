package com.codecrafters.msadminusers.service;

import com.codecrafters.msadminusers.dao.request.SignUpRequest;
import com.codecrafters.msadminusers.dao.request.SigninRequest;
import com.codecrafters.msadminusers.dao.response.JwtAuthenticationResponse;

public interface AuthenticationService {
    JwtAuthenticationResponse signup(SignUpRequest request);

    JwtAuthenticationResponse signin(SigninRequest request);
}
