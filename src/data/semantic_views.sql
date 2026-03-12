CREATE OR REPLACE VIEW semantic_sales_daily AS
SELECT t.date, c.region, t.business_unit, t.club_id, t.product_id, SUM(t.units) AS units_sold, SUM(t.net_sales) AS net_sales
FROM transactions t JOIN club_master c USING (club_id)
GROUP BY 1,2,3,4,5;

CREATE OR REPLACE VIEW semantic_sales_enriched AS
SELECT s.*, p.product_name, p.category
FROM semantic_sales_daily s JOIN product_master p USING (product_id);

CREATE OR REPLACE VIEW semantic_inventory_health AS
SELECT i.date, i.club_id, i.product_id, i.on_hand_units, s.units_sold,
CASE WHEN i.on_hand_units < 20 THEN 'risk' ELSE 'healthy' END AS inventory_status,
c.region, i.business_unit
FROM inventory_snapshots i
LEFT JOIN semantic_sales_daily s ON i.date = s.date AND i.club_id = s.club_id AND i.product_id = s.product_id
JOIN club_master c USING (club_id);

CREATE OR REPLACE VIEW semantic_promo_effectiveness AS
SELECT p.promo_id, p.product_id, p.promo_type, p.start_date, p.end_date,
AVG(s.net_sales) AS avg_daily_sales_during_promo
FROM promotions p
LEFT JOIN semantic_sales_daily s ON s.product_id = p.product_id
AND s.date BETWEEN p.start_date AND p.end_date
GROUP BY 1,2,3,4,5;

CREATE OR REPLACE VIEW semantic_kpi_daily AS
SELECT s.date, s.region, s.business_unit,
SUM(s.net_sales) AS total_net_sales,
SUM(r.return_units)::DOUBLE / NULLIF(SUM(s.units_sold),0) AS return_rate
FROM semantic_sales_daily s
LEFT JOIN returns r ON s.date = r.date AND s.club_id = r.club_id AND s.product_id = r.product_id
GROUP BY 1,2,3;

CREATE OR REPLACE VIEW semantic_metric_dictionary AS
SELECT * FROM metric_dictionary;
