SELECT
  artist,
  popularity,
  MAX(followers) as followers
FROM ((
    SELECT
      "RapCaviar" AS playlist,
      artist,
      popularity,
      MAX(followers) AS followers
    FROM
      `RapCaviar.artists`
    GROUP BY
      1,
      2,
      3)
  UNION ALL (
    SELECT
      "RockThis" AS playlist,
      artist,
      popularity,
      MAX(followers) AS followers
    FROM
      `RockThis.artists`
    GROUP BY
      1,
      2,
      3)
  UNION ALL (
    SELECT
      "todays_top_hits" AS playlist,
      artist,
      popularity,
      MAX(followers) AS followers
    FROM
      `todays_top_hits.artists`
    GROUP BY
      1,
      2,
      3))
GROUP BY
  1,
  2
ORDER BY
  2 DESC,
  3 DESC
