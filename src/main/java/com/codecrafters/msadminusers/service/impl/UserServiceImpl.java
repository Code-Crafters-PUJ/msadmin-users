package com.codecrafters.msadminusers.service.impl;

import com.codecrafters.msadminusers.domain.Account;
import com.codecrafters.msadminusers.repository.UserRepository;
import com.codecrafters.msadminusers.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    @Override
    public UserDetailsService userDetailsService() {
        return new UserDetailsService() {
            @Override
            public UserDetails loadUserByUsername(String username) {
                return (UserDetails) userRepository.findByEmail(username)
                        .orElseThrow(() -> new UsernameNotFoundException("User not found"));
            }
        };

    }

    public Account getUserById(Integer id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));
    }

    public void deleteById(Integer id) {
        userRepository.deleteById(id);
    }

    @Override
    public Account save(Account user) {
        return userRepository.save(user);
    }
}
