package com.med.medsystem.Entity;

import org.springframework.web.multipart.MultipartFile;

import lombok.Data;

@Data
public class ImageDiagnosisRequest {
    private MultipartFile image;
    private DoctorInfo doctorInfo;
}
