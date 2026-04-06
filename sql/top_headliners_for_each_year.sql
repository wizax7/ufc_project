WITH headers AS (
    SELECT 
        SPLIT_PART(name, ':', 2) AS header, 
        EXTRACT(YEAR FROM date) AS year
    FROM ufc_events
), 
headlining_fighers AS (
    SELECT TRIM(
        REGEXP_REPLACE(
            REGEXP_SPLIT_TO_TABLE(header, '\s+(vs\.|vs|v\.)\s+', 'i'), 
            '\s+\d+$', ''
        )
    ) AS headliner, 
    year
    FROM headers
)

SELECT 
    headliner, 
    year, 
    COUNT(*) AS main_event_count
FROM headlining_fighers
WHERE headliner <> ''
GROUP BY headliner, year
HAVING COUNT(*) > 1
ORDER BY year DESC, main_event_count DESC, headliner ASC