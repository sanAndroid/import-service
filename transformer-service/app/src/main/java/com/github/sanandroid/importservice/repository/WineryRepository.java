package com.github.sanandroid.importservice.repository;

import com.github.sanandroid.importservice.model.WineryEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface WineryRepository extends JpaRepository<WineryEntity, UUID> {
}
