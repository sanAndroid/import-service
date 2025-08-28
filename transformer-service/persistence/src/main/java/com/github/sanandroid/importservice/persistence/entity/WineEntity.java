package com.github.sanandroid.importservice.persistence.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UpdateTimestamp;
import org.hibernate.type.SqlTypes;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Entity
@Table(name = "wines")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WineEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false, updatable = false, columnDefinition = "uuid")
    private UUID id;

    @JdbcTypeCode(SqlTypes.VECTOR)
    @Column(name = "embedding", columnDefinition = "vector(384)")
    private float[] embedding;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "winery_id", nullable = false)
    private WineryEntity winery;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "type")
    private String type;

    @Column(name = "region")
    private String region;

    @Column(name = "country")
    private String country;

    @ElementCollection
    private List<String> grapes;

    @Column(name = "alcohol_content")
    private BigDecimal alcoholContent;

    @Column(name = "vintage")
    private Integer vintage;

    @Column(name = "price")
    private BigDecimal price;

    @Column(name = "price_range")
    private String priceRange;

    @Column(name = "currency")
    private String currency;

    @Column(name = "description", columnDefinition = "text")
    private String description;

    @Column(name = "quality_level")
    private String qualityLevel;

    @Column(name = "shop_url", unique = true)
    private String shopUrl;

    @Column(name = "bottle_size")
    private String bottleSize;

    @Column(name = "average_rating")
    private BigDecimal averageRating;

    @Column(name = "number_of_ratings")
    private Integer numberOfRatings;

    @ElementCollection
    @MapKeyColumn(name = "critic_name")
    @Column(name = "score")
    private Map<String, BigDecimal> criticScores;

    @ElementCollection
    private List<String> foodPairings;

    @Column(name = "serving_temperature")
    private String servingTemperature;

    @Column(name = "availability_status")
    private String availabilityStatus;

    @Column(name = "sku")
    private String sku;

    @Column(name = "image_url")
    private String imageUrl;

    @ElementCollection
    private List<String> sourceUrls;

    @Column(name = "scraped_at")
    private String scrapedAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
