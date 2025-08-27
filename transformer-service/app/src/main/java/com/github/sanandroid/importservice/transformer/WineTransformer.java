package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import org.springframework.stereotype.Service;

@Service
public class WineTransformer implements AbstractTransformer<Wine, WineEntity> {

    private final WineryRepository wineryRepository;

    public WineTransformer(WineryRepository wineryRepository) {
        this.wineryRepository = wineryRepository;
    }

    @Override
    public WineEntity transformToEntity(Wine wine) {
        WineryEntity wineryEntity = wineryRepository.findByWebsite(wine.wineryWebsite())
                .orElseThrow(() -> new RuntimeException("Winery not found for website: " + wine.wineryWebsite()));

        return new WineEntity(
                null,
                null,
                wineryEntity,
                wine.name(),
                wine.type(),
                wine.region(),
                wine.country(),
                wine.grapes(),
                wine.alcoholContent(),
                wine.vintage(),
                wine.price(),
                wine.priceRange(),
                wine.currency(),
                wine.description(),
                wine.qualityLevel(),
                wine.shopUrl(),
                wine.bottleSize(),
                wine.averageRating(),
                wine.numberOfRatings(),
                wine.criticScores(),
                wine.foodPairings(),
                wine.servingTemperature(),
                wine.availabilityStatus(),
                wine.sku(),
                wine.imageUrl(),
                wine.sourceUrls(),
                wine.scrapedAt(),
                null,
                null
        );
    }
}
