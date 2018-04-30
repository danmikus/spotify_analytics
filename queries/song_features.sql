SELECT
  playlist,
  ROUND(AVG(danceability), 3) AS danceability,
  ROUND(AVG(energy), 3) AS energy,
  ROUND(AVG(key), 3) AS key,
  ROUND(AVG(loudness), 3) AS loudness,
  ROUND(AVG(mode), 3) AS mode,
  ROUND(AVG(speechiness), 3) AS speechiness,
  ROUND(AVG(acousticness), 3) AS acousticness,
  ROUND(AVG(instrumentalness), 3) AS instrumentalness,
  ROUND(AVG(liveness), 3) AS liveness,
  ROUND(AVG(valence), 3) AS valence,
  ROUND(AVG(tempo), 3) AS tempo
FROM (
  SELECT
    *,
    "RapCaviar" AS playlist
  FROM
    RapCaviar.features
  UNION ALL
  SELECT
    *,
    "RockThis" AS playlist
  FROM
    RockThis.features
  UNION ALL
  SELECT
    *,
    "todays_top_hits" AS playlist
  FROM
    todays_top_hits.features)
GROUP BY
  1
