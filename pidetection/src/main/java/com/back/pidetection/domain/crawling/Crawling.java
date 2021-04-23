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
    private String storageUrl;

    @Builder
    public Crawling(String url, String storageUrl){
        this.url = url;
        this.storageUrl = storageUrl;

    }
}
