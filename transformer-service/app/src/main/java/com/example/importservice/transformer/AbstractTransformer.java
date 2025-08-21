package com.example.importservice.transformer;

public interface AbstractTransformer<T, E> {
    E transform(T t);
}
