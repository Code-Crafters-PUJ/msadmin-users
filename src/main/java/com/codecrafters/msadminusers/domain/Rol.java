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
@Table(name = "rol", schema = "usermicroservice")
public class Rol {
    @Id
    @GeneratedValue(generator = "uuid")
    @GenericGenerator(name = "uuid", strategy = "uuid2")
    private Integer idrol;

    private String description;
}
