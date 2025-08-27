package com.github.sanandroid.importservice.persistence.repository;

import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface WineRepository extends JpaRepository<WineEntity, UUID> {

    @Query(value = """
        INSERT INTO wines (
            id, winery_id, name, vintage, grape_varieties, price, description,
            image_url, region, quality_level, shop_url, wine_type, alcohol_content,
            bottle_size, country, average_rating, number_of_ratings, critic_scores,
            food_pairings, serving_temperature, availability_status, sku, source,
            scraped_at, embedding, created_at, updated_at
        )
        VALUES (
            :#{#wine.id}, :#{#wine.winery.id}, :#{#wine.name}, :#{#wine.vintage}, 
            CAST(:#{#wine.grapeVarieties} AS jsonb), :#{#wine.price}, :#{#wine.description},
            :#{#wine.imageUrl}, :#{#wine.region}, :#{#wine.qualityLevel}, :#{#wine.shopUrl},
            :#{#wine.wineType}, :#{#wine.alcoholContent}, :#{#wine.bottleSize},
            :#{#wine.country}, :#{#wine.averageRating}, :#{#wine.numberOfRatings},
            CAST(:#{#wine.criticScores} AS jsonb), CAST(:#{#wine.foodPairings} AS jsonb),
            :#{#wine.servingTemperature}, :#{#wine.availabilityStatus}, :#{#wine.sku},
            :#{#wine.source}, :#{#wine.scrapedAt}, CAST(:#{#wine.embedding} AS vector),
            now(), now()
        )
        ON CONFLICT (sku) DO UPDATE SET
            winery_id = EXCLUDED.winery_id,
            name = EXCLUDED.name,
            vintage = EXCLUDED.vintage,
            grape_varieties = EXCLUDED.grape_varieties,
            price = EXCLUDED.price,
            description = EXCLUDED.description,
            image_url = EXCLUDED.image_url,
            region = EXCLUDED.region,
            quality_level = EXCLUDED.quality_level,
            shop_url = EXCLUDED.shop_url,
            wine_type = EXCLUDED.wine_type,
            alcohol_content = EXCLUDED.alcohol_content,
            bottle_size = EXCLUDED.bottle_size,
            country = EXCLUDED.country,
            average_rating = EXCLUDED.average_rating,
            number_of_ratings = EXCLUDED.number_of_ratings,
            critic_scores = EXCLUDED.critic_scores,
            food_pairings = EXCLUDED.food_pairings,
            serving_temperature = EXCLUDED.serving_temperature,
            availability_status = EXCLUDED.availability_status,
            source = EXCLUDED.source,
            scraped_at = EXCLUDED.scraped_at,
            embedding = EXCLUDED.embedding,
            updated_at = now()
        """,
            nativeQuery = true)
    void upsert(@Param("wine") WineEntity wine);
}
