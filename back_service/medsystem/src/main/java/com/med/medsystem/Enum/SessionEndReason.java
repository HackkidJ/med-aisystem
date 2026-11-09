package com.med.medsystem.Enum;

public enum SessionEndReason {
    USER_REQUEST("USER_REQUEST"),
    SESSION_TIMEOUT("SESSION_TIMEOUT"),
    SYSTEM_ERROR("SYSTEM_ERROR"),
    CONVERSATION_COMPLETE("CONVERSATION_COMPLETE");

    private final String value;

    SessionEndReason(String value){
        this.value = value;
    }

    public String getValue(){
        return this.value;
    }
}
