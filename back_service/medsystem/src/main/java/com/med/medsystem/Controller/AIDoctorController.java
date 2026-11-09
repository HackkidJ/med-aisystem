package com.med.medsystem.Controller;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

import org.apache.catalina.connector.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.med.medsystem.Entity.AICallbackRequest;
import com.med.medsystem.Entity.AIConversationData;
import com.med.medsystem.Entity.AIMessageRequest;
import com.med.medsystem.Entity.AISessionRequest;
import com.med.medsystem.Entity.AISessionResponse;
import com.med.medsystem.Entity.DoctorInfo;
import com.med.medsystem.Service.AIDoctorService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.GetMapping;



@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "*")
public class AIDoctorController {
    private static final Logger logger = LoggerFactory.getLogger(AIDoctorController.class);
    @Autowired
    private AIDoctorService aiDoctorService;
      // 用于存储等待Python响应的请求
    private final Map<String, CompletableFuture<AISessionResponse>> pendingRequests = new ConcurrentHashMap<>();

    //vue发起调用的接口
    @PostMapping("/start-session")
    public CompletableFuture<ResponseEntity<Map<String,Object>>> startSession(@RequestBody AISessionRequest request) {
        logger.info("=== 收到start-session请求 ===");
        logger.info("请求数据: {}", request);
        logger.info("DoctorInfo: {}", request.getDoctorInfo());
        //TODO: process POST request
        String requestId = generateRequestId();
        try{
            CompletableFuture<AISessionResponse> future = new CompletableFuture<>();
            pendingRequests.put(requestId, future);
            aiDoctorService.startSession(request.getDoctorInfo(),requestId);

            return future.thenApply(response -> {
                Map<String,Object> result = new HashMap<>();
                result.put("success", response.getSuccess());
                result.put("message", response.getMessage());
                result.put("sessionId", response.getSessionId());
                result.put("data", response.getData());
                return ResponseEntity.ok(result);
            });
        }
        catch(Exception e){
            logger.error("处理开始会话回调请求失败", e);
            pendingRequests.remove(requestId);
            return CompletableFuture.completedFuture(
                ResponseEntity.internalServerError().body(createErrorResult("系统错误"+e.getMessage()))
            );
        }
    }

    @PostMapping("/session-callback")
    public ResponseEntity<Map<String,Object>> handleSessionCallback(@RequestBody AICallbackRequest callbackRequest) {
        logger.info("===收到python服务器回调===");
        logger.info("回调数据{}",callbackRequest);
        
        try{
            //构造响应data对象
            Map<String,Object> origin_data = callbackRequest.getData();
            AIConversationData data = new AIConversationData();
            data.setSessionId((String)origin_data.get("sessionId"));
            data.setMessageType((String)origin_data.get("type"));
            data.setContent((String)origin_data.get("content"));
            data.setTimestamp(callbackRequest.getTimestamp());
            if(data.getMessageType().equals("GREETING")){
                data.setConversationTurn(0);
            }
            else if (callbackRequest.getConversationTurn()!=null){
                data.setConversationTurn(callbackRequest.getConversationTurn());
            }
            else{
                data.setConversationTurn(null);
            }
        
            String requestId = callbackRequest.getRequestId();
            CompletableFuture<AISessionResponse> future = pendingRequests.get(requestId);
            if(future != null){
                AISessionResponse response = new AISessionResponse();
                response.setSuccess(true);
                response.setSessionId(callbackRequest.getSessionId());
                response.setMessage("会话创建成功");
                response.setData(data);

                future.complete(response);
                pendingRequests.remove(requestId);

                logger.info("回调处理完毕，请求id{}", requestId);
                return ResponseEntity.ok(Collections.singletonMap("success", true));
            }
            else{
                logger.warn("未找到对应等待请求，请求id：{}",requestId);
                return ResponseEntity.badRequest().body(Collections.singletonMap("success", false));
            }
        }
        catch(Exception e ){
            logger.error("处理请求会话回调时发生错误", e);
            return ResponseEntity.internalServerError().body(Collections.singletonMap("success", false));
        }
    }

