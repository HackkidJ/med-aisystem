package com.med.medsystem.Entity;

import com.med.medsystem.Enum.Level;

import java.sql.Blob;

import com.med.medsystem.Enum.Department;
import com.med.medsystem.Enum.Gender;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;


@Entity
@Data
@Table(name = "doctors")
public class Doctor {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    @Column(name = "identity_id")
    private String identityId;
    private String name;
    @Enumerated(EnumType.STRING)
    private Gender gender;
    private String phone;
    private String mail;
    private String address;
    @Enumerated(EnumType.STRING)
    private Department department;
    @Enumerated(EnumType.STRING)
    private Level level;
    private Blob picture;
}
