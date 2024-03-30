package com.codecrafters.msadminusers.repository;

import com.codecrafters.msadminusers.domain.Rol;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Set;

@Repository
public interface RoleRepository extends JpaRepository<Rol, Long> {
    Rol findByName(String name);
    Set<Rol> findAllByName(String name);
}
