package com.example.importservice.transformer;

import com.example.importservice.model.VdpWinery;
import com.example.importservice.model.Winery;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class VdpWineryTransformerTest {

    private final VdpWineryTransformer transformer = new VdpWineryTransformer();

    @Test
    void transform_shouldReturnWinery() {
        VdpWinery vdpWinery = new VdpWinery(
                "testName",
                "testStreet",
                "testPostalCity",
                "testPhone",
                "testEmail",
                "testWebsite",
                "testOpeningHours",
                "testOwners",
                "testCellarMaster",
                "testHectares",
                "testVarieties",
                "testGeology",
                "testRegion",
                "testFeatures",
                "testSparkling",
                "testMemberships",
                "testOrganicCert",
                "testSustainabilityCert",
                "testLagen",
                "testSourceUrl"
        );

        Winery result = transformer.transform(vdpWinery);

        assertThat(result.name()).isEqualTo("testName");
        assertThat(result.street()).isEqualTo("testStreet");
        assertThat(result.postalCity()).isEqualTo("testPostalCity");
        assertThat(result.phone()).isEqualTo("testPhone");
        assertThat(result.email()).isEqualTo("testEmail");
        assertThat(result.website()).isEqualTo("testWebsite");
        assertThat(result.openingHours()).isEqualTo("testOpeningHours");
        assertThat(result.owners()).isEqualTo("testOwners");
        assertThat(result.cellarMaster()).isEqualTo("testCellarMaster");
        assertThat(result.hectares()).isEqualTo("testHectares");
        assertThat(result.varieties()).isEqualTo("testVarieties");
        assertThat(result.geology()).isEqualTo("testGeology");
        assertThat(result.region()).isEqualTo("testRegion");
        assertThat(result.features()).isEqualTo("testFeatures");
        assertThat(result.sparkling()).isEqualTo("testSparkling");
        assertThat(result.memberships()).isEqualTo("testMemberships");
        assertThat(result.organicCert()).isEqualTo("testOrganicCert");
        assertThat(result.sustainabilityCert()).isEqualTo("testSustainabilityCert");
        assertThat(result.lagen()).isEqualTo("testLagen");
        assertThat(result.sourceUrl()).isEqualTo("testSourceUrl");
    }
}
