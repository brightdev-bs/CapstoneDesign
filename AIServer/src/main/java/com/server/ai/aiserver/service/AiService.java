package com.server.ai.aiserver.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

@Service
public class AiService {
    public void localSave(MultipartFile image, String sessionId) throws IOException {
        String filePath = "C:\\Users\\admin\\Desktop\\CapstoneDesign\\recognition\\ArcFace\\data\\target\\";

        long fileSize = (long)image.getBytes().length;
        String originFileName = image.getOriginalFilename().replace(" ", "");

        String fileName = sessionId+"_"+originFileName;

        System.out.println("파일 이름 : "+fileName);
        System.out.println("파일 크기 : "+fileSize);
        if(fileName.getBytes().length>0){
        }

        try{
            image.transferTo(new File(filePath + fileName));
        } catch (IOException e) {
            System.out.println("사용자 이미지 저장 실패.");
            e.printStackTrace();
        }
        System.out.println("사용자 이미지 저장 성공.");

    }

    public String run(String sessionId, String fileName){
        System.out.println("얼굴 매칭....");
        String flag="완료";
        //cmd
        try{
            //windows
            flag = cmd("cd C:\\Users\\admin\\Desktop\\CapstoneDesign\\recognition\\ArcFace && python verifi_final.py --data-dir data --nfolds 1 --sessionid "+sessionId+" --filename "+fileName);
            //linux 기반
//            cmd("python ~/Desktop/Capstone/test/test.py --sessionid "+sessionId);

        }catch(Throwable t){
            t.printStackTrace();
        }

        System.out.println("결과 전송 완료.");
        return flag;

    }
    public String cmd(String command) throws IOException, InterruptedException {
        String cmd[] = new String[3];
        //windows
        cmd[0] ="cmd.exe";
        cmd[1] = "/C";
        //linux 기반
//        cmd[0] = "/bin/sh";
//        cmd[1] = "-c";
        cmd[2] = command;

        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);

        process.waitFor();

        if (process.exitValue() == 0) {
            System.out.println("정상 종료");
        } else {
            System.out.println("비정상 종료");
        }


        BufferedReader br = new BufferedReader(
                new InputStreamReader(
                        process.getInputStream()));
        String line;
        while((line =br.readLine()) !=null){
//            System.out.println(line);
            if(line.equals("N/F"))
                return "얼굴 미검출";
        }
        return "완료";
    }

}
