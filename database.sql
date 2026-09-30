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
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0)
);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_restaurant ON products(restaurant_id);
CREATE INDEX idx_products_available ON products(is_available);
CREATE INDEX idx_orders_restaurant_status ON orders(restaurant_id, status);

-- Les coordonnees ajoutees sont des donnees de demonstration.
INSERT INTO restaurants (id, name, city, address, is_open, opening_hours, contact) VALUES
(1, 'Tasty Crousty Aix', 'Aix-en-Provence', '25 rue du Colonel Sam, 13100 Aix-en-Provence', TRUE, '11h30 - 23h00', '04.50.21.70.87'),
(2, 'Tasty Crousty Lyon', 'Lyon', '18 avenue des Tenders, 69002 Lyon', TRUE, '11h30 - 23h30', '04.50.21.70.88'),
(3, 'Tasty Crousty Paris', 'Paris', '7 place du Crousty, 75001 Paris', TRUE, '11h00 - 00h00', '01.40.21.70.89'),
(4, 'Tasty Crousty Marseille', 'Marseille', '42 rue du Poulet Dore, 13001 Marseille', TRUE, '11h30 - 23h00', '04.91.21.70.90'),
(5, 'Tasty Crousty Toulouse', 'Toulouse', '9 boulevard Sauce Maison, 31000 Toulouse', TRUE, '11h30 - 23h00', '05.61.21.70.91'),
(6, 'Tasty Crousty Bordeaux', 'Bordeaux', '31 rue du Riz Croustillant, 33000 Bordeaux', TRUE, '11h30 - 23h00', '05.56.21.70.92'),
(7, 'Tasty Crousty Lille', 'Lille', '14 avenue des Frites, 59000 Lille', TRUE, '11h30 - 23h00', '03.20.21.70.93'),
(8, 'Tasty Crousty Nice', 'Nice', '6 rue des Tenders, 06000 Nice', TRUE, '11h30 - 23h00', '04.93.21.70.94'),
(9, 'Tasty Crousty Nantes', 'Nantes', '22 place du Crousty, 44000 Nantes', TRUE, '11h30 - 23h00', '02.40.21.70.95'),
(10, 'Tasty Crousty Montpellier', 'Montpellier', '3 boulevard du Colonel Sam, 34000 Montpellier', TRUE, '11h30 - 23h00', '04.67.21.70.96');

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
     'Tenders de poulet croustillants avec frites et sauce au choix.', 'chicken', 10.90, TRUE, 1,
     '["poulet", "frites", "sauce"]'::jsonb),
    (4, 'Crousty Signature', '/images/products/crousty-signature.jpg',
     'Poulet croustillant, riz, oignons frits et sauce signature.', 'chicken', 13.90, TRUE, 2,
     '["poulet", "riz", "oignons frits", "sauce signature"]'::jsonb),
    (5, 'Frites Cheddar', '/images/products/frites-cheddar.jpg',
     'Frites croustillantes recouvertes de cheddar fondu.', 'side', 4.90, TRUE, 2,
     '["pommes de terre", "cheddar"]'::jsonb),
    (6, 'Tenders Box', '/images/products/tenders-box.jpg',
     'Tenders de poulet croustillants avec frites et sauce au choix.', 'chicken', 10.90, TRUE, 2,
     '["poulet", "frites", "sauce"]'::jsonb),
    (7, 'Wrap Veggie', '/images/products/wrap-veggie.jpg',
     'Wrap aux legumes croquants et sauce yaourt.', 'vegetarian', 9.90, TRUE, 3,
     '["galette", "salade", "tomate", "sauce yaourt"]'::jsonb),
    (8, 'Crousty Family', '/images/products/crousty-family.jpg',
     'Format a partager avec poulet croustillant, riz et sauces.', 'menu', 28.90, FALSE, 3,
     '["poulet", "riz", "sauces"]'::jsonb),
    (9, 'Cookie Chocolat', '/images/products/cookie-chocolat.jpg',
     'Cookie moelleux aux pepites de chocolat.', 'dessert', 3.50, TRUE, 3,
     '["farine", "chocolat", "beurre"]'::jsonb),
    (10, 'Crousty Original', '/images/products/crousty-original.jpg',
     'Poulet croustillant, riz parfume et sauce maison.', 'chicken', 11.90, TRUE, 4,
     '["poulet", "riz", "sauce maison"]'::jsonb),
    (11, 'Crousty Epice', '/images/products/crousty-epice.jpg',
     'Poulet croustillant, riz et sauce epicee.', 'chicken', 12.50, TRUE, 4,
     '["poulet", "riz", "sauce epicee"]'::jsonb),
    (12, 'The Glace Peche', '/images/products/the-glace-peche.jpg',
     'Boisson fraiche au the et a la peche.', 'drink', 2.90, TRUE, 4,
     '["the", "peche", "eau"]'::jsonb),
    (13, 'Crousty Lyonnais', '/images/products/crousty-lyonnais.jpg',
     'Poulet croustillant, riz, fromage et sauce maison.', 'chicken', 13.90, TRUE, 5,
     '["poulet", "riz", "fromage", "sauce maison"]'::jsonb),
    (14, 'Tenders Box', '/images/products/tenders-box.jpg',
     'Tenders de poulet croustillants avec frites et sauce au choix.', 'chicken', 10.90, TRUE, 5,
     '["poulet", "frites", "sauce"]'::jsonb),
    (15, 'Frites Cheddar', '/images/products/frites-cheddar.jpg',
     'Frites croustillantes recouvertes de cheddar fondu.', 'side', 4.90, TRUE, 5,
     '["pommes de terre", "cheddar"]'::jsonb),
    (16, 'Crousty Original', '/images/products/crousty-original.jpg',
     'Poulet croustillant, riz parfume et sauce maison.', 'chicken', 11.90, TRUE, 6,
     '["poulet", "riz", "sauce maison"]'::jsonb),
    (17, 'Wrap Veggie', '/images/products/wrap-veggie.jpg',
     'Wrap aux legumes croquants et sauce yaourt.', 'vegetarian', 9.90, TRUE, 6,
     '["galette", "salade", "tomate", "sauce yaourt"]'::jsonb),
    (18, 'Cookie Chocolat', '/images/products/cookie-chocolat.jpg',
     'Cookie moelleux aux pepites de chocolat.', 'dessert', 3.50, TRUE, 6,
     '["farine", "chocolat", "beurre"]'::jsonb),
    (19, 'Crousty Epice', '/images/products/crousty-epice.jpg',
     'Poulet croustillant, riz et sauce epicee.', 'chicken', 12.50, TRUE, 7,
     '["poulet", "riz", "sauce epicee"]'::jsonb),
    (20, 'Crousty Family', '/images/products/crousty-family.jpg',
     'Format a partager avec poulet croustillant, riz et sauces.', 'menu', 28.90, FALSE, 7,
     '["poulet", "riz", "sauces"]'::jsonb),
    (21, 'Tenders Box', '/images/products/tenders-box.jpg',
     'Tenders de poulet croustillants avec frites et sauce au choix.', 'chicken', 10.90, TRUE, 7,
     '["poulet", "frites", "sauce"]'::jsonb),
    (22, 'Crousty Original', '/images/products/crousty-original.jpg',
     'Poulet croustillant, riz parfume et sauce maison.', 'chicken', 11.90, TRUE, 8,
     '["poulet", "riz", "sauce maison"]'::jsonb),
    (23, 'Crousty Epice', '/images/products/crousty-epice.jpg',
     'Poulet croustillant, riz et sauce epicee.', 'chicken', 12.50, TRUE, 8,
     '["poulet", "riz", "sauce epicee"]'::jsonb),
    (24, 'The Glace Peche', '/images/products/the-glace-peche.jpg',
     'Boisson fraiche au the et a la peche.', 'drink', 2.90, TRUE, 8,
     '["the", "peche", "eau"]'::jsonb),
    (25, 'Crousty Lyonnais', '/images/products/crousty-lyonnais.jpg',
     'Poulet croustillant, riz, fromage et sauce maison.', 'chicken', 13.90, TRUE, 9,
     '["poulet", "riz", "fromage", "sauce maison"]'::jsonb),
    (26, 'Tenders Box', '/images/products/tenders-box.jpg',
     'Tenders de poulet croustillants avec frites et sauce au choix.', 'chicken', 10.90, TRUE, 9,
     '["poulet", "frites", "sauce"]'::jsonb),
    (27, 'Frites Cheddar', '/images/products/frites-cheddar.jpg',
     'Frites croustillantes recouvertes de cheddar fondu.', 'side', 4.90, TRUE, 9,
     '["pommes de terre", "cheddar"]'::jsonb),
    (28, 'Crousty Original', '/images/products/crousty-original.jpg',
     'Poulet croustillant, riz parfume et sauce maison.', 'chicken', 11.90, TRUE, 10,
     '["poulet", "riz", "sauce maison"]'::jsonb),
    (29, 'Wrap Veggie', '/images/products/wrap-veggie.jpg',
     'Wrap aux legumes croquants et sauce yaourt.', 'vegetarian', 9.90, TRUE, 10,
     '["galette", "salade", "tomate", "sauce yaourt"]'::jsonb),
    (30, 'Cookie Chocolat', '/images/products/cookie-chocolat.jpg',
     'Cookie moelleux aux pepites de chocolat.', 'dessert', 3.50, TRUE, 10,
     '["farine", "chocolat", "beurre"]'::jsonb);

SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));

INSERT INTO orders (id, order_number, restaurant_id, total_price, status, pickup_mode, customer) VALUES
(1, 'order_00001', 1, 11.90, 'ready', 'takeaway', '{"name": "Camille Martin", "email": "camille.martin@example.com"}'::jsonb),
(2, 'order_00002', 1, 12.50, 'preparing', 'onsite', '{"name": "Nolan Petit", "email": "nolan.petit@example.com"}'::jsonb),
(3, 'order_00003', 2, 13.90, 'collected', 'takeaway', '{"name": "Lea Bernard", "email": "lea.bernard@example.com"}'::jsonb),
(4, 'order_00004', 2, 4.90, 'validated', 'onsite', '{"name": "Hugo Robert", "email": "hugo.robert@example.com"}'::jsonb),
(5, 'order_00005', 3, 9.90, 'pending', 'takeaway', '{"name": "Ines Moreau", "email": "ines.moreau@example.com"}'::jsonb),
(6, 'order_00006', 3, 3.50, 'cancelled', 'onsite', '{"name": "Adam Laurent", "email": "adam.laurent@example.com"}'::jsonb),
(7, 'order_00007', 4, 11.90, 'ready', 'takeaway', '{"name": "Sarah Roux", "email": "sarah.roux@example.com"}'::jsonb),
(8, 'order_00008', 4, 12.50, 'preparing', 'onsite', '{"name": "Ethan Vincent", "email": "ethan.vincent@example.com"}'::jsonb),
(9, 'order_00009', 5, 13.90, 'collected', 'takeaway', '{"name": "Jade Fournier", "email": "jade.fournier@example.com"}'::jsonb),
(10, 'order_00010', 5, 10.90, 'validated', 'onsite', '{"name": "Noah Girard", "email": "noah.girard@example.com"}'::jsonb),
(11, 'order_00011', 6, 11.90, 'pending', 'takeaway', '{"name": "Emma Andre", "email": "emma.andre@example.com"}'::jsonb),
(12, 'order_00012', 6, 9.90, 'ready', 'onsite', '{"name": "Louis Mercier", "email": "louis.mercier@example.com"}'::jsonb),
(13, 'order_00013', 7, 12.50, 'preparing', 'takeaway', '{"name": "Lina Lambert", "email": "lina.lambert@example.com"}'::jsonb),
(14, 'order_00014', 7, 10.90, 'collected', 'onsite', '{"name": "Malo Bonnet", "email": "malo.bonnet@example.com"}'::jsonb),
(15, 'order_00015', 8, 11.90, 'validated', 'takeaway', '{"name": "Anna Francois", "email": "anna.francois@example.com"}'::jsonb),
(16, 'order_00016', 8, 12.50, 'pending', 'onsite', '{"name": "Rayan Garnier", "email": "rayan.garnier@example.com"}'::jsonb),
(17, 'order_00017', 9, 13.90, 'ready', 'takeaway', '{"name": "Mia Faure", "email": "mia.faure@example.com"}'::jsonb),
(18, 'order_00018', 9, 10.90, 'preparing', 'onsite', '{"name": "Sacha Rousseau", "email": "sacha.rousseau@example.com"}'::jsonb),
(19, 'order_00019', 10, 11.90, 'collected', 'takeaway', '{"name": "Lola Vincent", "email": "lola.vincent@example.com"}'::jsonb),
(20, 'order_00020', 10, 9.90, 'validated', 'onsite', '{"name": "Eli Simon", "email": "eli.simon@example.com"}'::jsonb);

SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 11.90), (2, 2, 1, 12.50),
(3, 4, 1, 13.90), (4, 5, 1, 4.90),
(5, 7, 1, 9.90), (6, 9, 1, 3.50),
(7, 10, 1, 11.90), (8, 11, 1, 12.50),
(9, 13, 1, 13.90), (10, 14, 1, 10.90),
(11, 16, 1, 11.90), (12, 17, 1, 9.90),
(13, 19, 1, 12.50), (14, 21, 1, 10.90),
(15, 22, 1, 11.90), (16, 23, 1, 12.50),
(17, 25, 1, 13.90), (18, 26, 1, 10.90),
(19, 28, 1, 11.90), (20, 29, 1, 9.90);

SELECT setval('order_items_id_seq', (SELECT MAX(id) FROM order_items));