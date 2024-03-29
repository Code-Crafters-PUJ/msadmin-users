package com.codecrafters.msadminusers.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "operacion", schema = "usermicroservice")
public class Operation {
}
