package com.codecrafters.msadminusers.repository;

import com.codecrafters.msadminusers.domain.Account;
import com.codecrafters.msadminusers.domain.Credentials;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CredentialsRepository  extends JpaRepository<Credentials, String> {
    Optional<Credentials> findByAccount(Account account);
    Optional<Credentials> findByEmail(String email);
    Boolean existsByEmail(String email);
}
