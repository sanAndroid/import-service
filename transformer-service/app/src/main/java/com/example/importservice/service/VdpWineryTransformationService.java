package com.example.importservice.service;

import com.example.importservice.model.VdpWinery;
import com.example.importservice.producer.WineryProducer;
import com.example.importservice.transformer.VdpWineryTransformer;
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