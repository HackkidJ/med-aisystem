package com.med.medsystem.Controller;

import java.util.Date;
import java.util.List;
import java.util.Map;

import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.med.medsystem.Entity.Logger;
import com.med.medsystem.Entity.Patient;
import com.med.medsystem.Enum.Gender;
import com.med.medsystem.Repository.LoggerRepository;
import com.med.medsystem.Repository.PatientRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;



@RestController
@RequestMapping("/medsystem/patient")
public class PatientController {

    @Autowired
    private PatientRepository patientRepository;
    @Autowired
    private LoggerRepository loggerRepository;

    @GetMapping("/findById")
    public Patient findById(@RequestParam String id) {
        return this.patientRepository.findByIdentityId(id);
    }

    @GetMapping("/getPatientById")
    public Patient findByIdentityId(@RequestParam("identityId") String identityId) {
        return this.patientRepository.findByIdentityId(identityId);
    }

    @GetMapping("/getPatientByName")
    public List<Patient> getMethodName(@RequestParam("name") String name) {
        return this.patientRepository.findByName(name);
    }
    
    @PatchMapping("/updatePatient")
    public ResponseEntity<Patient> updatePatient(@RequestBody Map<String, Object> request) {
        System.out.println("成功收到修改患者信息patch请求");
        
        boolean isAI = (Boolean) request.get("isAI");
        Map<String, Object> patientData = (Map<String, Object>) request.get("patient_data");
        
        // 检查患者是否存在
        String identityId = (String) patientData.get("identityId");
        Patient existingPatient = this.patientRepository.findByIdentityId(identityId);
        if (existingPatient == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        // 只更新传入的非空字段
        if (patientData.containsKey("name")) {
            String name = (String) patientData.get("name");
            if (name != null && !name.isEmpty()) {
                existingPatient.setName(name);
            }
        }
        
        if (patientData.containsKey("gender")) {
            String genderStr = (String) patientData.get("gender");
            if (genderStr != null && !genderStr.isEmpty()) {
                try {
                    existingPatient.setGender(Gender.valueOf(genderStr));
                } catch (IllegalArgumentException e) {
                    return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
                }
            }
        }
        
        if (patientData.containsKey("phone")) {
            existingPatient.setPhone((String) patientData.get("phone"));
        }
        
        if (patientData.containsKey("address")) {
            existingPatient.setAddress((String) patientData.get("address"));
        }
        
        if (patientData.containsKey("PMH")) {
            existingPatient.setPMH((String) patientData.get("PMH"));
        }
        
        if (patientData.containsKey("PI")) {
            existingPatient.setPI((String) patientData.get("PI"));
        }
        
        if (patientData.containsKey("CC")) {
            existingPatient.setCC((String) patientData.get("CC"));
        }
        
        if (patientData.containsKey("doc_id")) {
            String docId = (String) patientData.get("doc_id");
            if (docId != null && !docId.isEmpty()) {
                existingPatient.setDoc_id(docId);
            }
        }
        
        existingPatient.setUpdateTime(new Date(System.currentTimeMillis()));
        Patient savedPatient = this.patientRepository.save(existingPatient);
        
        // 记录日志
        Logger logger = new Logger();
        logger.setAI(isAI);
        logger.setContent("修改了patients表中的患者信息\n"
            + "Id: " + savedPatient.getId() + "\n"
            + "Identity: " + savedPatient.getIdentityId() + "\n"
            + "name: " + savedPatient.getName() + "\n"
            + "gender: " + savedPatient.getGender() + "\n"
            + "phone: " + savedPatient.getPhone() + "\n"
            + "address: " + savedPatient.getAddress() + "\n"
            + "PMH: " + savedPatient.getPMH() + "\n"
            + "PI: " + savedPatient.getPI() + "\n"
            + "CC: " + savedPatient.getCC() + "\n"
            + "updateTime: " + savedPatient.getUpdateTime() + "\n"
            + "doc_id: " + savedPatient.getDoc_id() + "\n"
        );
        logger.setExecuteTime(new Date(System.currentTimeMillis()));
        logger.setId(null);
        logger.setUserId(savedPatient.getDoc_id());
        this.loggerRepository.save(logger);
        
        return new ResponseEntity<>(savedPatient, HttpStatus.OK);
    }

    
    @PostMapping("/addPatient")
    public ResponseEntity<Patient> addPatient(@RequestBody Map<String,Object> request) {
        System.out.println("成功收到录入post请求");
        boolean isAI = (Boolean) request.get("isAI");
        ObjectMapper mapper = new ObjectMapper();
        Patient patient = mapper.convertValue(request.get("patient_data"),Patient.class);
        patient.setUpdateTime(new Date(System.currentTimeMillis()));
        patient.setId(null);
        Patient createPatient = this.patientRepository.save(patient);
        Logger logger = new Logger();
        logger.setAI(isAI);
        logger.setContent("向patients表添加了patient\n"
        +"Id:"+patient.getId()+"\n"
        +"Identity:"+patient.getIdentityId()+"\n"
        +"name:"+patient.getName()+"\n"
        +"gender:"+patient.getGender()+"\n"
        +"phone:"+patient.getPhone()+"\n"
        +"address"+patient.getAddress()+"\n"
        +"PMH:"+patient.getPMH()+"\n"
        +"PI:"+patient.getPI()+"\n"
        +"CC:"+patient.getCC()+"\n"
        +"updateTime:"+patient.getUpdateTime()+"\n"
        +"doc_id:"+patient.getDoc_id()+"\n"
        );
        logger.setExecuteTime(new Date(System.currentTimeMillis()));
        logger.setId(null);
        logger.setUserId(patient.getDoc_id());
        this.loggerRepository.save(logger);
        return new ResponseEntity<>(createPatient,HttpStatus.CREATED);
    }
    
}
