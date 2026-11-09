package com.med.medsystem.Repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import com.med.medsystem.Entity.Account;

public interface AccountRepository extends JpaRepository<Account,String>{
    public List<Account> findByPhone(String phone);
    public List<Account> findByIdentityId(String identityId);
}
