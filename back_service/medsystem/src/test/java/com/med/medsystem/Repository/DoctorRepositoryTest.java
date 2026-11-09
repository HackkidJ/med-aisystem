package com.med.medsystem.Repository;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class DoctorRepositoryTest {
    @Autowired
    private DoctorRepository doctorRepository;

    @Test
    void findAll() {
        System.out.println(doctorRepository.findAll());
    }
}
