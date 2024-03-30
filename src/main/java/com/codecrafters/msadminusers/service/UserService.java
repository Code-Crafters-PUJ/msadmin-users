package com.codecrafters.msadminusers.service;


import com.codecrafters.msadminusers.domain.Account;
import org.springframework.security.core.userdetails.UserDetailsService;


public interface UserService {
    UserDetailsService userDetailsService();

    Account getUserById(Integer id);

    void deleteById(Long id);

    Account save(Account user);




}