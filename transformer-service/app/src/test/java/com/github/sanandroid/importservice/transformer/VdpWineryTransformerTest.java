package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.winery.VdpWineryDto;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import com.github.javafaker.Faker;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class VdpWineryTransformerTest {

    private final VdpWineryTransformer transformer = new VdpWineryTransformer();
    private final Faker faker = new Faker();

    @Test
    void transform_ToEntity_shouldReturnWinery() {
        VdpWineryDto vdpWineryDto = new VdpWineryDto(
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

        WineryEntity result = transformer.transformToEntity(vdpWineryDto);

        assertThat(result.getName()).isEqualTo(vdpWineryDto.name());
        assertThat(result.getStreet()).isEqualTo(vdpWineryDto.street());
        assertThat(result.getPostalCity()).isEqualTo(vdpWineryDto.postalCity());
        assertThat(result.getPhone()).isEqualTo(vdpWineryDto.phone());
        assertThat(result.getEmail()).isEqualTo(vdpWineryDto.email());
        assertThat(result.getWebsite()).isEqualTo(vdpWineryDto.website());
        assertThat(result.getOpeningHours()).isEqualTo(vdpWineryDto.openingHours());
        assertThat(result.getOwners()).isEqualTo(vdpWineryDto.owners());
        assertThat(result.getCellarMaster()).isEqualTo(vdpWineryDto.cellarMaster());
        assertThat(result.getHectares()).isEqualTo(vdpWineryDto.hectares());
        assertThat(result.getVarieties()).isEqualTo(vdpWineryDto.varieties());
        assertThat(result.getGeology()).isEqualTo(vdpWineryDto.geology());
        assertThat(result.getRegion()).isEqualTo(vdpWineryDto.region());
        assertThat(result.getFeatures()).isEqualTo(vdpWineryDto.features());
        assertThat(result.getSparkling()).isEqualTo(vdpWineryDto.sparkling());
        assertThat(result.getMemberships()).isEqualTo(vdpWineryDto.memberships());
        assertThat(result.getOrganicCert()).isEqualTo(vdpWineryDto.organicCert());
        assertThat(result.getSustainabilityCert()).isEqualTo(vdpWineryDto.sustainabilityCert());
        assertThat(result.getLagen()).isEqualTo(vdpWineryDto.lagen());
        assertThat(result.getSourceUrl()).isEqualTo(vdpWineryDto.sourceUrl());
    }
}