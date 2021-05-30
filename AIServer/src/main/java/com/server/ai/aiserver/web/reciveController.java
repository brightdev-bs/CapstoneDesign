package com.server.ai.aiserver.web;

import com.server.ai.aiserver.service.AiService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.ArrayList;

@RequiredArgsConstructor
@RestController
public class reciveController {
    Boolean flag = false;
    ArrayList<String[]> queue =new ArrayList<String[]>();

    private final AiService aiService;

    @GetMapping("/")
    public String index(){
        return "index";
    }
    @CrossOrigin("http://ec2-13-209-242-131.ap-northeast-2.compute.amazonaws.com:8080")
    @PostMapping("/api/detection/input")
    public @ResponseBody String saveAndExcute(@RequestParam("image")MultipartFile image,  @RequestParam("sessionId") String sessionId) throws IOException {
        long start = System.currentTimeMillis();

//        HttpServletRequest req = ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest();
//        String ip = req.getRemoteAddr();
//        System.out.println("IP: "+ip);
        System.out.println(sessionId);

        String fileName = sessionId+"_"+image.getOriginalFilename();
        aiService.localSave(image, sessionId);

        queue.add(new String[]{fileName,sessionId});
        while(flag){}
        flag =true;
        String[] curr = queue.remove(0);
        fileName = curr[0];
        sessionId = curr[1];
        aiService.run(sessionId, fileName);

        System.out.println("매칭 완료.");

        long end = System.currentTimeMillis();

        System.out.println("소요시간 : "+ (end-start)/1000);

        flag = false;
        return "/result";

    }


}
