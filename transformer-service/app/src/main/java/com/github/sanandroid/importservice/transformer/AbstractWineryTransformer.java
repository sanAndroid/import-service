package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.winery.WineryDto;
import com.github.sanandroid.importservice.model.winery.WineryMessage;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;

public interface AbstractWineryTransformer<I extends WineryDto> extends AbstractTransformer<I, WineryEntity> {

    WineryMessage transformToMessage(I dto);

}

