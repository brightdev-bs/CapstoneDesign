package com.back.pidetection.web;

import com.back.pidetection.web.dto.DetectionResultDto;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.ArrayList;


@Controller
public class DetectionController {
    ArrayList<DetectionResultDto> resultDtos = new ArrayList<>();

    @GetMapping("/")
    public String index(){
        return "index";
    }

    @GetMapping("/wait-page")
    public String waitPage(){
        return "wait-page";
    }

    @PostMapping("/api/face/result")
    public String saveResult(@RequestBody DetectionResultDto resultDto, Model model) {
        if (resultDto.getImage().length != 0) {
            resultDtos.add(resultDto);
            return "wait-page";
        } else {
            model.addAttribute("result", resultDtos);
            return "redirect:detection-result";
        }

    }

}
