package com.example.transformerservice.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public record Winery(
    @JsonProperty("name") String name,
    @JsonProperty("street") String street,
    @JsonProperty("postal_city") String postalCity,
    @JsonProperty("phone") String phone,
    @JsonProperty("email") String email,
    @JsonProperty("website") String website,
    @JsonProperty("opening_hours") String openingHours,
    @JsonProperty("owners") String owners,
    @JsonProperty("cellar_master") String cellarMaster,
    @JsonProperty("hectares") String hectares,
    @JsonProperty("varieties") String varieties,
    @JsonProperty("geology") String geology,
    @JsonProperty("region") String region,
    @JsonProperty("features") String features,
    @JsonProperty("sparkling") String sparkling,
    @JsonProperty("memberships") String memberships,
    @JsonProperty("organic_cert") String organicCert,
    @JsonProperty("sustain_cert") String sustainabilityCert,
    @JsonProperty("lagen") String lagen,
    @JsonProperty("source_url") String sourceUrl
) {}
