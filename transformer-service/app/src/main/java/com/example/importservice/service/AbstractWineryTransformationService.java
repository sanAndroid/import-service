package com.example.importservice.service;

import com.example.importservice.model.ImportedWinery;
import com.example.importservice.model.WineryEntity;
import com.example.importservice.repository.WineryRepository;
import com.example.importservice.transformer.AbstractWineryTransformer;

public abstract class AbstractWineryTransformationService<I extends ImportedWinery>  extends AbstractTransformationService<I , WineryEntity> {

    protected AbstractWineryTransformationService(
            WineryRepository repository,
            AbstractWineryTransformer<I> transformer
    ) {
        super(repository, transformer);
    }

}