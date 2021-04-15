package com.back.pidetection.domain.crawling;


import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@Getter
@NoArgsConstructor
@Entity
public class Crawling {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 500, nullable = false)
    private String url;

    @Lob
    private byte[] image;

    @Builder
    public Crawling(String url, byte[] image){
        this.url = url;
        this.image = image;

    }
}
