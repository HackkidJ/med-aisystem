package com.med.medsystem.Entity;

public class AIMessageRequest {
    public AIMessageRequest(String sessionId, String userInput, DoctorInfo doctorInfo, String requestId) {
        this.sessionId = sessionId;
        this.userInput = userInput;
        this.doctorInfo = doctorInfo;
        this.requestId = requestId;
    }

    private String requestId;
    private String sessionId;
    private String userInput;
    private DoctorInfo doctorInfo;

    public AIMessageRequest(){}

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public DoctorInfo getDoctorInfo() {
        return doctorInfo;
    }

    public void setDoctorInfo(DoctorInfo doctorInfo) {
        this.doctorInfo = doctorInfo;
    }

    public String getUserInput() {
        return userInput;
    }

    public void setUserInput(String userInput) {
        this.userInput = userInput;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }
}
