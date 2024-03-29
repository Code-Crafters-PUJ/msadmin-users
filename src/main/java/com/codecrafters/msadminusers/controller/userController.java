package com.codecrafters.msadminusers.controller;

import com.codecrafters.msadminusers.domain.Account;
import com.codecrafters.msadminusers.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/user")
public class userController {

        @Autowired
        private UserService userService;

        @GetMapping("/{id}")
        public ResponseEntity<Account> getAccountforId(@PathVariable Integer id) {
            return ResponseEntity.ok(userService.getUserId(id));
        }
        @DeleteMapping("/{id}")
        public ResponseEntity<Void> deleteAccount(@PathVariable Integer id) {
                userService.deleteById(id);
                return ResponseEntity.noContent().build();
        }

        @PutMapping("/{id}")
        public ResponseEntity<Account> updateAccount(@PathVariable Integer id, @RequestBody Account account) {
                Account user = userService.getUserId(id);
                user.setName(account.getName());
                user.setLast_name(account.getLast_name());
                user.setEmail(account.getEmail());
                return ResponseEntity.ok(userService.save(user));
        }


}
