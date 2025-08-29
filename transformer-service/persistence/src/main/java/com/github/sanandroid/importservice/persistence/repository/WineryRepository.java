package com.github.sanandroid.importservice.persistence.repository;

import com.github.sanandroid.importservice.persistence.entity.WineryEntity;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface WineryRepository extends JpaRepository<WineryEntity, UUID> {


    @Modifying
    @Transactional
    @Query(value = """
            INSERT INTO wineries (
              id, name, website, source_url, email, phone, street, postal_city, region,
              owners, cellar_master, opening_hours, memberships, organic_cert, sustainability_cert,
              features, geology, hectares, lagen, varieties, sparkling, embedding, created_at, updated_at
            ) VALUES (
              COALESCE(:#{#w.id}, gen_random_uuid()), :#{#w.name}, :#{#w.website}, :#{#w.sourceUrl},
              :#{#w.email}, :#{#w.phone}, :#{#w.street}, :#{#w.postalCity}, :#{#w.region},
              :#{#w.owners}, :#{#w.cellarMaster}, :#{#w.openingHours}, :#{#w.memberships},
              :#{#w.organicCert}, :#{#w.sustainabilityCert}, :#{#w.features}, :#{#w.geology},
              :#{#w.hectares}, :#{#w.lagen}, :#{#w.varieties}, :#{#w.sparkling},
              CAST(:#{#w.embedding} AS vector), NOW(), NOW()
            )
            ON CONFLICT (website) DO UPDATE SET
              name                = EXCLUDED.name,
              source_url          = EXCLUDED.source_url,
              email               = EXCLUDED.email,
              phone               = EXCLUDED.phone,
              street              = EXCLUDED.street,
              postal_city         = EXCLUDED.postal_city,
              region              = EXCLUDED.region,
              owners              = EXCLUDED.owners,
              cellar_master       = EXCLUDED.cellar_master,
              opening_hours       = EXCLUDED.opening_hours,
              memberships         = EXCLUDED.memberships,
              organic_cert        = EXCLUDED.organic_cert,
              sustainability_cert = EXCLUDED.sustainability_cert,
              features            = EXCLUDED.features,
              geology             = EXCLUDED.geology,
              hectares            = EXCLUDED.hectares,
              lagen               = EXCLUDED.lagen,
              varieties           = EXCLUDED.varieties,
              sparkling           = EXCLUDED.sparkling,
              embedding           = EXCLUDED.embedding,
              updated_at          = NOW()
            """, nativeQuery = true)
    int upsert(@Param("w") WineryEntity w);

    @Modifying
    @Transactional
    @Query(value = """
            INSERT INTO wineries (
              id, name, website, source_url, email, phone, street, postal_city, region,
              owners, cellar_master, opening_hours, memberships, organic_cert, sustainability_cert,
              features, geology, hectares, lagen, varieties, sparkling, embedding, created_at, updated_at
            ) VALUES (
              COALESCE(:#{#w.id}, gen_random_uuid()), :#{#w.name}, :#{#w.website}, :#{#w.sourceUrl},
              :#{#w.email}, :#{#w.phone}, :#{#w.street}, :#{#w.postalCity}, :#{#w.region},
              :#{#w.owners}, :#{#w.cellarMaster}, :#{#w.openingHours}, :#{#w.memberships},
              :#{#w.organicCert}, :#{#w.sustainabilityCert}, :#{#w.features}, :#{#w.geology},
              :#{#w.hectares}, :#{#w.lagen}, :#{#w.varieties}, :#{#w.sparkling},
              CAST(:#{#w.embedding} AS vector), NOW(), NOW()
            )
            ON CONFLICT (website) DO NOTHING
            """, nativeQuery = true)
    int insertIfNotExists(@Param("w") WineryEntity w);

    Optional<WineryEntity> findByName(String name);

    Optional<WineryEntity> findByWebsite(String website);
}
