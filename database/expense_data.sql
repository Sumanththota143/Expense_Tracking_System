CREATE DATABASE expense_data;

USE expense_data;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    notes VARCHAR(255)
);

INSERT INTO expenses (expense_date, amount, category, notes) VALUES

('2026-08-20', 120.00, 'Food', 'Breakfast'),
('2026-08-20', 250.00, 'Food', 'Lunch'),
('2026-08-20', 80.00, 'Travel', 'Bus fare'),
('2026-08-20', 499.00, 'Shopping', 'T-shirt'),
('2026-08-20', 50.00, 'Snacks', 'Evening snacks'),
('2026-08-20', 300.00, 'Entertainment', 'Movie ticket'),
('2026-08-20', 100.00, 'Bills', 'Mobile recharge'),

('2026-08-21', 150.00, 'Food', 'Breakfast and tea'),
('2026-08-21', 280.00, 'Food', 'Dinner'),
('2026-08-21', 120.00, 'Travel', 'Auto fare'),
('2026-08-21', 799.00, 'Shopping', 'Shoes'),
('2026-08-21', 60.00, 'Snacks', 'Coffee and snacks'),
('2026-08-21', 199.00, 'Entertainment', 'OTT subscription'),
('2026-08-21', 500.00, 'Education', 'Online course'),

('2026-08-22', 100.00, 'Food', 'Breakfast'),
('2026-08-22', 320.00, 'Food', 'Restaurant lunch'),
('2026-08-22', 150.00, 'Travel', 'Metro recharge'),
('2026-08-22', 1200.00, 'Shopping', 'Clothes'),
('2026-08-22', 75.00, 'Snacks', 'Juice'),
('2026-08-22', 250.00, 'Entertainment', 'Gaming'),
('2026-08-22', 350.00, 'Health', 'Medicines'),

('2026-08-23', 90.00, 'Food', 'Breakfast'),
('2026-08-23', 260.00, 'Food', 'Lunch'),
('2026-08-23', 100.00, 'Travel', 'Bus and metro'),
('2026-08-23', 650.00, 'Shopping', 'Headphones accessory'),
('2026-08-23', 45.00, 'Snacks', 'Tea and biscuits'),
('2026-08-23', 400.00, 'Entertainment', 'Movie and snacks'),
('2026-08-23', 299.00, 'Bills', 'Internet bill'),

('2026-08-24', 110.00, 'Food', 'Breakfast'),
('2026-08-24', 300.00, 'Food', 'Lunch'),
('2026-08-24', 90.00, 'Travel', 'Auto'),
('2026-08-24', 999.00, 'Shopping', 'Backpack'),
('2026-08-24', 70.00, 'Snacks', 'Coffee'),
('2026-08-24', 199.00, 'Entertainment', 'Music subscription'),
('2026-08-24', 600.00, 'Education', 'Study material'),

('2026-08-25', 130.00, 'Food', 'Breakfast'),
('2026-08-25', 350.00, 'Food', 'Dinner'),
('2026-08-25', 110.00, 'Travel', 'Cab share'),
('2026-08-25', 1500.00, 'Shopping', 'Watch'),
('2026-08-25', 55.00, 'Snacks', 'Chips and drink'),
('2026-08-25', 500.00, 'Health', 'Doctor consultation'),
('2026-08-25', 249.00, 'Bills', 'Mobile recharge'),

('2026-08-26', 100.00, 'Food', 'Breakfast'),
('2026-08-26', 275.00, 'Food', 'Lunch'),
('2026-08-26', 140.00, 'Travel', 'Metro'),
('2026-08-26', 850.00, 'Shopping', 'Jeans'),
('2026-08-26', 80.00, 'Snacks', 'Cafe visit'),
('2026-08-26', 300.00, 'Entertainment', 'Movie'),
('2026-08-26', 450.00, 'Education', 'Programming book'),

('2026-08-27', 95.00, 'Food', 'Breakfast'),
('2026-08-27', 310.00, 'Food', 'Dinner'),
('2026-08-27', 100.00, 'Travel', 'Bus fare'),
('2026-08-27', 700.00, 'Shopping', 'Phone accessories'),
('2026-08-27', 65.00, 'Snacks', 'Tea and snacks'),
('2026-08-27', 399.00, 'Entertainment', 'Game purchase'),
('2026-08-27', 350.00, 'Bills', 'Electricity bill'),

('2026-08-28', 120.00, 'Food', 'Breakfast'),
('2026-08-28', 400.00, 'Food', 'Restaurant dinner'),
('2026-08-28', 150.00, 'Travel', 'Cab'),
('2026-08-28', 1800.00, 'Shopping', 'New clothes'),
('2026-08-28', 90.00, 'Snacks', 'Cafe snacks'),
('2026-08-28', 250.00, 'Entertainment', 'Movie ticket'),
('2026-08-28', 600.00, 'Health', 'Gym membership');