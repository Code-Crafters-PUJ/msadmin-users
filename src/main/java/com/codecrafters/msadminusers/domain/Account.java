package com.codecrafters.msadminusers.domain;

import jakarta.persistence.*;
import lombok.*;

import java.util.Date;
import java.util.Set;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "cuenta", schema = "usermicroservice", uniqueConstraints = {
        @UniqueConstraint(columnNames = {"cedula"})}


)
public class Account {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long idcuenta;
    private String firstName;
    private String last_name;
    @Column(unique = true)
    private String cedula;
    @Column(unique = true)
    private String email;
    private String password;
    private Date last_access_date;

    @ManyToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @JoinTable(name = "user_roles",
            joinColumns = @JoinColumn(name = "user_id", referencedColumnName = "idcuenta"),
            inverseJoinColumns = @JoinColumn(name = "role_id", referencedColumnName = "idrol"))
    private Set<Rol> roles;
}
