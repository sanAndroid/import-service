package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.winery.VdpWineryDto;
import com.github.sanandroid.importservice.model.winery.WineryMessage;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformer implements AbstractWineryTransformer<VdpWineryDto> {

    @Override
    public WineryMessage transformToMessage(VdpWineryDto importedWinery) {
        return new WineryMessage(
                importedWinery.name(),
                importedWinery.website()
        );
    }

    @Override
    public WineryEntity transformToEntity(VdpWineryDto importedWinery) {
        return new WineryEntity(
                null,
                null,
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
                importedWinery.sourceUrl(),
                null,
                null
        );
    }
}
