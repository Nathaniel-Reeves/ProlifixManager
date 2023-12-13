CREATE USER 'client'@'%' IDENTIFIED BY 'ClientPassword!5';
GRANT ALL PRIVILEGES ON *.* TO 'client'@'%';
FLUSH PRIVILEGES;
-- CREATE USER 'dallasj'@'%' IDENTIFIED BY 'dallasjPassword!5';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'dallasj'@'%';
-- FLUSH PRIVILEGES;