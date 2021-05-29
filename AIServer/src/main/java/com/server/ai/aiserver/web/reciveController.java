package com.server.ai.aiserver.web;

import com.server.ai.aiserver.service.AiService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpSession;
import java.io.IOException;


@RequiredArgsConstructor
@RestController
public class reciveController {
    
    private final AiService aiService;

    @GetMapping("/")
    public String index(){
        return "index";
    }
    
    @PostMapping("/api/detection/input")
    public @ResponseBody String saveAndExcute(@RequestParam("image")MultipartFile image, HttpSession session) throws IOException {
        String sessionId = session.getId();
        String fileName = sessionId+"_"+image.getOriginalFilename();

        aiService.localSave(image, sessionId);
        aiService.run(sessionId, fileName);

        System.out.println("매칭 완료.");

        return "/result";

    }
}
