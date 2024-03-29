package com.codecrafters.msadminusers.controller;

import com.codecrafters.msadminusers.DTO.LoginDto;
import com.codecrafters.msadminusers.DTO.SignUpDto;
import com.codecrafters.msadminusers.domain.Account;
import com.codecrafters.msadminusers.domain.Rol;
import com.codecrafters.msadminusers.repository.RoleRepository;
import com.codecrafters.msadminusers.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;

@RestController
@RequestMapping("/users/auth")
public class AuthController {
    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RoleRepository roleRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;
    @PostMapping("/login")
    public ResponseEntity<String> authenticateUser(@RequestBody LoginDto loginDto){
        Authentication authentication = authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(
                loginDto.getEmail(), loginDto.getPassword()));

        SecurityContextHolder.getContext().setAuthentication(authentication);
        return new ResponseEntity<>("User signed-in successfully!.", HttpStatus.OK);
    }

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@RequestBody SignUpDto signUpDto){

        // add check for username exists in a DB
        if(userRepository.existsByEmail(signUpDto.getEmail())){
            return new ResponseEntity<>("Ese correo electronico ya esta registrado!", HttpStatus.BAD_REQUEST);
        }

        // create user object
        Account user = new Account();
        user.setName(signUpDto.getName());
        user.setEmail(signUpDto.getEmail());
        user.setLast_name(signUpDto.getLast_name());
        user.setName(signUpDto.getName());
        user.setCedula(signUpDto.getCedula());
        user.setPassword(passwordEncoder.encode(signUpDto.getPassword()));
        Rol roles = roleRepository.findByName(signUpDto.getRole()).get();
        user.setRoles(Collections.singleton(roles));
        userRepository.save(user);
        return new ResponseEntity<>("Usuario regitrado exitosamente", HttpStatus.OK);

    }
}
