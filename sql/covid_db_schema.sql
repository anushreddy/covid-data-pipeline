CREATE TABLE IF NOT EXISTS covid_stats (
	id INT AUTO_INCREMENT PRIMARY KEY,
	city VARCHAR(255),
	province VARCHAR(255),
	country VARCHAR(255),
	keyId VARCHAR(255),
	confirmed INT,
	deaths SMALLINT,
	recovered SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastUpdate TIMESTAMP
);

select * from covid_stats;