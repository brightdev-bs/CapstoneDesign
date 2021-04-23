package com.back.pidetection.web.dto;


import com.back.pidetection.domain.crawling.Crawling;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;


@Getter
@NoArgsConstructor
public class CrawlingSaveRequestDto {
    private String storageUrl;
    private String url;

    @Builder
    public CrawlingSaveRequestDto(String url, String storageUrl){
        this.url = url;
        this.storageUrl =storageUrl;
    }

    public Crawling toEntity(){
        return Crawling.builder()
                .url(url)
                .storageUrl(storageUrl)
                .build();
    }


}
