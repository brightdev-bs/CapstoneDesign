package com.server.ai.aiserver.web;

import com.server.ai.aiserver.service.AiService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;


@RequiredArgsConstructor
@RestController
public class reciveController {
    
    private final AiService aiService;
    
    @PostMapping("/api/detection/input")
    public @ResponseBody String saveAndExcute(@RequestParam("image")MultipartFile image) throws IOException {
        HttpServletRequest req = ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest();
        String clientIp = req.getRemoteAddr();

        aiService.localSave(image);
        aiService.run(clientIp);

        return "/result";

    }
}
