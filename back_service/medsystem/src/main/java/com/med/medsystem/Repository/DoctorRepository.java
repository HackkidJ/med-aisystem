package com.med.medsystem.Repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.med.medsystem.Entity.Doctor;

public interface DoctorRepository extends JpaRepository<Doctor,String>{

    
}
