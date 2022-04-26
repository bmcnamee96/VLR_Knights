SELECT vlr.player_name, vlr.team_abbreviation, COUNT(vlr.team_abbreviation)
FROM vlr_knights as vlr
GROUP BY (vlr.player_name, vlr.team_abbreviation)
ORDER BY COUNT(vlr.team_abbreviation) desc, vlr.team_abbreviation;

SELECT * FROM vlr_knights;