    private String generateRequestId(){
        return "req_" + System.currentTimeMillis() + "_" +UUID.randomUUID().toString().substring(0,8);
    }
    
    @PostMapping(value = "/image-diagnosis",consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public CompletableFuture<ResponseEntity<Map<String,Object>>> imageDiagnosis(@RequestParam("image") MultipartFile imageFile,@RequestParam("doctorInfo") String doctorInfoJson) {
        logger.info("=== 收到医学影像诊断请求 ===");
        logger.info("文件名称: {}", imageFile.getOriginalFilename());
        logger.info("文件大小: {} bytes", imageFile.getSize());
        logger.info("文件类型: {}", imageFile.getContentType());
        ObjectMapper objectMapper = new ObjectMapper();
        String requestId = generateRequestId();
        try{
            if(imageFile.isEmpty()){
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(createErrorResult("请上传有效图片文件")));
            }
            String contentType = imageFile.getContentType();
            if(contentType == null || !contentType.startsWith("image/")){
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(createErrorResult("请上传图片文件")));
            }
            // 验证文件大小（限制为10MB）
            if (imageFile.getSize() > 10 * 1024 * 1024) {
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(createErrorResult("图片大小不能超过10mb")));
            }
            // 解析doctorInfo
            DoctorInfo doctorInfo;
            try {
                  doctorInfo = objectMapper.readValue(doctorInfoJson, DoctorInfo.class);
            } catch (Exception e) {
                logger.error("解析doctorInfo失败", e);
                return CompletableFuture.completedFuture(ResponseEntity.badRequest().body(createErrorResult("医生信息格式错误")));
            }
            CompletableFuture<AISessionResponse> future = new CompletableFuture<>();
            pendingRequests.put(requestId, future);
            aiDoctorService.processImageDiagnosis(imageFile,doctorInfo,requestId);
            return future.thenApply(response ->{
                Map<String, Object> result = new HashMap<>();
                result.put("success", response.getSuccess());
                result.put("message", response.getMessage());
                result.put("data", response.getData());
                return ResponseEntity.ok(result);
            });
        }
        catch(Exception e){
            logger.error("处理影像回调请求失败", e);
            pendingRequests.remove(requestId);
            return CompletableFuture.completedFuture(
                ResponseEntity.internalServerError().body(createErrorResult("医学影像转发失败：" + e.getMessage()))
            );
        }

    }

    @PostMapping("/image-diagnosis-callback")
