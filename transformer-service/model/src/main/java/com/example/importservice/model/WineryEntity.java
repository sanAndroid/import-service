package com.example.importservice.model;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

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
public record WineryEntity(

        @Id
        @GeneratedValue(strategy = GenerationType.UUID)
        @Column(name = "id", nullable = false, updatable = false, columnDefinition = "uuid")
        UUID id,

        @Column(name = "name", nullable = false)
        String name,

        @Column(name = "street")
        String street,

        @Column(name = "postal_city")
        String postalCity,

        @Column(name = "phone")
        String phone,

        @Column(name = "email")
        String email,

        @Column(name = "website", unique = true)
        String website,

        @Column(name = "opening_hours", columnDefinition = "text")
        String openingHours,

        @Column(name = "owners")
        String owners,

        @Column(name = "cellar_master")
        String cellarMaster,

        @Column(name = "hectares")
        String hectares,

        @Column(name = "varieties", columnDefinition = "text")
        String varieties,

        @Column(name = "geology", columnDefinition = "text")
        String geology,

        @Column(name = "region")
        String region,

        @Column(name = "features", columnDefinition = "text")
        String features,

        @Column(name = "sparkling")
        String sparkling,

        @Column(name = "memberships", columnDefinition = "text")
        String memberships,

        @Column(name = "organic_cert")
        String organicCert,

        @Column(name = "sustainability_cert")
        String sustainabilityCert,

        @Column(name = "lagen", columnDefinition = "text")
        String lagen,

        @Column(name = "source_url")
        String sourceUrl,

        @CreationTimestamp
        @Column(name = "created_at", nullable = false, updatable = false)
        Instant createdAt,

        @UpdateTimestamp
        @Column(name = "updated_at", nullable = false)
        Instant updatedAt
){}
