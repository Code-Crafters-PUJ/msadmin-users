package com.codecrafters.msadminusers.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.GenericGenerator;

@Getter
@Setter
@Entity
@Table(name = "permisos", schema = "usermicroservice")
public class Permissions {
    @Id
    @GeneratedValue(generator = "uuid")
    @GenericGenerator(name = "uuid", strategy = "uuid2")
    private Integer idpermisos;

    private Integer idmodulo;
    private Integer idcuenta;
    private Integer idtipo_permiso;
}
