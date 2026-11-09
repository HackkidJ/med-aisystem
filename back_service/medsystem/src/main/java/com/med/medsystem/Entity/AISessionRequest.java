package com.med.medsystem.Entity;

public class AISessionRequest {
    private DoctorInfo doctorInfo;
    public AISessionRequest(){}

    public AISessionRequest(DoctorInfo doctorInfo){
        this.doctorInfo = doctorInfo;
    }

    public DoctorInfo getDoctorInfo(){
        return this.doctorInfo;
    }

    public void setDoctorInfo(DoctorInfo doctorInfo){
        this.doctorInfo = doctorInfo;
    }
}
