package com.github.sanandroid.importservice.transformer;

public interface AbstractTransformer<T, E> {
    E transform(T t);
}
