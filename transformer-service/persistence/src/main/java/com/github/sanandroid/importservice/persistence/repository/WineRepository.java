package com.github.sanandroid.importservice.persistence.repository;

import com.github.sanandroid.importservice.persistence.entity.WineEntity;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface WineRepository extends JpaRepository<WineEntity, UUID> {

    @Modifying
    @Transactional
    @Query(value = """
    INSERT INTO wines (
      id, winery_id, name, type, region, country, grapes, alcohol_content, vintage, price, price_range, currency,
      description, quality_level, shop_url, bottle_size, average_rating, number_of_ratings, critic_scores,
      food_pairings, serving_temperature, availability_status, sku, image_url, source_urls, scraped_at,
      created_at, updated_at
    ) VALUES (
      COALESCE(:#{#w.id}, gen_random_uuid()), :#{#w.winery.id}, :#{#w.name}, :#{#w.type}, :#{#w.region},
      :#{#w.country}, :#{#w.grapes}, :#{#w.alcoholContent}, :#{#w.vintage}, :#{#w.price},
      :#{#w.priceRange}, :#{#w.currency}, :#{#w.description}, :#{#w.qualityLevel}, :#{#w.shopUrl},
      :#{#w.bottleSize}, :#{#w.averageRating}, :#{#w.numberOfRatings}, :#{#w.criticScores},
      :#{#w.foodPairings}, :#{#w.servingTemperature}, :#{#w.availabilityStatus}, :#{#w.sku},
      :#{#w.imageUrl}, :#{#w.sourceUrls}, :#{#w.scrapedAt}, NOW(), NOW()
    )
    ON CONFLICT (shop_url) DO UPDATE SET
      winery_id           = EXCLUDED.winery_id,
      name                = EXCLUDED.name,
      type                = EXCLUDED.type,
      region              = EXCLUDED.region,
      country             = EXCLUDED.country,
      grapes              = EXCLUDED.grapes,
      alcohol_content     = EXCLUDED.alcohol_content,
      vintage             = EXCLUDED.vintage,
      price               = EXCLUDED.price,
      price_range         = EXCLUDED.price_range,
      currency            = EXCLUDED.currency,
      description         = EXCLUDED.description,
      quality_level       = EXCLUDED.quality_level,
      bottle_size         = EXCLUDED.bottle_size,
      average_rating      = EXCLUDED.average_rating,
      number_of_ratings   = EXCLUDED.number_of_ratings,
      critic_scores       = EXCLUDED.critic_scores,
      food_pairings       = EXCLUDED.food_pairings,
      serving_temperature = EXCLUDED.serving_temperature,
      availability_status = EXCLUDED.availability_status,
      sku                 = EXCLUDED.sku,
      image_url           = EXCLUDED.image_url,
      source_urls         = EXCLUDED.source_urls,
      scraped_at          = EXCLUDED.scraped_at,
      updated_at          = NOW()
    """, nativeQuery = true)
    int upsert(@Param("w") WineEntity w);
}