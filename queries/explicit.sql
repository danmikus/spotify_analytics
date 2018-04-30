SELECT
  playlist,
  SUM(CASE
      WHEN explicit = TRUE THEN 1
      ELSE 0 END)/count(*) AS explicit_perc,
  SUM(CASE
      WHEN explicit = FALSE THEN 1
      ELSE 0 END)/count(*) AS non_explicit_perc
FROM (
  SELECT
    "RapCaviar" AS playlist,
    explicit
  FROM
    `RapCaviar.tracks`
  UNION ALL
  SELECT
    "RockThis" AS playlist,
    explicit
  FROM
    `RockThis.tracks`
  UNION ALL
  SELECT
    "todays_top_hits" AS playlist,
    explicit
  FROM
    `todays_top_hits.tracks`)
GROUP BY
  1
