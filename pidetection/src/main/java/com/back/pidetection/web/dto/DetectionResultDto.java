package com.back.pidetection.web.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;


@Getter
@NoArgsConstructor
public class DetectionResultDto {
    private String url;
    private byte[] image;

    @Builder
    public DetectionResultDto(String url, byte[] image){
        this.image = image;
        this.url =url;
    }

}
