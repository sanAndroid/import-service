package com.github.sanandroid.importservice.transformer;

public interface AbstractTransformer<I, E> {
    E transformToEntity(I i);
}
