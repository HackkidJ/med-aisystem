package com.med.medsystem.Controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.med.medsystem.Entity.Account;
import com.med.medsystem.Entity.Doctor;
import com.med.medsystem.Repository.AccountRepository;
import com.med.medsystem.Repository.DoctorRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@Deprecated
@RestController
@RequestMapping("/medsystem/doctor/deprecated")
public class DoctorHandler {
    @Autowired
    private DoctorRepository doctorRepository;
    @Autowired
    private AccountRepository accountRepository;
    private PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    @GetMapping("/findAll")
    public List<Doctor> findAll() {
        return doctorRepository.findAll();
    }

    @PostMapping("/add")
    public ResponseEntity<Doctor> createDoctor(@RequestBody Doctor doctor) {
        String identity = doctor.getIdentityId();
        Account account = new Account();
        List<Doctor> doctors = doctorRepository.findAll();
        for(Doctor tempDoctor : doctors){
            if(tempDoctor.getIdentityId().equals(identity)){
                return new ResponseEntity<>(null,HttpStatus.CONFLICT);
            }
        }
        doctor.setId(null);
        //本系统不对医生身份做自主注册的功能 此处只保留建立医生对象的方法
        Doctor createDoctor = this.doctorRepository.save(doctor);
        String originPasswd = getLastSixChars(createDoctor.getIdentityId());
        String encodedPasswd = this.passwordEncoder.encode(originPasswd);
        account.setId(doctor.getId());
        account.setIdentityId(identity);
        account.setPhone(createDoctor.getPhone());
        account.setPasswd(encodedPasswd);
        this.accountRepository.save(account);
        return new ResponseEntity<>(createDoctor,HttpStatus.CREATED);
    }
    
    @PostMapping("/login")
    public ResponseEntity<Doctor> loginDoctor(@RequestBody Account account) {
        String identity = account.getIdentityId();
        String phone = account.getPhone();
        String originPasswd = account.getPasswd();
        List<Account> accounts = null;
        Account realAccount = null;
        
        //优先拿身份证号进行匹配 前端会把身份证号设为只读 不容易重复
        if(identity != null && realAccount == null) {
            accounts = this.accountRepository.findByIdentityId(identity);
            if(accounts.size() == 1){
                realAccount = accounts.get(0);
            }
            else{
                return new ResponseEntity<>(null,HttpStatus.CONFLICT);
            }
        }
        else if(phone != null && realAccount == null){
            accounts = this.accountRepository.findByPhone(phone);
            if(accounts.size() == 1){
                realAccount = accounts.get(0);
            }
            else{
                return new ResponseEntity<>(null,HttpStatus.CONFLICT);
            }
        }
        else{
            return new ResponseEntity<>(null,HttpStatus.CONFLICT);
        }
        String dbPasswd = realAccount.getPasswd();
        
        if(this.passwordEncoder.matches(originPasswd, dbPasswd)){
            Doctor doctor = this.doctorRepository.findById(realAccount.getId()).get();
            return new ResponseEntity<>(doctor,HttpStatus.OK);
        }
        else{
            return new ResponseEntity<>(null,HttpStatus.UNAUTHORIZED);
        }

        
    }
    

    //从身份证号中最后六位取出作初始密码
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
