WITH headers AS (
    SELECT SPLIT_PART(name, ':', 2) AS header
    FROM ufc_events
    ),
    headlining_fighters AS (
        SELECT TRIM(
            REGEXP_REPLACE(
                REGEXP_SPLIT_TO_TABLE(header, '\s+(vs\.|vs|v\.)\s+', 'i'), 
                '\s+\d+$', ''
            )
        ) AS headliner
        FROM headers
    )

SELECT 
    headliner, 
    COUNT(*) AS main_event_count
FROM headlining_fighters
WHERE headliner <> ''
GROUP BY headliner
ORDER BY 2 DESC
LIMIT 10;