package com.example.importservice.transformer;

public interface AbstractTransformer<T,O> {
    O transform(T t);
}
