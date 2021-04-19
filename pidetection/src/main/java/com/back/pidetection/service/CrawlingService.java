package com.back.pidetection.service;

import com.back.pidetection.domain.crawling.CrawlingRepository;
import com.back.pidetection.web.dto.CrawlingSaveRequestDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@RequiredArgsConstructor
@Service
public class CrawlingService {

    private final CrawlingRepository crawlingRepository;

    @Transactional
    public Long save(CrawlingSaveRequestDto requestDto){
        return crawlingRepository.save(requestDto.toEntity()).getId();
    }

}
