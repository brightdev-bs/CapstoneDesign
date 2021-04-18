package com.back.pidetection.web;

import com.back.pidetection.web.dto.DetectionResultResponseDto;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.web.client.RestTemplate;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringRunner.class)
@WebMvcTest(DetectionController.class)
public class DetectionControllerTest {
    @Autowired
    MockMvc mockMvc;

    @Autowired
    RestTemplate restTemplate;


    @Test
    public void connect() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.get("/"))
                .andExpect(status().isOk());
    }

    @Test public void result(){
        byte[] image ={1,1,1,1};
        DetectionResultResponseDto responseDto = new DetectionResultResponseDto("www",image);

    }
}
