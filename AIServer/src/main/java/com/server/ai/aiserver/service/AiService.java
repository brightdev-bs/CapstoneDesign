package com.server.ai.aiserver.service;

import com.server.ai.aiserver.web.dto.DetectionRequestDto;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

import java.io.File;
import java.io.IOException;

public class AiService {
    public void localSave(MultipartFile image) throws IOException {
        String filePath="C:/arcface 경로";
        String fileName = image.getOriginalFilename();
        long fileSize = (long)image.getBytes().length;

        System.out.println("파일 이름 : "+fileName);
        System.out.println("파일 크기 : "+fileSize);

        try{
            image.transferTo(new File(filePath + fileName));
        } catch (IOException e) {
            System.out.println("사용자 이미지 저장 실패.");
            e.printStackTrace();
        }
        System.out.println("사용자 이미지 저장 성공.");

    }

    public void run(){
        //cmd
    }
}
