package com.codecrafters.msadminusers.domain;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "credenciales", schema = "usermicroservice",uniqueConstraints = {
        @UniqueConstraint(columnNames = {"email"})
})
public class Credentials {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;
    private String email;
    private String password;


    @OneToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @JoinColumn(name = "idcuenta")
    private Account account;


}
