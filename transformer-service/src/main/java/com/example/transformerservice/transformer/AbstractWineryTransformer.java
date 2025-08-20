package com.example.transformerservice.transformer;

import com.example.transformerservice.model.ImportedWinery;
import com.example.transformerservice.model.Winery;

public interface AbstractWineryTransformer<T extends  ImportedWinery> extends AbstractTransformer<T, Winery> {
}

