package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.model.winery.WineryDto;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.AbstractWineryTransformer;

public abstract class AbstractWineryTransformationService<I extends WineryDto>
        extends AbstractTransformationService<
        I,
        WineryEntity,
        WineryRepository,
        AbstractWineryTransformer<I>
        > {

    protected AbstractWineryTransformationService(
            WineryRepository repository,
            AbstractWineryTransformer<I> transformer
    ) {
        super(repository, transformer);
    }
}