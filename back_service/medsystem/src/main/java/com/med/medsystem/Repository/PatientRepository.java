package com.med.medsystem.Repository;



import org.springframework.data.jpa.repository.JpaRepository;

import com.med.medsystem.Entity.Patient;
import java.util.List;



public interface PatientRepository extends JpaRepository <Patient,String>{
    public Patient findByIdentityId(String identityId);
    public List<Patient> findByName(String name);
}
