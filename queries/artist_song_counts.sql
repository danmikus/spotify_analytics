SELECT
  artist,
  COUNT(*) as song_count
FROM (
  SELECT
    artist
  FROM
    `RapCaviar.artists`
  UNION ALL
  SELECT
    artist
  FROM
    `RockThis.artists`
  UNION ALL
  SELECT
    artist
  FROM
    `todays_top_hits.artists`)
GROUP BY
  1
ORDER BY
  2 DESC
