package com.back.pidetection.web.dto;


import com.back.pidetection.domain.crawling.Crawling;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;


@Getter
@NoArgsConstructor
public class CrawlingSaveRequestDto {
    private String url;
    private byte[] image;

    @Builder
    public CrawlingSaveRequestDto(String url, byte[] image){
        this.url = url;
        this.image =image;
    }

    public Crawling toEntity(){
        return Crawling.builder()
                .url(url)
                .image(image)
                .build();
    }


}
