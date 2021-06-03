package com.server.ai.aiserver.web;

import com.server.ai.aiserver.service.AiService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;

@RequiredArgsConstructor
@RestController
public class reciveController {
    final int MAXIMUMMULTI = 1;
    int currMulti =0;
    int waiting =0;
    Object addLock = new Object();
    Object waitLock =new Object();
    Object doneLock = new Object();
    ArrayList<String[]> queue =new ArrayList<String[]>();

    private final AiService aiService;

    @GetMapping("/")
    public String index(){
        return "index";
    }
    @CrossOrigin("http://ec2-13-209-242-131.ap-northeast-2.compute.amazonaws.com:8080")
    @PostMapping("/api/detection/input")
    public  @ResponseBody String saveAndExcute(@RequestParam("image")MultipartFile image,  @RequestParam("sessionId") String sessionId) throws IOException {

        long start = System.currentTimeMillis();


        String originFileName = image.getOriginalFilename().replace(" ", "");

        String fileName = sessionId+"_"+originFileName;
        aiService.localSave(image, sessionId);
        synchronized (addLock){
            queue.add(new String[]{fileName,sessionId});
            waiting =queue.size();
        }


        if(currMulti >= MAXIMUMMULTI){
            System.out.println("서버용량을 모두 사용중입니다. Wait...");
            System.out.println("현재 대기열: "+currMulti);
        }

        synchronized (waitLock){
            while(currMulti >= MAXIMUMMULTI){}
            String[] curr = queue.remove(0);

            fileName = curr[0];
            sessionId = curr[1];
            System.out.println("매칭 실행 session: "+sessionId);
            System.out.println("현재 실행중인 프로세스 수: "+ ++currMulti);
            System.out.println("대기 중인 처리: "+ queue.size());

        }
        String flag = aiService.run(sessionId, fileName);

        long end = System.currentTimeMillis();

        System.out.println("소요시간 : "+ (end-start)/1000);

        synchronized (doneLock){
           --currMulti;
        }

        if(flag.equals("완료"))
            return "/result";
        else
            return "얼굴 미검출";

    }


}
