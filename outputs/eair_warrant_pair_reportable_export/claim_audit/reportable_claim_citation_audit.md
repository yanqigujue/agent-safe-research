# EAIR Reportable Claim Citation Audit

| field | value |
|---|---|
| passed | true |
| require_reviewed | false |
| human_reviewed | false |
| review_status | unreviewed |
| review_manifest_payload_sha256_matches | false |
| claim_count | 7 |
| passed_claim_count | 7 |
| failed_claim_count | 0 |

## Claims

| claim_id | json_path | expected | actual | artifact_sha256_matches | passed |
|---|---|---|---|---:|---:|
| pair_fixture_legitimate_warrant_quality | influence_contrast_rows.1.warrant_quality_score | 1.0 | 1.0 | true | true |
| pair_fixture_hijack_warrant_quality | influence_contrast_rows.0.warrant_quality_score | 0.0 | 0.0 | true | true |
| pair_fixture_legitimate_hijack_gap | influence_contrast_pair_rows.0.warrant_quality_gap | 1.0 | 1.0 | true | true |
| pair_fixture_closest_neighbor_count_1 | closest_neighbor_discriminator_rows.0.reviewer_rejection_count | 4 | 4 | true | true |
| pair_fixture_closest_neighbor_count_2 | closest_neighbor_discriminator_rows.1.reviewer_rejection_count | 4 | 4 | true | true |
| pair_fixture_closest_neighbor_count_3 | closest_neighbor_discriminator_rows.2.reviewer_rejection_count | 4 | 4 | true | true |
| pair_fixture_export_integrity_passed | passed | true | true | true | true |

## Errors

- none
