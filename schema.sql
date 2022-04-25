-- id field does seem redundant for the example as one can use the natural key IP instead of the surrogate key ID

CREATE TABLE IF NOT EXISTS tr069server_device ( 
    id int NOT NULL AUTO_INCREMENT,
    ip VARCHAR(15) NOT NULL UNIQUE,
    customer_code VARCHAR(8) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS tr069server_provisioningstatus ( 
    ip VARCHAR(15) NOT NULL UNIQUE,
    status BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY(ip),
    FOREIGN KEY(ip) REFERENCES tr069server_device(ip) ON DELETE CASCADE
);

INSERT INTO tr069server_device(ip, customer_code) VALUES ("4.5.5.5","MAN001");
INSERT INTO tr069server_provisioningstatus(ip) VALUES ("4.5.5.5");

-- SELECT * FROM tr069server_provisioningstatus;
-- SELECT * FROM tr069server_device;

-- DROP TABLE IF EXISTS  tr069server_device;
-- DROP TABLE IF EXISTS  tr069server_provisioningstatus;