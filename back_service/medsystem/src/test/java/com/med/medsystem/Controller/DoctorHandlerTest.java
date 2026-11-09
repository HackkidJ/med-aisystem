package com.med.medsystem.Controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.med.medsystem.MedsystemApplication;
import com.med.medsystem.Entity.Doctor;
import com.med.medsystem.Enum.Gender;


@SpringBootTest(classes=MedsystemApplication.class)
public class DoctorHandlerTest {
    @Autowired
    private DoctorHandler doctorHandler;
    @Test
    void testCreateDoctor() {
        String name = "hackkid";
        String identity = "537222199402042970";
        String phone = "1232132132";
        String gender = "男";
        Gender gen = Gender.valueOf(gender);
        Doctor doctor = new Doctor();
        doctor.setName(name);
        doctor.setIdentityId(identity);
        doctor.setPhone(phone);
        doctor.setGender(gen);

        this.doctorHandler.createDoctor(doctor);

    }

    @Test
    void testFindAll() {

    }

    @Test
    void testGetLastSixChars() {

    }

    @Test
    void testLoginDoctor() {

    }
}