public ResponseEntity<Map<String,Object>> handleImageDiagnosisCallback(@RequestBody AICallbackRequest callbackRequest) {
    logger.info("===收到python服务器图像诊断回调===");
    logger.info("回调数据: {}", callbackRequest);
    
    try{
        // 构造响应data对象
        Map<String,Object> origin_data = callbackRequest.getData();
        AIConversationData data = new AIConversationData();

        data.setMessageType("IMAGE_DIAGNOSIS"); // 设置消息类型为图像诊断
        data.setContent((String)origin_data.get("content"));
        data.setTimestamp(callbackRequest.getTimestamp());
        data.setConversationTurn(0); // 图像诊断没有对话轮次，设为0
        
        String requestId = callbackRequest.getRequestId();
        CompletableFuture<AISessionResponse> future = pendingRequests.get(requestId);
        if(future != null){
            AISessionResponse response = new AISessionResponse();
            response.setSuccess(true);
            response.setMessage("图像诊断完成");
            response.setData(data);

            future.complete(response);
            pendingRequests.remove(requestId);

            logger.info("图像诊断回调处理完毕，请求id: {}", requestId);
            return ResponseEntity.ok(Collections.singletonMap("success", true));
        }
        else{
            logger.warn("未找到对应等待请求，请求id：{}", requestId);
            return ResponseEntity.badRequest().body(Collections.singletonMap("success", false));
        }
    }
    catch(Exception e){
        logger.error("处理图像诊断回调时发生错误", e);
        return ResponseEntity.internalServerError().body(Collections.singletonMap("success", false));
    }
}
    

    @PostMapping("/send-message")
    public CompletableFuture<ResponseEntity<Map<String,Object>>> sendMessage(@RequestBody AIMessageRequest request) {
        try{
            CompletableFuture<AISessionResponse> future = new CompletableFuture<>();
            String requestId = generateRequestId();
            pendingRequests.put(requestId, future);
            aiDoctorService.sendMessage(request.getSessionId(), request.getUserInput(), request.getDoctorInfo(),requestId);
            
            return future.thenApply(response -> {
                Map<String,Object>result = new HashMap<>();
                result.put("success", response.getSuccess());
                result.put("sessionId", response.getSessionId());
                result.put("message", response.getMessage());
                result.put("data", response.getData());
                return ResponseEntity.ok(result);
            });
        }
        catch(Exception e){
            return CompletableFuture.completedFuture(
                ResponseEntity.internalServerError().body(createErrorResult("发送消息失败：" + e.getMessage()))
            );
        }
    }

    @PostMapping("/message-callback")
    public ResponseEntity<Map<String,Object>> handleMessageCallback(@RequestBody AICallbackRequest callbackRequest) {
        logger.info("===收到python服务器消息回调===");
        logger.info("回调数据{}",callbackRequest);
        
        try{
            AIConversationData data = new AIConversationData();
            data.setSessionId(callbackRequest.getSessionId());
            data.setContent(callbackRequest.getContent());
            data.setMessageType(callbackRequest.getMessageType());
            data.setTimestamp(callbackRequest.getTimestamp());
            data.setConversationTurn(callbackRequest.getConversationTurn());
            
            String requestId = callbackRequest.getRequestId();
            CompletableFuture<AISessionResponse> future = pendingRequests.get(requestId);
            if(future != null){
                AISessionResponse response = new AISessionResponse();
                response.setSuccess(true);
                response.setSessionId(data.getSessionId());
                response.setMessage("返回消息成功");
                response.setData(data);
                future.complete(response);
                pendingRequests.remove(requestId);

                logger.info("回调消息处理完毕，请求id{}", requestId);
                return ResponseEntity.ok(Collections.singletonMap("success",true));
            }
            else{
                logger.warn("未找到对应回调等待请求，请求id：{}",requestId);
                return ResponseEntity.badRequest().body(Collections.singletonMap("success", false));
            }
        }
        catch(Exception e ){
            logger.error("处理ai消息回调时发生错误", e);
            return ResponseEntity.internalServerError().body(Collections.singletonMap("success", false));
        }
    }
    
    
    @PostMapping("/end-session")
    public ResponseEntity<Map<String,Object>> endSession(@RequestBody String sessionId,
    @RequestParam(defaultValue = "USER_REQUEST") String reason) {
        //TODO: process POST request
        try{
            AISessionResponse response = aiDoctorService.endSession(sessionId, reason);
            Map<String,Object> result = new HashMap<>();
            result.put("success", response.getSuccess());
            result.put("message", response.getMessage());
            return ResponseEntity.ok(result);
        }
        catch(Exception e){
            return ResponseEntity.internalServerError().body(
                createErrorResult("结束会话失败："+e.getMessage())
            );
        }
    }
    
    @GetMapping("/health")
    public ResponseEntity<Map<String,Object>> healthCheck() {
        boolean isHealthy = aiDoctorService.healthCheck();
        Map<String,Object> result = new HashMap<>();
        result.put("status", isHealthy ? "healthy":"unhealthy");
        result.put("pythonServerAvailable", isHealthy);
        result.put("timestamp", System.currentTimeMillis());
        return ResponseEntity.ok(result);
    }

    private Map<String,Object> createErrorResult(String message){
        Map<String,Object> result = new HashMap<>();
        result.put("success", false);
        result.put("message", message);
        return result;
    }
    
    
}
