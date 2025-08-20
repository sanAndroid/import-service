package com.example.transformerservice.transformer;

public interface AbstractTransformer<T,O> {
    O transform(T t);
}
