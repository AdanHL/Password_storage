SELECT * FROM accounts WHERE rowid=1
CREATE TABLE accounts(cuenta TEXT, plataforma TEXT, cont BLOB)
INSERT INTO accounts VALUES(?, ?, ?)
SELECT rowid, cuenta, plataforma FROM accounts
SELECT cuenta, plataforma, cont FROM accounts WHERE rowid = 
SELECT cuenta FROM accounts WHERE rowid = 
SELECT cont FROM accounts WHERE rowid = 
UPDATE accounts SET cuenta = ?, plataforma = ?, cont = ? WHERE rowid = ?
DELETE FROM accounts WHERE rowid =
