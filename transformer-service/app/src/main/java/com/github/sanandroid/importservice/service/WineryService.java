package com.github.sanandroid.importservice.service;

// TODO: See how to implement that later import com.github.sanandroid.importservice.model.winery.WineryDto;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.AbstractWineryTransformer;

public class AbstractWineryService<I>
        extends AbstractService<
                I,
                WineryEntity,
        WineryRepository,
                AbstractWineryTransformer<I>
                > {

    protected AbstractWineryService(
            WineryRepository repository,
            AbstractWineryTransformer<I> transformer
    ) {
        super(repository, transformer);
    }
}