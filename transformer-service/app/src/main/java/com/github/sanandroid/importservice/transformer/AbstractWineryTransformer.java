package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.ImportedWinery;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;

public interface AbstractWineryTransformer<T extends  ImportedWinery> extends AbstractTransformer<T, WineryEntity> {
}

