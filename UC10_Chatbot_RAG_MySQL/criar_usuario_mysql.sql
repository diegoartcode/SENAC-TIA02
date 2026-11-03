-- Execute no MySQL Workbench ou phpMyAdmin como administrador.
-- Confirme primeiro o nome real do seu banco: lojatech1 ou lojatech.
-- Substitua a senha de exemplo antes de executar.
CREATE USER IF NOT EXISTS 'lojatech_leitura'@'localhost' IDENTIFIED BY 'TROQUE_POR_SENHA_FORTE';
GRANT SELECT ON lojatech1.pedidos TO 'lojatech_leitura'@'localhost';
-- Caso use o host 127.0.0.1 e o servidor não encontre o usuário,
-- pode ser necessário ajustar o host do usuário MySQL ao seu ambiente.
SHOW GRANTS FOR 'lojatech_leitura'@'localhost';
