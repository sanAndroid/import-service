package com.github.sanandroid.importservice.persistence.converter;

import com.pgvector.PGvector;
import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

import java.sql.SQLException;

@Converter(autoApply = false)
public class PgVectorFloatArrayConverter implements AttributeConverter<float[], Object> {

    @Override
    public Object convertToDatabaseColumn(float[] attribute) {
        if (attribute == null) {
            return null;
        }
        return new PGvector(attribute);
    }

    @Override
    public float[] convertToEntityAttribute(Object dbData) {
        if (dbData == null) {
            return null;
        }
        if (dbData instanceof PGvector pgVector) {
            return pgVector.toArray();
        }
        // fallback if dbData is stored as string (depends on driver)
        if (dbData instanceof String str) {
            try {
                return new PGvector(str).toArray();
            } catch (SQLException e) {
                // TODO: Probably a log error and return null is better here
                throw new RuntimeException(e);
            }
        }
        throw new IllegalArgumentException("Unsupported type for vector column: " + dbData.getClass());
    }
}