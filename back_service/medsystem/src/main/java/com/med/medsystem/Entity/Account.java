package com.med.medsystem.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Entity
@Data
@Table(name = "account")
public class Account {
    @Id
    private String id;
    @Column(name = "identity_id")
    private String identityId;
    private String phone;
    private String passwd;
}
