package com.github.sanandroid.importservice.model.wine;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;
import java.util.Map;

public record Wine(
        @JsonProperty("name") String name,
        @JsonProperty("winery") String winery,
        @JsonProperty("winery_website") String wineryWebsite,
        @JsonProperty("type") String type,
        @JsonProperty("region") String region,
        @JsonProperty("country") String country,
        @JsonProperty("grapes") List<String> grapes,
        @JsonProperty("alcohol_content") Float alcoholContent,
        @JsonProperty("vintage") Integer vintage,
        @JsonProperty("price") Float price,
        @JsonProperty("price_range") String priceRange,
        @JsonProperty("currency") String currency,
        @JsonProperty("description") String description,
        @JsonProperty("quality_level") String qualityLevel,
        @JsonProperty("shop_url") String shopUrl,
        @JsonProperty("bottle_size") String bottleSize,
        @JsonProperty("average_rating") Float averageRating,
        @JsonProperty("number_of_ratings") Integer numberOfRatings,
        @JsonProperty("critic_scores") Map<String, Float> criticScores,
        @JsonProperty("food_pairings") List<String> foodPairings,
        @JsonProperty("serving_temperature") String servingTemperature,
        @JsonProperty("availability_status") String availabilityStatus,
        @JsonProperty("sku") String sku,
        @JsonProperty("image_url") String imageUrl,
        @JsonProperty("source_urls") List<String> sourceUrls,
        @JsonProperty("scraped_at") String scrapedAt
) {
}