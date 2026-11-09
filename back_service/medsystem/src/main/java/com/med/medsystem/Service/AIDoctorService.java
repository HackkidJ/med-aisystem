package com.med.medsystem.Service;

import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.http.*;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.med.medsystem.Entity.AIMessageRequest;
import com.med.medsystem.Entity.AISessionResponse;
import com.med.medsystem.Entity.DoctorInfo;
import com.med.medsystem.config.PythonServerProperties;

@Service
public class AIDoctorService {
    
    private static final Logger logger = LoggerFactory.getLogger(AIDoctorService.class);
    @Autowired
    private final RestTemplate restTemplate;
    @Autowired
    private final PythonServerProperties pythonServerProperties;
    @Autowired
    private ObjectMapper objectMapper;

    private final String selfUrl = "http://localhost:8081";

public void processImageDiagnosis(MultipartFile imageFile, DoctorInfo doctorInfo, String requestId) {
    try{
        String url = pythonServerProperties.getBaseUrl() + "/image-diagnosis";
        
        // 将图片转换为base64
        String base64Image = Base64.getEncoder().encodeToString(imageFile.getBytes());
        
        Map<String, Object> request = new HashMap<>();
        request.put("doctorInfo", doctorInfo);
        request.put("requestId", requestId);
        request.put("imageData", base64Image);
        request.put("imageName", imageFile.getOriginalFilename());
        request.put("contentType", imageFile.getContentType());
        request.put("callbackUrl", selfUrl + "/api/ai/image-diagnosis-callback"); // 添加回调URL
        
        new Thread(() -> {
            try{
                ResponseEntity<Map> response = restTemplate.postForEntity(
                    url, createHttpEntity(request), Map.class
                );
                if(response.getStatusCode() != HttpStatus.OK){
                    logger.error("调用Python图像诊断服务失败: {}", response.getStatusCode());
                }
            }
            catch(Exception e){
                logger.error("调用Python图像诊断服务时发生错误", e);
            }
        }).start();
        
    } catch(Exception e){
        logger.error("处理医学影像诊断时发生错误", e);
        throw new RuntimeException("医学影像诊断处理失败", e);
    }
}
    

    public AIDoctorService(RestTemplate pythonRestTemplate,PythonServerProperties properties){
        this.restTemplate = pythonRestTemplate;
        this.pythonServerProperties = properties;
    }

    public void startSession(DoctorInfo doctorInfo,String requestId){
        try{
            String url = pythonServerProperties.getBaseUrl()+"/start-session";
            Map<String,Object> request = new HashMap<>();
            request.put("doctorInfo", doctorInfo);
            request.put("requestId", requestId);
            request.put("callbackUrl", selfUrl+"/api/ai/session-callback");
            
            new Thread(() -> {
                try{
                    ResponseEntity<Map> response = restTemplate.postForEntity(
                        url, createHttpEntity(request), Map.class
                        );
                    if(response.getStatusCode() != HttpStatus.OK){
                        logger.error("调用Python服务失败{}", response.getStatusCode());
                    }
                }
                catch(Exception e ){
                    logger.error("调用Python服务时发生错误", e);
                }
            }).start();
        }
        catch(Exception e){
            logger.error("启动AI会话失败", e);
            throw new RuntimeException("启动AI会话失败",e);
        }
    }

    public AISessionResponse sendMessage(String sessionId,String userInput,DoctorInfo doctorInfo,String requestId){
        try{
            String url = pythonServerProperties.getBaseUrl()+"/process-message";

            AIMessageRequest request = new AIMessageRequest(sessionId,userInput,doctorInfo,requestId);
            ResponseEntity<AISessionResponse> response = restTemplate.postForEntity(
                url, createHttpEntity(request), AISessionResponse.class
            );
            if(response.getStatusCode() == HttpStatus.OK && response.getBody()!=null){
                logger.info("AI消息处理成功，会话id{}",sessionId);
                return response.getBody();
            }else{
                logger.error("AI消息处理失败，会话id{},状态码{}", sessionId,response.getStatusCode());
                return createErrorResponse("AI消息处理失败");
            }
            
        }

        catch(Exception e){
            logger.error("调用Python服务器处理时发生错误，会话id{}", sessionId, e);
            return createErrorResponse("服务暂时不可用"+e.getMessage());
        }
    }

    public AISessionResponse endSession(String sessionId,String reason){
        try{
            String url = pythonServerProperties.getBaseUrl()+"/end-session";
            Map<String,String> request = new HashMap<>();
            request.put("sessionId", sessionId);
            request.put("reason", reason);

            ResponseEntity<AISessionResponse> response = restTemplate.postForEntity(
                url, createHttpEntity(request), AISessionResponse.class
            );

            if(response.getStatusCode()==HttpStatus.OK && response.getBody() != null){
                logger.info("AI会话结束成功，会话id{}，原因{}",sessionId,reason);
                return response.getBody();
            }
            else{
                logger.error("AI会话结束失败，会话id{}，状态码{}",sessionId,response.getStatusCode());
                return createErrorResponse("AI会话结束失败");
            }
        }

        catch(Exception e){
            logger.error("调用Python服务器结束会话时发生错误,会话id{}", sessionId, e);
            return createErrorResponse("结束AI会话失败"+e.getMessage());
        }
    }

    public boolean healthCheck(){
        try{
            String url = pythonServerProperties.getBaseUrl()+"/health";
            ResponseEntity<Map> response = restTemplate.getForEntity(
                url, Map.class);
                return response.getStatusCode() == HttpStatus.OK;
        }
        catch(Exception e){
            logger.warn("python服务器健康检查失败", e);
        }
        return false;
    }

    private HttpEntity<Object> createHttpEntity(Object body){
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        return new HttpEntity<>(body,headers);
    }

    private AISessionResponse createErrorResponse(String message){
        AISessionResponse response = new AISessionResponse();
        response.setSuccess(false);
        response.setMessage(message);
        return response;
    }
}
