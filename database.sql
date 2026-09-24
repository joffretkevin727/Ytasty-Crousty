DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS restaurants CASCADE;

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    is_open BOOLEAN NOT NULL DEFAULT TRUE,
    opening_hours VARCHAR(100) NOT NULL,
    contact VARCHAR(50) NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(12) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'staff', 'direction')),
    restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE SET NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image TEXT NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    ingredients JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(64) UNIQUE NOT NULL,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    total_price NUMERIC(10, 2) NOT NULL CHECK (total_price >= 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'validated', 'preparing', 'ready', 'collected', 'cancelled')),
    pickup_mode VARCHAR(20) NOT NULL CHECK (pickup_mode IN ('onsite', 'takeaway')),
    customer JSONB NOT NULL
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0)
);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_restaurant ON products(restaurant_id);
CREATE INDEX idx_products_available ON products(is_available);
CREATE INDEX idx_orders_restaurant_status ON orders(restaurant_id, status);

INSERT INTO restaurants (id, name, city, address, is_open, opening_hours, contact) VALUES
(1, 'Ytasty Crousty Aix', 'Aix-en-Provence', '12 cours Mirabeau, 13100 Aix-en-Provence', TRUE, '11h30 - 23h00', '0442000001'),
(2, 'Ytasty Crousty Lyon', 'Lyon', '5 place Bellecour, 69002 Lyon', TRUE, '11h30 - 23h30', '0478000002'),
(3, 'Ytasty Crousty Paris', 'Paris', '45 rue de Rivoli, 75001 Paris', TRUE, '11h00 - 00h00', '0140000003');

SELECT setval('restaurants_id_seq', (SELECT MAX(id) FROM restaurants));

INSERT INTO users (id, first_name, last_name, username, password_hash, role, restaurant_id) VALUES
(1, 'Admin', 'Ytasty', 'admin123', '$2b$12$3xGSCqzSEGIoayvj3a/LTemxuDbADnQ1JDJYqHvxUr/aOpsddWqAa', 'admin', NULL);

SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

INSERT INTO products
    (id, name, image, description, category, price, is_available, restaurant_id, ingredients)
VALUES
    (1, 'Crousty Original', '/images/products/crousty-original.jpg',
     'Poulet croustillant, riz parfume et sauce maison.', 'chicken', 11.90, TRUE, 1,
     '["poulet", "riz", "sauce maison"]'::jsonb),
    (2, 'Crousty Epice', '/images/products/crousty-epice.jpg',
     'Poulet croustillant, riz et sauce epicee.', 'chicken', 12.50, TRUE, 1,
     '["poulet", "riz", "sauce epicee"]'::jsonb),
    (3, 'Tenders Box', '/images/products/tenders-box.jpg',
     'Tenders de poulet croustillants avec frites et sauce au choix.', 'chicken', 10.90, TRUE, 2,
     '["poulet", "frites", "sauce"]'::jsonb),
    (4, 'Crousty Lyonnais', '/images/products/crousty-lyonnais.jpg',
     'Poulet croustillant, riz, fromage et sauce maison.', 'chicken', 13.90, TRUE, 2,
     '["poulet", "riz", "fromage", "sauce maison"]'::jsonb),
    (5, 'Wrap Veggie', '/images/products/wrap-veggie.jpg',
     'Wrap aux legumes croquants et sauce yaourt.', 'vegetarian', 9.90, TRUE, 3,
     '["galette", "salade", "tomate", "sauce yaourt"]'::jsonb),
    (6, 'Frites Cheddar', '/images/products/frites-cheddar.jpg',
     'Frites croustillantes recouvertes de cheddar fondu.', 'side', 4.90, TRUE, 3,
     '["pommes de terre", "cheddar"]'::jsonb),
    (7, 'Crousty Family', '/images/products/crousty-family.jpg',
     'Format a partager avec poulet croustillant, riz et sauces.', 'menu', 28.90, FALSE, 1,
     '["poulet", "riz", "sauces"]'::jsonb),
    (8, 'Cookie Chocolat', '/images/products/cookie-chocolat.jpg',
     'Cookie moelleux aux pepites de chocolat.', 'dessert', 3.50, TRUE, 2,
     '["farine", "chocolat", "beurre"]'::jsonb),
    (9, 'The Glace Peche', '/images/products/the-glace-peche.jpg',
     'Boisson fraiche au the et a la peche.', 'drink', 2.90, TRUE, 3,
     '["the", "peche", "eau"]'::jsonb);

SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));