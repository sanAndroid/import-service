package com.github.sanandroid.importservice.transformer;

import com.github.sanandroid.importservice.model.winery.VdpWineryDto;
import com.github.sanandroid.importservice.model.winery.WineryMessage;
import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class VdpWineryTransformer implements AbstractWineryTransformer<VdpWineryDto> {

    @Override
    public WineryMessage transformToMessage(VdpWineryDto importedWinery) {
        return new WineryMessage(
                importedWinery.getName(),
                Optional.ofNullable(importedWinery.getWebsite())
                        .map(uri -> uri.getScheme() + "://" + uri.getHost())
                        .orElse(null)
        );
    }

    @Override
    public WineryEntity transformToEntity(VdpWineryDto importedWinery) {
        return new WineryEntity(
                null,
                null,
                importedWinery.getName(),
                importedWinery.getStreet(),
                importedWinery.getPostalCity(),
                importedWinery.getPhone(),
                importedWinery.getEmail(),
                importedWinery.getSourceUrl(),
                importedWinery.getOpeningHours(),
                importedWinery.getOwners(),
                importedWinery.getCellarMaster(),
                importedWinery.getHectares(),
                importedWinery.getVarieties(),
                importedWinery.getGeology(),
                importedWinery.getRegion(),
                importedWinery.getFeatures(),
                importedWinery.getSparkling(),
                importedWinery.getMemberships(),
                importedWinery.getOrganicCert(),
                importedWinery.getSustainabilityCert(),
                importedWinery.getLagen(),
                Optional.ofNullable(importedWinery.getWebsite())
                        .map(uri -> uri.getScheme() + "://" + uri.getHost())
                        .orElse(null),
                null,
                null
        );
    }
}
