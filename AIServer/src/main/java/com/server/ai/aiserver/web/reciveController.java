package com.server.ai.aiserver.web;

import com.server.ai.aiserver.service.AiService;
import com.server.ai.aiserver.web.dto.DetectionRequestDto;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


@RequiredArgsConstructor
@RestController
public class reciveController {
    
    private final AiService aiService;

    @PostMapping("/api/detection")
    public void saveAndExcute(@RequestBody DetectionRequestDto requestDto){
        aiService.localSave(requestDto);
        aiService.run();
    }
}
