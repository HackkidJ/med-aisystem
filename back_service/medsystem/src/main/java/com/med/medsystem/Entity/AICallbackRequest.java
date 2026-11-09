package com.med.medsystem.Entity;

import java.util.Map;

public class AICallbackRequest {
    public AICallbackRequest() {
    }

    private String requestId;
    private String sessionId;
    private String messageType;
    private String content;
    private String timestamp;
    private Map<String,Object> data;
    private Integer conversationTurn;

    public Integer getConversationTurn() {
        return conversationTurn;
    }

    public void setConversationTurn(Integer conversationTurn) {
        this.conversationTurn = conversationTurn;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public Map<String, Object> getData() {
        return data;
    }

    public void setData(Map<String, Object> data) {
        this.data = data;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getMessageType() {
        return messageType;
    }

    public void setMessageType(String messageType) {
        this.messageType = messageType;
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }
}
