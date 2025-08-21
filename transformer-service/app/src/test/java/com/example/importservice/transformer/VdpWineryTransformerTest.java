package com.example.importservice.transformer;

import com.example.importservice.model.VdpWinery;
import com.example.importservice.model.Winery;
import com.example.importservice.model.WineryEntity;
import com.github.javafaker.Faker;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class VdpWineryTransformerTest {

    private final VdpWineryTransformer transformer = new VdpWineryTransformer();
    private final Faker faker = new Faker();

    @Test
    void transform_shouldReturnWinery() {
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

        WineryEntity result = transformer.transform(vdpWinery);

        assertThat(result.name()).isEqualTo(vdpWinery.name());
        assertThat(result.street()).isEqualTo(vdpWinery.street());
        assertThat(result.postalCity()).isEqualTo(vdpWinery.postalCity());
        assertThat(result.phone()).isEqualTo(vdpWinery.phone());
        assertThat(result.email()).isEqualTo(vdpWinery.email());
        assertThat(result.website()).isEqualTo(vdpWinery.website());
        assertThat(result.openingHours()).isEqualTo(vdpWinery.openingHours());
        assertThat(result.owners()).isEqualTo(vdpWinery.owners());
        assertThat(result.cellarMaster()).isEqualTo(vdpWinery.cellarMaster());
        assertThat(result.hectares()).isEqualTo(vdpWinery.hectares());
        assertThat(result.varieties()).isEqualTo(vdpWinery.varieties());
        assertThat(result.geology()).isEqualTo(vdpWinery.geology());
        assertThat(result.region()).isEqualTo(vdpWinery.region());
        assertThat(result.features()).isEqualTo(vdpWinery.features());
        assertThat(result.sparkling()).isEqualTo(vdpWinery.sparkling());
        assertThat(result.memberships()).isEqualTo(vdpWinery.memberships());
        assertThat(result.organicCert()).isEqualTo(vdpWinery.organicCert());
        assertThat(result.sustainabilityCert()).isEqualTo(vdpWinery.sustainabilityCert());
        assertThat(result.lagen()).isEqualTo(vdpWinery.lagen());
        assertThat(result.sourceUrl()).isEqualTo(vdpWinery.sourceUrl());
    }
}