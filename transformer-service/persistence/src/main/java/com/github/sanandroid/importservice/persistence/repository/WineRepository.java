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
              id, winery_id, name, type, region, country,
              embedding, alcohol_content, vintage, price, price_range, currency,
              description, quality_level, shop_url, bottle_size, average_rating,
              number_of_ratings, serving_temperature, availability_status, sku,
              image_url, scraped_at, created_at, updated_at
            ) VALUES (
              COALESCE(:#{#w.id}, gen_random_uuid()),
              :#{#w.winery.id},
              :#{#w.name},
              :#{#w.type},
              :#{#w.region},
              :#{#w.country},
              CAST(:#{#w.embedding} AS vector),
              :#{#w.alcoholContent},
              :#{#w.vintage},
              :#{#w.price},
              :#{#w.priceRange},
              :#{#w.currency},
              :#{#w.description},
              :#{#w.qualityLevel},
              :#{#w.shopUrl},
              :#{#w.bottleSize},
              :#{#w.averageRating},
              :#{#w.numberOfRatings},
              :#{#w.servingTemperature},
              :#{#w.availabilityStatus},
              :#{#w.sku},
              :#{#w.imageUrl},
              :#{#w.scrapedAt},
              NOW(), NOW()
            )
            -- prefer a composite wine identity; fallback to shop_url when present
            ON CONFLICT ON CONSTRAINT wines_upsert_idx
            DO UPDATE SET
              type               = EXCLUDED.type,
              region             = EXCLUDED.region,
              country            = EXCLUDED.country,
              embedding          = EXCLUDED.embedding,
              alcohol_content    = EXCLUDED.alcohol_content,
              price              = EXCLUDED.price,
              price_range        = EXCLUDED.price_range,
              currency           = EXCLUDED.currency,
              description        = EXCLUDED.description,
              quality_level      = EXCLUDED.quality_level,
              shop_url           = EXCLUDED.shop_url,
              bottle_size        = EXCLUDED.bottle_size,
              average_rating     = EXCLUDED.average_rating,
              number_of_ratings  = EXCLUDED.number_of_ratings,
              serving_temperature= EXCLUDED.serving_temperature,
              availability_status= EXCLUDED.availability_status,
              sku                = EXCLUDED.sku,
              image_url          = EXCLUDED.image_url,
              scraped_at         = EXCLUDED.scraped_at,
              updated_at         = NOW()
            """, nativeQuery = true)
    void upsert(@Param("w") WineEntity w);
}