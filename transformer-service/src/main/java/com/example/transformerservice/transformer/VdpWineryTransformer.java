package com.example.transformerservice.transformer;

import com.example.transformerservice.model.ImportedWinery;
import com.example.transformerservice.model.VdpWinery;
import com.example.transformerservice.model.Winery;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformer implements AbstractWineryTransformer {

    @Override
    public Winery transform(ImportedWinery importedWinery) {
        VdpWinery vdpWinery = (VdpWinery) importedWinery;
        return new Winery(
            vdpWinery.name(),
            vdpWinery.street(),
            vdpWinery.postalCity(),
            vdpWinery.phone(),
            vdpWinery.email(),
            vdpWinery.website(),
            vdpWinery.openingHours(),
            vdpWinery.owners(),
            vdpWinery.cellarMaster(),
            vdpWinery.hectares(),
            vdpWinery.varieties(),
            vdpWinery.geology(),
            vdpWinery.region(),
            vdpWinery.features(),
            vdpWinery.sparkling(),
            vdpWinery.memberships(),
            vdpWinery.organicCert(),
            vdpWinery.sustainabilityCert(),
            vdpWinery.lagen(),
            vdpWinery.sourceUrl()
        );
    }
}
