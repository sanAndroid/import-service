package com.github.sanandroid.importservice.persistence.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.AllArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.UpdateTimestamp;
import org.hibernate.type.SqlTypes;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(
        name = "wineries",
        indexes = {
                @Index(name = "idx_winery_name_region", columnList = "name, region"),
                @Index(name = "uk_winery_website", columnList = "website", unique = true)
        }
)
@Getter
@Setter
@NoArgsConstructor // JPA requires a no-args constructor
@AllArgsConstructor
public class WineryEntity {

        @Id
        @GeneratedValue(strategy = GenerationType.UUID)
        @Column(name = "id", nullable = false, updatable = false, columnDefinition = "uuid")
        private UUID id;

        @JdbcTypeCode(SqlTypes.VECTOR)
        @Column(name = "embedding", columnDefinition = "vector(384)")
        private float[] embedding;

        @Column(name = "name", nullable = false)
        private String name;

        @Column(name = "street")
        private String street;

        @Column(name = "postal_city")
        private String postalCity;

        @Column(name = "phone")
        private String phone;

        @Column(name = "email")
        private String email;

        @Column(name = "website", unique = true)
        private String website;

        @Column(name = "opening_hours", columnDefinition = "text")
        private String openingHours;

        @Column(name = "owners")
        private String owners;

        @Column(name = "cellar_master")
        private String cellarMaster;

        @Column(name = "hectares")
        private String hectares;

        @Column(name = "varieties", columnDefinition = "text")
        private String varieties;

        @Column(name = "geology", columnDefinition = "text")
        private String geology;

        @Column(name = "region")
        private String region;

        @Column(name = "features", columnDefinition = "text")
        private String features;

        @Column(name = "sparkling")
        private String sparkling;

        @Column(name = "memberships", columnDefinition = "text")
        private String memberships;

        @Column(name = "organic_cert")
        private String organicCert;

        @Column(name = "sustainability_cert")
        private String sustainabilityCert;

        @Column(name = "lagen", columnDefinition = "text")
        private String lagen;

        @Column(name = "source_url")
        private String sourceUrl;

        @CreationTimestamp
        @Column(name = "created_at", nullable = false, updatable = false)
        private Instant createdAt;

        @UpdateTimestamp
        @Column(name = "updated_at", nullable = false)
        private Instant updatedAt;

}