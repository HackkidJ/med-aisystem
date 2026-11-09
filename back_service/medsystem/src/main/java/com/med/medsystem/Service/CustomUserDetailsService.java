package com.med.medsystem.Service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.med.medsystem.Controller.AuthenController;
import com.med.medsystem.Entity.Account;
import com.med.medsystem.Repository.AccountRepository;

@Service
public class CustomUserDetailsService implements UserDetailsService {
    
    @Autowired
    private AccountRepository accountRepository;
    
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // 这里假设username可能是身份证号或手机号
        List<Account> accounts = accountRepository.findByIdentityId(username);
        if (accounts == null || accounts.isEmpty()) {
            accounts = accountRepository.findByPhone(username);
        }
        
        if (accounts == null || accounts.isEmpty()) {
            throw new UsernameNotFoundException("用户不存在: " + username);
        }
        
        if (accounts.size() > 1) {
            throw new UsernameNotFoundException("找到多个用户: " + username);
        }
        
        Account account = accounts.get(0);
        return new AuthenController.CustomUserDetails(account);
    }
}