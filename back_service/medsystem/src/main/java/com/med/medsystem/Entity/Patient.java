package com.med.medsystem.Entity;

import java.util.Date;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
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
@Table(name = "patients")
@JsonIgnoreProperties(ignoreUnknown = true)
public class Patient {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    @Column(name = "identity_id")
    private String identityId;
    private String name;
    @Enumerated(EnumType.STRING)
    private Gender gender;
    private String phone;
    private String address;
    private String PMH;
    private String PI;
    private String CC;
    @Column(name = "update_time")
    private Date updateTime;
    private String doc_id;
}
