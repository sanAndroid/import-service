package com.example.transformerservice.service;

import com.example.transformerservice.model.ImportedWinery;
import com.example.transformerservice.model.Winery;
import com.example.transformerservice.producer.WineryProducer;
import com.example.transformerservice.transformer.AbstractWineryTransformer;
import org.springframework.stereotype.Service;

@Service
public abstract class AbstractWineryTransformationService extends AbstractTransformationService<ImportedWinery, Winery> {

    protected AbstractWineryTransformationService(
            WineryProducer producer,
            AbstractWineryTransformer transformer
    ) {
        super(producer,transformer);
    }

}