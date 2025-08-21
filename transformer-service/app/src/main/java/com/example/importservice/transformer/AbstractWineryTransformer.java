package com.example.importservice.transformer;

import com.example.importservice.model.ImportedWinery;
import com.example.importservice.model.Winery;
import com.example.importservice.model.WineryEntity;

public interface AbstractWineryTransformer<T extends  ImportedWinery> extends AbstractTransformer<T, WineryEntity> {
}

