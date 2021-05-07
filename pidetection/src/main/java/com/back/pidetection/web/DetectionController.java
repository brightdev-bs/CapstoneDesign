package com.back.pidetection.web;

import com.back.pidetection.web.dto.DetectionResultDto;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.util.ArrayList;


@Controller
public class DetectionController {
//    ArrayList<String> urls= new ArrayList<>();
//    ArrayList<byte[]> images= new ArrayList<>();
    ArrayList<DetectionResultDto> resultDtos = new ArrayList<>();
    @GetMapping("/")
    public String index(){
        return "index";
    }

    @GetMapping("/wait-page")
    public String waitPage(){
        return "wait-page";
    }

    @PostMapping("/api/detection/result")
    public String saveResult(@RequestBody DetectionResultDto resultDto, Model model) {
        if (resultDto.getImage().length != 0) {
//            urls.add(resultDto.getUrl());
//            images.add(resultDto.getImage());
            resultDtos.add(resultDto);
            return "wait-page";
        } else {
            return "redirect:detection-result";
        }

    }
    @GetMapping("/detection-result")
    public String resultTest2(Model model){
//        model.addAttribute("result-url", urls);
//        model.addAttribute("result-image", images);
        model.addAttribute("result",resultDtos);
        return "detection-result";
    }


    @PostMapping("/api/detection/input")
    public @ResponseBody void inputSaveTest( @RequestParam("image")MultipartFile image) throws IOException {
        String filePath="/Users/kimtaejun/Desktop/Capstone/pidetection/src/main/java/com/back/pidetection/web/";

        String fileName = image.getOriginalFilename();
        System.out.println("파일 이름 : "+fileName);
        byte[] im = image.getBytes();
        long fileSize = (long)im.length;
        System.out.println("파일 크기 : "+im.length);

        try{
            image.transferTo(new File(filePath + fileName));

        } catch (IOException e) {
            System.out.println("사용자 이미지 저장 실패.");
            e.printStackTrace();
        }
        System.out.println("사용자 이미지 저장 성공.");

    }

}
