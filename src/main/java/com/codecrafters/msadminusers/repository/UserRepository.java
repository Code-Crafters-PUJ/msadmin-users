package com.codecrafters.msadminusers.repository;

import com.codecrafters.msadminusers.domain.Account;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
@Repository
public interface UserRepository extends JpaRepository<Account, Integer> {
    Optional<Account> findById(Integer id);
    Optional<Account> findByCedula(Integer cedula);
    Optional<Account> findByEmail(String email);

    Boolean existsBycedula(Integer cedula);

    Boolean existsByEmail(String email);
}
