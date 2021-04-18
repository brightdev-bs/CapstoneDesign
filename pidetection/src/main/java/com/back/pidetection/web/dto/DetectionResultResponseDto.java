package com.back.pidetection.web.dto;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public class DetectionResultResponseDto {
    private final String[] url;
    private final byte[][] image;

}
