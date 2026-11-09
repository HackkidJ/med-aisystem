package com.med.medsystem.Entity;

import java.util.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Table;
import lombok.Data;

@Entity
@Data
@Table(name = "logger")
public class Logger {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    @Column(name = "execute_time")
    private Date executeTime;
    private String content;
    @Column(name = "user_id")
    private String userId;
    @Column(name = "is_AI")
    private boolean isAI;
}
