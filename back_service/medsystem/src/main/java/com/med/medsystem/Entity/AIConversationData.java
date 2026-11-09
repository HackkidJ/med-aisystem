package com.med.medsystem.Entity;

public class AIConversationData {
    private String sessionId;
    private String messageType;
    private String content;
    private String timestamp;
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
}
