LOAD DATA INTO dataset.transactions FROM FILES(format='CSV', uris=['gs://bucket/transactions.csv']);
LOAD DATA INTO dataset.inventory_snapshots FROM FILES(format='CSV', uris=['gs://bucket/inventory_snapshots.csv']);
-- Repeat for remaining tables
