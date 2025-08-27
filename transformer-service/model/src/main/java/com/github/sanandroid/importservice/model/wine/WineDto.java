package com.github.sanandroid.importservice.model.wine;

import java.util.List;
import java.util.Map;

public record WineDto(
            String name,
            String winery,
            Integer vintage,
            List<String> grapeVarieties,
            Double price,
            String description,
            String imageUrl,
            String wineryWebsite,
            String region,
            String qualityLevel,
            String shopUrl,
            String wineType,
            Double alcoholContent,
            String bottleSize,
            String country,
            Double averageRating,
            Integer numberOfRatings,
            Map<String, Double> criticScores,
            List<String> foodPairings,
            String servingTemperature,
            String availabilityStatus,
            String sku,
            String source,
            String scrapedAt
)
    {}
