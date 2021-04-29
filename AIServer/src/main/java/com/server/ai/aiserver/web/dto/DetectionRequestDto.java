package com.server.ai.aiserver.web.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@Getter
public class DetectionRequestDto {
    private byte[] image;

    @Builder
    public DetectionRequestDto(byte[] image){
        this.image =image;
    }

}
