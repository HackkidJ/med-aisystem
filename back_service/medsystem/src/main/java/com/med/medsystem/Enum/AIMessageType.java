package com.med.medsystem.Enum;

public enum AIMessageType {
    GREETING("GREETING"),
    AI_RESPONSE("AI_RESPONSE"),
    ERROR("ERROR"),
    SESSION_END("SESSION_END");

    private final String value;

    AIMessageType(String value){
        this.value = value;
    }

    public String getValue(){
        return value;
    }
}
