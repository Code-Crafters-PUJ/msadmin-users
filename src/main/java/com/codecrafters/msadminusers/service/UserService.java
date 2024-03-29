package com.codecrafters.msadminusers.service;

import com.codecrafters.msadminusers.domain.Account;
import com.codecrafters.msadminusers.repository.CredentialsRepository;
import com.codecrafters.msadminusers.repository.UserRepository;
import jakarta.persistence.criteria.CriteriaBuilder;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Set;
import java.util.stream.Collectors;

@Service
public class UserService implements UserDetailsService {

    private UserRepository userRepositorys;
    private CredentialsRepository credentialsRepository;

    public UserService(UserRepository userRepository) {
        this.userRepositorys = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String Email) throws UsernameNotFoundException {
        Account user = userRepositorys.findByEmail(Email)
                .orElseThrow(() ->
                        new UsernameNotFoundException("User not found with username or email: "+ Email));

        Set<GrantedAuthority> authorities = user
                .getRoles()
                .stream()
                .map((role) -> new SimpleGrantedAuthority(role.getDescription())).collect(Collectors.toSet());

        return new org.springframework.security.core.userdetails.User(user.getEmail(),
                user.getPassword(),
                authorities);
    }


    public Account getUserId(Integer id) {
        return userRepositorys.findById(id).orElse(null);
    }

    public void deleteById(Integer id) {
        userRepositorys.deleteById(id);
    }

    public Account save(Account user) {
        return userRepositorys.save(user);
    }
}
