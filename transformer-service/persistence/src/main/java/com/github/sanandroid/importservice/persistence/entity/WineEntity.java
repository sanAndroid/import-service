package com.github.sanandroid.importservice.persistence.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(
        name = "wines",
        indexes = {
                @Index(name = "idx_wine_winery_vintage", columnList = "winery_id, vintage"),
                @Index(name = "idx_wine_name_winery", columnList = "name, winery_id")
        },
        uniqueConstraints = {
                // adjust as you like; sku often unique, or (winery, name, vintage, bottle_size)
                @UniqueConstraint(name = "uk_wine_sku", columnNames = {"sku"})
        }
)
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
public class WineEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false, updatable = false, columnDefinition = "uuid")
    private UUID id;

    // --- Relations ---
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "winery_id", nullable = false, columnDefinition = "uuid",
            foreignKey = @ForeignKey(name = "fk_wine_winery"))
    private WineryEntity winery;

    // --- Core fields ---
    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "vintage")
    private Integer vintage;

    @JdbcTypeCode(SqlTypes.JSON) // requires PostgreSQL + Hibernate JSON support
    @Column(name = "grape_varieties", columnDefinition = "jsonb")
    private List<String> grapeVarieties;

    @Column(name = "price")
    private Double price;

    @Column(name = "description", columnDefinition = "text")
    private String description;

    @Column(name = "image_url")
    private String imageUrl;

    @Column(name = "region")
    private String region;

    @Column(name = "quality_level")
    private String qualityLevel;

    @Column(name = "shop_url")
    private String shopUrl;

    @Column(name = "wine_type")
    private String wineType;

    @Column(name = "alcohol_content")
    private Double alcoholContent;

    @Column(name = "bottle_size")
    private String bottleSize;

    @Column(name = "country")
    private String country;

    @Column(name = "average_rating")
    private Double averageRating;

    @Column(name = "number_of_ratings")
    private Integer numberOfRatings;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "critic_scores", columnDefinition = "jsonb")
    private Map<String, Double> criticScores;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "food_pairings", columnDefinition = "jsonb")
    private List<String> foodPairings;

    @Column(name = "serving_temperature")
    private String servingTemperature;

    @Column(name = "availability_status")
    private String availabilityStatus;

    @Column(name = "sku", length = 128)
    private String sku;

    @Column(name = "source")
    private String source;

    @Column(name = "scraped_at")
    private String scrapedAt; // or Instant if you store an actual timestamp

    // --- Embedding (pgvector) ---
    @JdbcTypeCode(SqlTypes.VECTOR)
    @Column(name = "embedding", columnDefinition = "vector(384)")
    private float[] embedding;

    // --- Timestamps ---
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}