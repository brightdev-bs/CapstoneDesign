package com.back.pidetection.web;

import com.back.pidetection.web.dto.DetectionResultResponseDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.ArrayList;

@Controller
public class DetectionController {

    @GetMapping("/")
    public String index(){
        return "index";
    }

    @GetMapping("/api/face/result")
    public String result(DetectionResultResponseDto responseDto, Model model){
        model.addAttribute("result", responseDto);

        return "detection-result";
    }

}
