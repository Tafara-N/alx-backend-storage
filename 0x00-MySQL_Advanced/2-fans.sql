-- Script ranks country origins OF bands
-- ordered BY the number OF (non - UNIQUE) fans

SELECT DISTINCT `origin`, SUM(`fans`) AS `nb_fans` FROM `metal_bands`
GROUP BY `origin`
ORDER BY `nb_fans` DESC;
