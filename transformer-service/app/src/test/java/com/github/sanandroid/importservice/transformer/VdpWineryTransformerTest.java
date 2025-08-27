package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.winery.VdpWinery;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.javafaker.Faker;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class VdpWineryTransformerTest {

    private final VdpWineryTransformer transformer = new VdpWineryTransformer();
    private final Faker faker = new Faker();

    @Test
    void transform_ToEntity_shouldReturnWinery() {
        VdpWinery vdpWinery = new VdpWinery(
                faker.company().name(),
                faker.address().streetAddress(),
                faker.address().city(),
                faker.phoneNumber().phoneNumber(),
                faker.internet().emailAddress(),
                faker.internet().url(),
                faker.lorem().sentence(),
                faker.name().fullName(),
                faker.name().fullName(),
                faker.number().digit(),
                faker.lorem().word(),
                faker.lorem().word(),
                faker.address().state(),
                faker.lorem().word(),
                faker.lorem().word(),
                faker.lorem().word(),
                faker.lorem().word(),
                faker.lorem().word(),
                faker.lorem().word(),
                faker.internet().url()
        );

        WineryEntity result = transformer.transformToEntity(vdpWinery);

        assertThat(result.getName()).isEqualTo(vdpWinery.name());
        assertThat(result.getStreet()).isEqualTo(vdpWinery.street());
        assertThat(result.getPostalCity()).isEqualTo(vdpWinery.postalCity());
        assertThat(result.getPhone()).isEqualTo(vdpWinery.phone());
        assertThat(result.getEmail()).isEqualTo(vdpWinery.email());
        assertThat(result.getWebsite()).isEqualTo(vdpWinery.website());
        assertThat(result.getOpeningHours()).isEqualTo(vdpWinery.openingHours());
        assertThat(result.getOwners()).isEqualTo(vdpWinery.owners());
        assertThat(result.getCellarMaster()).isEqualTo(vdpWinery.cellarMaster());
        assertThat(result.getHectares()).isEqualTo(vdpWinery.hectares());
        assertThat(result.getVarieties()).isEqualTo(vdpWinery.varieties());
        assertThat(result.getGeology()).isEqualTo(vdpWinery.geology());
        assertThat(result.getRegion()).isEqualTo(vdpWinery.region());
        assertThat(result.getFeatures()).isEqualTo(vdpWinery.features());
        assertThat(result.getSparkling()).isEqualTo(vdpWinery.sparkling());
        assertThat(result.getMemberships()).isEqualTo(vdpWinery.memberships());
        assertThat(result.getOrganicCert()).isEqualTo(vdpWinery.organicCert());
        assertThat(result.getSustainabilityCert()).isEqualTo(vdpWinery.sustainabilityCert());
        assertThat(result.getLagen()).isEqualTo(vdpWinery.lagen());
        assertThat(result.getSourceUrl()).isEqualTo(vdpWinery.sourceUrl());
    }
}