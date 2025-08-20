package com.example.transformerservice.transformer;

import com.example.transformerservice.model.VdpWinery;
import com.example.transformerservice.model.Winery;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformer implements AbstractWineryTransformer<VdpWinery> {

    @Override
    public Winery transform(VdpWinery importedWinery) {
        return new Winery(
            importedWinery.name(),
            importedWinery.street(),
            importedWinery.postalCity(),
            importedWinery.phone(),
            importedWinery.email(),
            importedWinery.website(),
            importedWinery.openingHours(),
            importedWinery.owners(),
            importedWinery.cellarMaster(),
            importedWinery.hectares(),
            importedWinery.varieties(),
            importedWinery.geology(),
            importedWinery.region(),
            importedWinery.features(),
            importedWinery.sparkling(),
            importedWinery.memberships(),
            importedWinery.organicCert(),
            importedWinery.sustainabilityCert(),
            importedWinery.lagen(),
            importedWinery.sourceUrl()
        );
    }
}
