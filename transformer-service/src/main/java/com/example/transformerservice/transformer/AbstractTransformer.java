package com.example.transformerservice.transformer;

public interface AbstractTransformer<T,O> {
    public abstract O transform(T t);
}
