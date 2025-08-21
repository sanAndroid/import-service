package com.example.importservice.service;

import com.example.importservice.model.VdpWinery;
import com.example.importservice.repository.WineryRepository;
import com.example.importservice.transformer.VdpWineryTransformer;
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