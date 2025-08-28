package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.model.wine.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;

@Service
public class WineTransformer implements AbstractTransformer<WineDto, WineEntity> {

    private final WineryRepository wineryRepository;

    public WineTransformer(WineryRepository wineryRepository) {
        this.wineryRepository = wineryRepository;
    }

    @Override
    public WineEntity transformToEntity(WineDto wine) {
        WineryEntity wineryEntity = wineryRepository.findByWebsite(wine.getWineryWebsite())
                .orElseThrow(() -> new RuntimeException("Winery not found for website: " + wine.getWineryWebsite()));

        return new WineEntity(
                null,                       // id
                null,                       // externalId
                wineryEntity,               // winery
                wine.getName(),             // name
                wine.getType(),             // type
                wine.getRegion(),           // region
                wine.getCountry(),          // country
                wine.getGrapes(),           // grapes
                BigDecimal.valueOf(wine.getAlcoholContent()).setScale(1, RoundingMode.HALF_UP),   // alcoholContent
                wine.getVintage(),          // vintage
                BigDecimal.valueOf(wine.getPrice()).setScale(2,RoundingMode.HALF_UP),            // price
                wine.getPriceRange(),       // priceRange
                wine.getCurrency(),         // currency
                wine.getDescription(),      // description
                wine.getQualityLevel(),     // qualityLevel
                wine.getShopUrl(),          // shopUrl
                wine.getBottleSize(),       // bottleSize
                BigDecimal.valueOf(wine.getAverageRating()).setScale(1, RoundingMode.HALF_UP),    // averageRating
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
}
