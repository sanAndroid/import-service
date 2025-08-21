package com.example.importservice.transformer;

import com.example.importservice.model.ImportedWinery;
import com.example.importservice.model.Winery;

public interface AbstractWineryTransformer<T extends  ImportedWinery> extends AbstractTransformer<T, Winery> {
}

