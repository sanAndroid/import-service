package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.winery.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Optional;

@Service
public class WineTransformer implements AbstractTransformer<WineDto, WineEntity> {

    @Override
    public WineEntity transformToEntity(WineDto wine) {

        return new WineEntity(
                null,                       // id
                null,                       // externalId
                null,               // winery
                wine.getName(),             // name
                wine.getType(),             // type
                wine.getRegion(),           // region
                wine.getCountry(),          // country
                wine.getGrapes(),           // grapes
                convertToBigDecimal(wine.getAlcoholContent(), 1),
                wine.getVintage(),          // vintage
                convertToBigDecimal(wine.getPrice(), 2),            // price
                wine.getPriceRange(),       // priceRange
                wine.getCurrency(),         // currency
                wine.getDescription(),      // description
                wine.getQualityLevel(),     // qualityLevel
                wine.getShopUrl(),          // shopUrl
                wine.getBottleSize(),       // bottleSize
                convertToBigDecimal(wine.getAverageRating(), 1),    // averageRating
                wine.getNumberOfRatings(),  // numberOfRatings
                null,     // TODO: criticScores => To this later, once I get real critic scores
                wine.getFoodPairings(),     // foodPairings
                wine.getServingTemperature(), // servingTemperature
                wine.getAvailabilityStatus(), // availabilityStatus
                wine.getSku(),              // sku
                wine.getImageUrl(),         // imageUrl
                wine.getSourceUrls(),       // sourceUrls
                wine.getScrapedAt(),        // scrapedAt
                null,                       // createdAt
                null                        // updatedAt
        );
    }

    private BigDecimal convertToBigDecimal(Double value, Integer scale) {
        return Optional.ofNullable(value)
                .map(val -> BigDecimal.valueOf(val).setScale(scale, RoundingMode.HALF_UP))
                .orElse(null);
    }
}
