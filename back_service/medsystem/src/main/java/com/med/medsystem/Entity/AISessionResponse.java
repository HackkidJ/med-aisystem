package com.med.medsystem.Entity;

public class AISessionResponse {
    private Boolean success;
    public Boolean getSuccess() {
        return success;
    }

    public void setSuccess(Boolean success) {
        this.success = success;
    }

    private String sessionId;
    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    private String message;
    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    private AIConversationData data;

    public AIConversationData getData() {
        return data;
    }

    public void setData(AIConversationData data) {
        this.data = data;
    }

    public AISessionResponse(){}
}
