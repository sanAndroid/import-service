package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.ImportedWinery;
import com.github.sanandroid.importservice.model.WineryEntity;

public interface AbstractWineryTransformer<T extends  ImportedWinery> extends AbstractTransformer<T, WineryEntity> {
}

