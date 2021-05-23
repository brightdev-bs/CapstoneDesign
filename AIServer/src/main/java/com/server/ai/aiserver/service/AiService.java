package com.server.ai.aiserver.service;

import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

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

    public void run(String clientIp){
        System.out.println("얼굴 매칭....");

        //cmd
        try{
//            cmd("bin 생성 && 얼굴 인식");
            cmd("cd C:\\Users\\admin\\Desktop && mkdir test");

        }catch(Throwable t){
            t.printStackTrace();
        }

        System.out.println("결과 전송 완료.");
        System.out.println("종료.");


    }
    public void cmd(String command) throws IOException {
        String cmd[] = new String[3];
        cmd[0] ="cmd.exe";
        // 명령어 모두 실해 후 종료 옵션.
        cmd[1] = "/C";
        cmd[2] = command;

        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);


        BufferedReader br = new BufferedReader(
                new InputStreamReader(
                        process.getInputStream()));
        String line;
        while((line =br.readLine()) !=null)
            System.out.println(line);
    }

    public static void main(String[] args) {
        AiService aiService = new AiService();
        aiService.run();
    }
}
