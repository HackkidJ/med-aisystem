package com.med.medsystem.Repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.med.medsystem.Entity.Logger;

public interface LoggerRepository extends JpaRepository<Logger,String>{
    
}
