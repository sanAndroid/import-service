package com.example.transformerservice.service;

import com.example.transformerservice.model.ImportedWinery;
import com.example.transformerservice.model.Winery;
import com.example.transformerservice.producer.WineryProducer;
import com.example.transformerservice.transformer.AbstractWineryTransformer;

public abstract class AbstractWineryTransformationService<I extends ImportedWinery>  extends AbstractTransformationService<I , Winery> {

    protected AbstractWineryTransformationService(
            WineryProducer producer,
            AbstractWineryTransformer<I> transformer
    ) {
        super(producer, transformer);
    }

}