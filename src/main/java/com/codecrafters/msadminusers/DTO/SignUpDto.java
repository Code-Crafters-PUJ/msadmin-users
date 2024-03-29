package com.codecrafters.msadminusers.DTO;
import lombok.Data;

@Data
public class SignUpDto {
    private String name;
    private String last_name;
    private String email;
    private String password;
    private String cedula;
    private String role;
}
