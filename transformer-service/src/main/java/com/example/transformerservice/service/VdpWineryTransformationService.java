package com.example.transformerservice.service;

import com.example.transformerservice.model.VdpWinery;
import com.example.transformerservice.producer.WineryProducer;
import com.example.transformerservice.transformer.VdpWineryTransformer;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformationService extends AbstractWineryTransformationService<VdpWinery> {

    protected VdpWineryTransformationService(
            WineryProducer producer,
            VdpWineryTransformer transformer
    ) {
        super(producer, transformer);
    }

}