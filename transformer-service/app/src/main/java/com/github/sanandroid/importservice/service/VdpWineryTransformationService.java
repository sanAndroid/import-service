package com.github.sanandroid.importservice.service;

import com.github.sanandroid.importservice.model.VdpWinery;
import com.github.sanandroid.importservice.repository.WineryRepository;
import com.github.sanandroid.importservice.transformer.VdpWineryTransformer;
import org.springframework.stereotype.Service;

@Service
public class VdpWineryTransformationService extends AbstractWineryTransformationService<VdpWinery> {

    protected VdpWineryTransformationService(
            WineryRepository repository,
            VdpWineryTransformer transformer
    ) {
        super(repository, transformer);
    }

}