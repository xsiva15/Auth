-- Подключаем расширение для генерации UUID (через pgcrypto)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Создаём схему, если ещё нет
CREATE SCHEMA IF NOT EXISTS asclavia_schema;

-- Создаём таблицу users, если ещё не существует

--CREATE TABLE IF NOT EXISTS asclavia_schema.users (
--    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
--    username VARCHAR(255) NOT NULL,
--    password_hash VARCHAR(255) NOT NULL,
--    email VARCHAR(255) NOT NULL,
 --   created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
--    is_active BOOLEAN DEFAULT TRUE,
--    phone_number VARCHAR(20)
--);

