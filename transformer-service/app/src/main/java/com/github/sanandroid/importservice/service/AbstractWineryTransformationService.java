package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.model.ImportedWinery;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.AbstractWineryTransformer;

public abstract class AbstractWineryTransformationService<I extends ImportedWinery>  extends AbstractTransformationService<I , WineryEntity> {

    protected AbstractWineryTransformationService(
            WineryRepository repository,
            AbstractWineryTransformer<I> transformer
    ) {
        super(repository, transformer);
    }

}