package com.example.importservice.service;

import com.example.importservice.model.ImportedWinery;
import com.example.importservice.model.Winery;
import com.example.importservice.producer.WineryProducer;
import com.example.importservice.transformer.AbstractWineryTransformer;

public abstract class AbstractWineryTransformationService<I extends ImportedWinery>  extends AbstractTransformationService<I , Winery> {

    protected AbstractWineryTransformationService(
            WineryProducer producer,
            AbstractWineryTransformer<I> transformer
    ) {
        super(producer, transformer);
    }

}