package com.back.pidetection.web;


import com.back.pidetection.service.CrawlingService;
import com.back.pidetection.web.dto.CrawlingSaveRequestDto;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RequiredArgsConstructor
@RestController
public class CrawlingApiController {

    private final CrawlingService crawlingService;

    @PostMapping("/api/face")
    public Long save(@RequestBody CrawlingSaveRequestDto requestDto){
        return crawlingService.save(requestDto);
    }
}
