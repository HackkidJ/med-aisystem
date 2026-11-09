package com.med.medsystem.Controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.med.medsystem.Entity.Account;
import com.med.medsystem.Entity.Doctor;
import com.med.medsystem.Repository.AccountRepository;
import com.med.medsystem.Repository.DoctorRepository;
import com.med.medsystem.Util.JwtTokenUtil;

@RestController
@RequestMapping("/medsystem/doctor")
public class AuthenController {
    
    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    @Autowired
    private AccountRepository accountRepository;
    
    @Autowired
    private DoctorRepository doctorRepository;
    
    private PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    /**
     * 替换原来的登录方法，使用JWT认证
     */
    @PostMapping("/login")
    public ResponseEntity<?> loginDoctor(@RequestBody Account account) {
        try {
            String identity = account.getIdentityId();
            String phone = account.getPhone();
            String originPasswd = account.getPasswd();
            
            List<Account> accounts = null;
            Account realAccount = null;
            
            // 优先拿身份证号进行匹配
            if (identity != null && !identity.trim().isEmpty()) {
                accounts = accountRepository.findByIdentityId(identity);
                if (accounts != null && accounts.size() == 1) {
                    realAccount = accounts.get(0);
                } else if (accounts != null && accounts.size() > 1) {
                    Map<String, String> errorResponse = new HashMap<>();
                    errorResponse.put("error", "找到多个用户，请联系管理员");
                    return new ResponseEntity<>(errorResponse, HttpStatus.CONFLICT);
                }
            }
            
            // 如果身份证号没找到，尝试手机号
            if (realAccount == null && phone != null && !phone.trim().isEmpty()) {
                accounts = accountRepository.findByPhone(phone);
                if (accounts != null && accounts.size() == 1) {
                    realAccount = accounts.get(0);
                } else if (accounts != null && accounts.size() > 1) {
                    Map<String, String> errorResponse = new HashMap<>();
                    errorResponse.put("error", "找到多个用户，请联系管理员");
                    return new ResponseEntity<>(errorResponse, HttpStatus.CONFLICT);
                }
            }
            
            if (realAccount == null) {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("error", "用户不存在");
                return new ResponseEntity<>(errorResponse, HttpStatus.UNAUTHORIZED);
            }
            
            // 验证密码
            String dbPasswd = realAccount.getPasswd();
            if (!passwordEncoder.matches(originPasswd, dbPasswd)) {
                Map<String, String> errorResponse = new HashMap<>();
                errorResponse.put("error", "密码错误");
                return new ResponseEntity<>(errorResponse, HttpStatus.UNAUTHORIZED);
            }
            
            // 生成JWT token
            CustomUserDetails userDetails = new CustomUserDetails(realAccount);
            final String token = jwtTokenUtil.generateToken(userDetails);
            
            // 获取医生信息
            Doctor doctor = doctorRepository.findById(realAccount.getId()).orElse(null);
            
            // 返回结果，包含JWT token和原有数据
            Map<String, Object> response = new HashMap<>();
            response.put("token", token); // 新增：JWT token
            response.put("doctor", doctor); // 保持原有返回数据
            response.put("identityId", realAccount.getIdentityId());
            response.put("phone", realAccount.getPhone());
            response.put("id", realAccount.getId());
            
            return new ResponseEntity<>(response, HttpStatus.OK);
            
        } catch (BadCredentialsException e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("error", "认证失败");
            return new ResponseEntity<>(errorResponse, HttpStatus.UNAUTHORIZED);
        } catch (Exception e) {
            Map<String, String> errorResponse = new HashMap<>();
            errorResponse.put("error", "登录失败: " + e.getMessage());
            return new ResponseEntity<>(errorResponse, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
    /**
     * 保留原有的添加医生功能（需要JWT认证）
     */
    @PostMapping("/add")
    public ResponseEntity<Doctor> createDoctor(@RequestBody Doctor doctor) {
        try {
            String identity = doctor.getIdentityId();
            Account account = new Account();
            List<Doctor> doctors = doctorRepository.findAll();
            
            // 检查身份证号是否重复 - 保持原有逻辑
            for(Doctor tempDoctor : doctors){
                if(tempDoctor.getIdentityId().equals(identity)){
                    return new ResponseEntity<>(null, HttpStatus.CONFLICT);
                }
            }
            
            doctor.setId(null);
            Doctor createDoctor = doctorRepository.save(doctor);
            
            // 设置初始密码 - 保持原有逻辑
            String originPasswd = getLastSixChars(createDoctor.getIdentityId());
            String encodedPasswd = passwordEncoder.encode(originPasswd);
            
            account.setId(doctor.getId());
            account.setIdentityId(identity);
            account.setPhone(createDoctor.getPhone());
            account.setPasswd(encodedPasswd);
            accountRepository.save(account);
            
            return new ResponseEntity<>(createDoctor, HttpStatus.CREATED);
            
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
    /**
     * 保留原有的查询所有医生功能（需要JWT认证）
     */
    @GetMapping("/findAll")
    public ResponseEntity<List<Doctor>> findAll() {
        try {
            List<Doctor> doctors = doctorRepository.findAll();
            return new ResponseEntity<>(doctors, HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(null, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
    // 自定义UserDetails实现
    public static class CustomUserDetails implements org.springframework.security.core.userdetails.UserDetails {
        private final Account account;
        
        public CustomUserDetails(Account account) {
            this.account = account;
        }
        
        @Override
        public String getUsername() {
            return account.getIdentityId();
        }
        
        @Override
        public String getPassword() {
            return account.getPasswd();
        }
        
        @Override
        public boolean isAccountNonExpired() { return true; }
        
        @Override
        public boolean isAccountNonLocked() { return true; }
        
        @Override
        public boolean isCredentialsNonExpired() { return true; }
        
        @Override
        public boolean isEnabled() { return true; }
        
        @Override
        public java.util.Collection<org.springframework.security.core.authority.SimpleGrantedAuthority> getAuthorities() {
            return java.util.Collections.emptyList();
        }
        
        public Account getAccount() {
            return account;
        }
    }
    
    // 从身份证号中最后六位取出作初始密码 - 保持原有逻辑
    public static String getLastSixChars(String str) {
        if (str == null) {
            return null;
        }
        if (str.length() <= 6) {
            return str;
        }
        return str.substring(str.length() - 6);
    }
}