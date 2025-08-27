package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.wine.Wine;
import com.github.sanandroid.importservice.model.wine.WineDto;
import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.sanandroid.importservice.persistence.repository.WineryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Optional;

@Component
@RequiredArgsConstructor
public class WineTransformer implements AbstractTransformer<WineDto, WineEntity> {

    private final WineryRepository wineryRepository;

    @Override
    public WineEntity transformToEntity(WineDto dto) {
        // Resolve winery (prefer by ID; fallback by website/name if needed)
        WineryEntity winery = resolveWinery(dto);
        WineEntity e = new WineEntity();
        e.setWinery(winery);
        e.setName(dto.name());
        e.setVintage(dto.vintage());
        e.setGrapeVarieties(dto.grapeVarieties());
        e.setPrice(dto.price());
        e.setDescription(dto.description());
        e.setImageUrl(dto.imageUrl());
        e.setRegion(dto.region());
        e.setQualityLevel(dto.qualityLevel());
        e.setShopUrl(dto.shopUrl());
        e.setWineType(dto.wineType());
        e.setAlcoholContent(dto.alcoholContent());
        e.setBottleSize(dto.bottleSize());
        e.setCountry(dto.country());
        e.setAverageRating(dto.averageRating());
        e.setNumberOfRatings(dto.numberOfRatings());
        e.setCriticScores(dto.criticScores());
        e.setFoodPairings(dto.foodPairings());
        e.setServingTemperature(dto.servingTemperature());
        e.setAvailabilityStatus(dto.availabilityStatus());
        e.setSku(dto.sku());
        e.setSource(dto.source());
        e.setScrapedAt(dto.scrapedAt());        // consider Instant and proper parsing
        e.setEmbedding(null);                   // filled later by vectorizer
        e.setCreatedAt(Instant.now());          // DB @CreationTimestamp can handle this
        e.setUpdatedAt(Instant.now());
        return e;
    }


    private WineryEntity resolveWinery(WineDto dto) {
        if (dto.wineryWebsite() != null) {
            Optional<WineryEntity> byWebsite = wineryRepository.findByWebsite(dto.wineryWebsite());
            if (byWebsite.isPresent()) return byWebsite.get();
        }
        if (dto.winery() != null) {
            return wineryRepository.findByName(dto.winery()).orElseThrow(() -> new IllegalArgumentException("Winery not found: " + dto.winery()));
        }


        throw new IllegalArgumentException("Cannot resolve winery (no id/website/name in DTO)");
    }
}