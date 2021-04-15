package com.back.pidetection.service;

import com.back.pidetection.domain.crawling.CrawlingRepository;
import com.back.pidetection.web.dto.CrawlingSaveRequestDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class CrawlingService {

    private final CrawlingRepository crawlingRepository;

    public Long save(CrawlingSaveRequestDto requestDto){
        return crawlingRepository.save(requestDto.toEntity()).getId();
    }

}