package com.codecrafters.msadminusers;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
public class MsadminUsersApplication {

	public static void main(String[] args) {
		SpringApplication.run(MsadminUsersApplication.class, args);
	}

}
