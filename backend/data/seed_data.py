"""
Seed data for all 12 practice datasets.

Contains realistic data for data engineering SQL practice.
Each function returns (table_name, columns, rows) ready for DuckDB insertion.
"""

from datetime import date, datetime


def get_customers():
    """Customer master data — 20 rows."""
    return (
        "customers",
        ["customer_id", "name", "email", "region", "segment", "join_date"],
        [
            (1, "Alice Johnson", "alice@example.com", "North", "Premium", "2022-01-15"),
            (2, "Bob Smith", "bob@example.com", "South", "Standard", "2022-03-22"),
            (3, "Carol Williams", "carol@example.com", "East", "Premium", "2021-11-10"),
            (4, "David Brown", "david@example.com", "West", "Standard", "2023-01-05"),
            (5, "Eve Davis", "eve@example.com", "North", "Budget", "2022-07-18"),
            (6, "Frank Miller", "frank@example.com", "South", "Premium", "2021-06-30"),
            (7, "Grace Wilson", "grace@example.com", "East", "Standard", "2022-09-12"),
            (8, "Hank Moore", "hank@example.com", "West", "Budget", "2023-04-25"),
            (9, "Ivy Taylor", "ivy@example.com", "North", "Premium", "2021-12-01"),
            (10, "Jack Anderson", "jack@example.com", "South", "Standard", "2022-05-14"),
            (11, "Karen Thomas", "karen@example.com", "East", "Premium", "2022-02-28"),
            (12, "Leo Jackson", "leo@example.com", "West", "Budget", "2023-06-10"),
            (13, "Mia White", "mia@example.com", "North", "Standard", "2021-08-20"),
            (14, "Noah Harris", "noah@example.com", "South", "Premium", "2022-11-03"),
            (15, "Olivia Martin", "olivia@example.com", "East", "Budget", "2023-02-14"),
            (16, "Paul Garcia", "paul@example.com", "West", "Standard", "2022-04-07"),
            (17, "Quinn Lee", "quinn@example.com", "North", "Premium", "2021-10-19"),
            (18, "Rita Clark", "rita@example.com", "South", "Budget", "2023-03-30"),
            (19, "Sam Lewis", "sam@example.com", "East", "Standard", "2022-06-25"),
            (20, "Tina Hall", "tina@example.com", "West", "Premium", "2021-09-08"),
        ],
    )


def get_products():
    """Product catalog — 15 rows."""
    return (
        "products",
        ["product_id", "name", "category", "price", "stock_quantity"],
        [
            (101, "Laptop Pro", "Electronics", 1299.99, 150),
            (102, "Wireless Mouse", "Electronics", 29.99, 500),
            (103, "Mechanical Keyboard", "Electronics", 89.99, 300),
            (104, "USB-C Hub", "Electronics", 49.99, 200),
            (105, "Monitor 27inch", "Electronics", 399.99, 100),
            (106, "Office Chair", "Furniture", 249.99, 80),
            (107, "Standing Desk", "Furniture", 599.99, 60),
            (108, "Desk Lamp", "Furniture", 39.99, 250),
            (109, "Notebook Pack", "Stationery", 12.99, 1000),
            (110, "Pen Set", "Stationery", 8.99, 800),
            (111, "Backpack", "Accessories", 59.99, 400),
            (112, "Water Bottle", "Accessories", 14.99, 600),
            (113, "Headphones", "Electronics", 199.99, 220),
            (114, "Webcam HD", "Electronics", 79.99, 180),
            (115, "Cable Organizer", "Accessories", 9.99, 700),
        ],
    )


def get_sellers():
    """Seller master data — 8 rows."""
    return (
        "sellers",
        ["seller_id", "name", "region", "target_revenue", "active_since"],
        [
            (1, "TechWorld", "North", 50000.00, "2020-01-01"),
            (2, "OfficeMart", "South", 40000.00, "2019-06-15"),
            (3, "GadgetZone", "East", 60000.00, "2021-03-20"),
            (4, "FurniCo", "West", 35000.00, "2020-08-10"),
            (5, "QuickShip", "North", 45000.00, "2021-01-01"),
            (6, "PrimeGoods", "South", 55000.00, "2019-11-25"),
            (7, "ValueStore", "East", 30000.00, "2022-02-14"),
            (8, "MegaDeals", "West", 70000.00, "2020-05-05"),
        ],
    )


def get_orders():
    """Order transactions — 60 rows with various statuses."""
    return (
        "orders",
        ["order_id", "customer_id", "seller_id", "product_id", "quantity", "amount", "status", "order_date", "delivery_date"],
        [
            (1001, 1, 1, 101, 1, 1299.99, "delivered", "2024-01-05", "2024-01-10"),
            (1002, 2, 2, 106, 2, 499.98, "delivered", "2024-01-06", "2024-01-12"),
            (1003, 3, 3, 113, 1, 199.99, "delivered", "2024-01-07", "2024-01-11"),
            (1004, 1, 1, 102, 3, 89.97, "delivered", "2024-01-08", "2024-01-13"),
            (1005, 4, 4, 107, 1, 599.99, "cancelled", "2024-01-09", None),
            (1006, 5, 5, 103, 1, 89.99, "delivered", "2024-01-10", "2024-01-15"),
            (1007, 6, 6, 105, 1, 399.99, "delivered", "2024-01-11", "2024-01-16"),
            (1008, 7, 7, 109, 5, 64.95, "delivered", "2024-01-12", "2024-01-17"),
            (1009, 8, 8, 111, 2, 119.98, "returned", "2024-01-13", "2024-01-18"),
            (1010, 9, 1, 101, 1, 1299.99, "delivered", "2024-01-15", "2024-01-20"),
            (1011, 10, 2, 108, 3, 119.97, "delivered", "2024-01-16", "2024-01-21"),
            (1012, 11, 3, 113, 2, 399.98, "shipped", "2024-01-17", None),
            (1013, 12, 4, 106, 1, 249.99, "delivered", "2024-01-18", "2024-01-23"),
            (1014, 13, 5, 104, 2, 99.98, "delivered", "2024-01-19", "2024-01-24"),
            (1015, 14, 6, 107, 1, 599.99, "delivered", "2024-01-20", "2024-01-25"),
            (1016, 15, 7, 110, 10, 89.90, "cancelled", "2024-01-21", None),
            (1017, 16, 8, 112, 4, 59.96, "delivered", "2024-01-22", "2024-01-27"),
            (1018, 17, 1, 103, 1, 89.99, "delivered", "2024-01-23", "2024-01-28"),
            (1019, 18, 2, 114, 1, 79.99, "returned", "2024-01-24", "2024-01-29"),
            (1020, 19, 3, 102, 2, 59.98, "delivered", "2024-01-25", "2024-01-30"),
            (1021, 20, 4, 115, 5, 49.95, "delivered", "2024-01-26", "2024-01-31"),
            (1022, 1, 5, 105, 1, 399.99, "delivered", "2024-02-01", "2024-02-06"),
            (1023, 2, 6, 101, 1, 1299.99, "delivered", "2024-02-02", "2024-02-07"),
            (1024, 3, 7, 103, 2, 179.98, "shipped", "2024-02-03", None),
            (1025, 4, 8, 108, 1, 39.99, "delivered", "2024-02-04", "2024-02-09"),
            (1026, 5, 1, 111, 1, 59.99, "delivered", "2024-02-05", "2024-02-10"),
            (1027, 6, 2, 102, 5, 149.95, "delivered", "2024-02-06", "2024-02-11"),
            (1028, 7, 3, 107, 1, 599.99, "cancelled", "2024-02-07", None),
            (1029, 8, 4, 104, 3, 149.97, "delivered", "2024-02-08", "2024-02-13"),
            (1030, 9, 5, 113, 1, 199.99, "delivered", "2024-02-09", "2024-02-14"),
            (1031, 10, 6, 106, 1, 249.99, "delivered", "2024-02-10", "2024-02-15"),
            (1032, 11, 7, 112, 3, 44.97, "delivered", "2024-02-11", "2024-02-16"),
            (1033, 12, 8, 101, 1, 1299.99, "delivered", "2024-02-12", "2024-02-17"),
            (1034, 13, 1, 109, 2, 25.98, "returned", "2024-02-13", "2024-02-18"),
            (1035, 14, 2, 103, 1, 89.99, "delivered", "2024-02-14", "2024-02-19"),
            (1036, 15, 3, 110, 5, 44.95, "delivered", "2024-02-15", "2024-02-20"),
            (1037, 16, 4, 114, 1, 79.99, "delivered", "2024-02-16", "2024-02-21"),
            (1038, 17, 5, 105, 1, 399.99, "shipped", "2024-02-17", None),
            (1039, 18, 6, 115, 2, 19.98, "delivered", "2024-02-18", "2024-02-23"),
            (1040, 19, 7, 101, 1, 1299.99, "delivered", "2024-02-19", "2024-02-24"),
            (1041, 20, 8, 102, 4, 119.96, "delivered", "2024-02-20", "2024-02-25"),
            (1042, 1, 1, 113, 1, 199.99, "delivered", "2024-03-01", "2024-03-06"),
            (1043, 3, 3, 106, 1, 249.99, "delivered", "2024-03-02", "2024-03-07"),
            (1044, 5, 5, 107, 1, 599.99, "delivered", "2024-03-03", "2024-03-08"),
            (1045, 7, 7, 104, 2, 99.98, "cancelled", "2024-03-04", None),
            (1046, 9, 1, 108, 1, 39.99, "delivered", "2024-03-05", "2024-03-10"),
            (1047, 11, 3, 111, 3, 179.97, "delivered", "2024-03-06", "2024-03-11"),
            (1048, 13, 5, 112, 2, 29.98, "delivered", "2024-03-07", "2024-03-12"),
            (1049, 15, 7, 115, 1, 9.99, "delivered", "2024-03-08", "2024-03-13"),
            (1050, 17, 1, 101, 1, 1299.99, "delivered", "2024-03-09", "2024-03-14"),
            # Duplicate order_id for deduplication practice
            (1050, 17, 1, 101, 1, 1299.99, "delivered", "2024-03-09", "2024-03-14"),
            (1051, 2, 2, 105, 1, 399.99, "delivered", "2024-03-10", "2024-03-15"),
            (1052, 4, 4, 103, 1, 89.99, "delivered", "2024-03-11", "2024-03-16"),
            (1053, 6, 6, 109, 3, 38.97, "delivered", "2024-03-12", "2024-03-17"),
            (1054, 8, 8, 110, 2, 17.98, "shipped", "2024-03-13", None),
            (1055, 10, 2, 114, 1, 79.99, "delivered", "2024-03-14", "2024-03-19"),
            (1056, 12, 4, 102, 2, 59.98, "delivered", "2024-03-15", "2024-03-20"),
            (1057, 14, 6, 113, 1, 199.99, "delivered", "2024-03-16", "2024-03-21"),
            (1058, 16, 8, 107, 1, 599.99, "delivered", "2024-03-17", "2024-03-22"),
            (1059, 18, 2, 108, 1, 39.99, "delivered", "2024-03-18", "2024-03-23"),
            (1060, 20, 4, 111, 1, 59.99, "delivered", "2024-03-19", "2024-03-24"),
        ],
    )


def get_employees():
    """Employee data — 15 rows with hierarchy."""
    return (
        "employees",
        ["employee_id", "name", "department_id", "manager_id", "hire_date", "salary", "status"],
        [
            (1, "Sarah CEO", 1, None, "2018-01-01", 180000, "active"),
            (2, "Tom VP Eng", 2, 1, "2018-06-15", 150000, "active"),
            (3, "Uma VP Sales", 3, 1, "2019-03-01", 140000, "active"),
            (4, "Victor Dev", 2, 2, "2020-01-10", 95000, "active"),
            (5, "Wendy Dev", 2, 2, "2020-04-20", 92000, "active"),
            (6, "Xena QA", 2, 2, "2021-02-15", 85000, "active"),
            (7, "Yuri Sales", 3, 3, "2020-08-01", 75000, "active"),
            (8, "Zara Sales", 3, 3, "2021-05-10", 72000, "active"),
            (9, "Adam Ops", 4, 1, "2019-07-22", 88000, "active"),
            (10, "Beth Data", 2, 2, "2021-09-01", 105000, "active"),
            (11, "Carl Intern", 2, 4, "2023-06-01", 45000, "inactive"),
            (12, "Dana HR", 5, 1, "2019-11-15", 82000, "active"),
            (13, "Erik Sales", 3, 3, "2022-01-10", 70000, "active"),
            (14, "Fay Dev", 2, 2, "2022-07-01", 98000, "active"),
            (15, "Gina Ops", 4, 9, "2023-03-15", 78000, "active"),
        ],
    )


def get_departments():
    """Department data — 5 rows."""
    return (
        "departments",
        ["department_id", "name", "budget", "location"],
        [
            (1, "Executive", 500000, "HQ"),
            (2, "Engineering", 1200000, "HQ"),
            (3, "Sales", 800000, "Regional"),
            (4, "Operations", 600000, "HQ"),
            (5, "Human Resources", 400000, "HQ"),
        ],
    )


def get_transactions():
    """Financial transactions — 30 rows across two systems for reconciliation."""
    return (
        "transactions",
        ["txn_id", "account_id", "amount", "txn_type", "txn_date", "system"],
        [
            (1, "ACC001", 500.00, "credit", "2024-01-05", "source"),
            (2, "ACC001", -200.00, "debit", "2024-01-06", "source"),
            (3, "ACC002", 1500.00, "credit", "2024-01-07", "source"),
            (4, "ACC002", -300.00, "debit", "2024-01-08", "source"),
            (5, "ACC003", 800.00, "credit", "2024-01-09", "source"),
            (6, "ACC003", -150.00, "debit", "2024-01-10", "source"),
            (7, "ACC001", 250.00, "credit", "2024-01-11", "source"),
            (8, "ACC004", 2000.00, "credit", "2024-01-12", "source"),
            (9, "ACC004", -500.00, "debit", "2024-01-13", "source"),
            (10, "ACC005", 1200.00, "credit", "2024-01-14", "source"),
            (11, "ACC005", -400.00, "debit", "2024-01-15", "source"),
            (12, "ACC001", -100.00, "debit", "2024-01-16", "source"),
            (13, "ACC002", 600.00, "credit", "2024-01-17", "source"),
            (14, "ACC003", -200.00, "debit", "2024-01-18", "source"),
            (15, "ACC006", 900.00, "credit", "2024-01-19", "source"),
            # Target system — some mismatches for reconciliation practice
            (1, "ACC001", 500.00, "credit", "2024-01-05", "target"),
            (2, "ACC001", -200.00, "debit", "2024-01-06", "target"),
            (3, "ACC002", 1500.00, "credit", "2024-01-07", "target"),
            (4, "ACC002", -300.00, "debit", "2024-01-08", "target"),
            (5, "ACC003", 800.00, "credit", "2024-01-09", "target"),
            (6, "ACC003", -150.00, "debit", "2024-01-10", "target"),
            (7, "ACC001", 250.00, "credit", "2024-01-11", "target"),
            (8, "ACC004", 2100.00, "credit", "2024-01-12", "target"),  # Mismatch: 2000 vs 2100
            (9, "ACC004", -500.00, "debit", "2024-01-13", "target"),
            (10, "ACC005", 1200.00, "credit", "2024-01-14", "target"),
            # txn_id 11 missing in target — missing record
            (12, "ACC001", -100.00, "debit", "2024-01-16", "target"),
            (13, "ACC002", 600.00, "credit", "2024-01-17", "target"),
            (14, "ACC003", -200.00, "debit", "2024-01-18", "target"),
            (15, "ACC006", 900.00, "credit", "2024-01-19", "target"),
            (16, "ACC006", 50.00, "credit", "2024-01-20", "target"),  # Extra in target
        ],
    )


def get_events():
    """Clickstream / event log data — 25 rows."""
    return (
        "events",
        ["event_id", "user_id", "event_type", "event_timestamp", "page", "session_id"],
        [
            (1, "U001", "page_view", "2024-01-10 09:00:00", "/home", "S001"),
            (2, "U001", "click", "2024-01-10 09:01:30", "/products", "S001"),
            (3, "U001", "page_view", "2024-01-10 09:02:00", "/products", "S001"),
            (4, "U001", "add_to_cart", "2024-01-10 09:05:00", "/products/101", "S001"),
            (5, "U001", "purchase", "2024-01-10 09:10:00", "/checkout", "S001"),
            (6, "U002", "page_view", "2024-01-10 10:00:00", "/home", "S002"),
            (7, "U002", "click", "2024-01-10 10:03:00", "/categories", "S002"),
            (8, "U002", "page_view", "2024-01-10 10:04:00", "/categories", "S002"),
            (9, "U002", "page_view", "2024-01-10 14:00:00", "/home", "S003"),
            (10, "U002", "add_to_cart", "2024-01-10 14:05:00", "/products/102", "S003"),
            (11, "U003", "page_view", "2024-01-11 08:00:00", "/home", "S004"),
            (12, "U003", "click", "2024-01-11 08:01:00", "/deals", "S004"),
            (13, "U003", "purchase", "2024-01-11 08:15:00", "/checkout", "S004"),
            (14, "U001", "page_view", "2024-01-12 11:00:00", "/home", "S005"),
            (15, "U001", "page_view", "2024-01-12 11:30:00", "/account", "S005"),
            (16, "U004", "page_view", "2024-01-12 12:00:00", "/home", "S006"),
            (17, "U004", "click", "2024-01-12 12:01:00", "/products", "S006"),
            (18, "U004", "add_to_cart", "2024-01-12 12:05:00", "/products/105", "S006"),
            (19, "U004", "add_to_cart", "2024-01-12 12:06:00", "/products/113", "S006"),
            (20, "U004", "purchase", "2024-01-12 12:15:00", "/checkout", "S006"),
            (21, "U005", "page_view", "2024-01-13 09:00:00", "/home", "S007"),
            (22, "U005", "click", "2024-01-13 09:02:00", "/products", "S007"),
            (23, "U005", "page_view", "2024-01-13 09:03:00", "/products", "S007"),
            (24, "U005", "page_view", "2024-01-13 15:00:00", "/home", "S008"),
            (25, "U005", "purchase", "2024-01-13 15:10:00", "/checkout", "S008"),
        ],
    )


def get_inventory_snapshots():
    """Daily inventory snapshots — 30 rows."""
    return (
        "inventory_snapshots",
        ["snapshot_date", "product_id", "warehouse_id", "qty_on_hand", "qty_reserved"],
        [
            ("2024-01-01", 101, "WH1", 150, 10),
            ("2024-01-01", 102, "WH1", 500, 20),
            ("2024-01-01", 103, "WH1", 300, 5),
            ("2024-01-01", 105, "WH2", 100, 8),
            ("2024-01-01", 107, "WH2", 60, 3),
            ("2024-01-01", 113, "WH1", 220, 15),
            ("2024-01-15", 101, "WH1", 140, 12),
            ("2024-01-15", 102, "WH1", 480, 25),
            ("2024-01-15", 103, "WH1", 295, 8),
            ("2024-01-15", 105, "WH2", 92, 5),
            ("2024-01-15", 107, "WH2", 58, 4),
            ("2024-01-15", 113, "WH1", 210, 18),
            ("2024-02-01", 101, "WH1", 130, 15),
            ("2024-02-01", 102, "WH1", 460, 30),
            ("2024-02-01", 103, "WH1", 288, 10),
            ("2024-02-01", 105, "WH2", 85, 7),
            ("2024-02-01", 107, "WH2", 55, 2),
            ("2024-02-01", 113, "WH1", 195, 20),
            ("2024-02-15", 101, "WH1", 118, 8),
            ("2024-02-15", 102, "WH1", 440, 22),
            ("2024-02-15", 103, "WH1", 280, 12),
            ("2024-02-15", 105, "WH2", 78, 6),
            ("2024-02-15", 107, "WH2", 50, 5),
            ("2024-02-15", 113, "WH1", 180, 16),
            ("2024-03-01", 101, "WH1", 105, 10),
            ("2024-03-01", 102, "WH1", 420, 18),
            ("2024-03-01", 103, "WH1", 270, 8),
            ("2024-03-01", 105, "WH2", 70, 4),
            ("2024-03-01", 107, "WH2", 45, 3),
            ("2024-03-01", 113, "WH1", 165, 14),
        ],
    )


def get_pipeline_run_log():
    """Pipeline execution logs — 20 rows."""
    return (
        "pipeline_run_log",
        ["run_id", "pipeline_name", "status", "start_ts", "end_ts", "records_processed", "error_message"],
        [
            (1, "ingest_orders", "success", "2024-01-10 01:00:00", "2024-01-10 01:15:00", 5000, None),
            (2, "ingest_customers", "success", "2024-01-10 01:00:00", "2024-01-10 01:05:00", 200, None),
            (3, "transform_daily_agg", "success", "2024-01-10 02:00:00", "2024-01-10 02:30:00", 3500, None),
            (4, "ingest_orders", "failed", "2024-01-11 01:00:00", "2024-01-11 01:02:00", 0, "Connection timeout"),
            (5, "ingest_orders", "success", "2024-01-11 01:30:00", "2024-01-11 01:45:00", 4800, None),
            (6, "ingest_customers", "success", "2024-01-11 01:00:00", "2024-01-11 01:06:00", 210, None),
            (7, "transform_daily_agg", "success", "2024-01-11 02:00:00", "2024-01-11 02:28:00", 3200, None),
            (8, "export_to_warehouse", "failed", "2024-01-11 03:00:00", "2024-01-11 03:01:00", 0, "Auth failed"),
            (9, "ingest_orders", "success", "2024-01-12 01:00:00", "2024-01-12 01:12:00", 5200, None),
            (10, "transform_daily_agg", "success", "2024-01-12 02:00:00", "2024-01-12 02:25:00", 3800, None),
            (11, "export_to_warehouse", "success", "2024-01-12 03:00:00", "2024-01-12 03:20:00", 3800, None),
            (12, "ingest_orders", "success", "2024-01-13 01:00:00", "2024-01-13 01:18:00", 5500, None),
            (13, "ingest_customers", "failed", "2024-01-13 01:00:00", "2024-01-13 01:01:00", 0, "Schema mismatch"),
            (14, "transform_daily_agg", "failed", "2024-01-13 02:00:00", "2024-01-13 02:05:00", 0, "Upstream dependency failed"),
            (15, "ingest_orders", "success", "2024-01-14 01:00:00", "2024-01-14 01:14:00", 4900, None),
            (16, "ingest_customers", "success", "2024-01-14 01:00:00", "2024-01-14 01:04:00", 215, None),
            (17, "transform_daily_agg", "success", "2024-01-14 02:00:00", "2024-01-14 02:22:00", 3600, None),
            (18, "export_to_warehouse", "success", "2024-01-14 03:00:00", "2024-01-14 03:15:00", 3600, None),
            (19, "data_quality_check", "success", "2024-01-14 04:00:00", "2024-01-14 04:10:00", 15000, None),
            (20, "data_quality_check", "failed", "2024-01-13 04:00:00", "2024-01-13 04:02:00", 0, "Null PK detected"),
        ],
    )


def get_source_target_recon():
    """Source-to-target reconciliation data — 10 rows."""
    return (
        "source_target_recon",
        ["recon_date", "table_name", "source_count", "target_count", "source_sum", "target_sum", "status"],
        [
            ("2024-01-10", "orders", 5000, 5000, 2500000.00, 2500000.00, "matched"),
            ("2024-01-10", "customers", 200, 200, None, None, "matched"),
            ("2024-01-11", "orders", 4800, 4795, 2400000.00, 2395000.00, "mismatched"),
            ("2024-01-11", "customers", 210, 210, None, None, "matched"),
            ("2024-01-12", "orders", 5200, 5200, 2600000.00, 2600000.00, "matched"),
            ("2024-01-12", "customers", 210, 210, None, None, "matched"),
            ("2024-01-13", "orders", 5500, 5500, 2750000.00, 2750000.00, "matched"),
            ("2024-01-13", "customers", 215, 200, None, None, "mismatched"),
            ("2024-01-14", "orders", 4900, 4900, 2450000.00, 2450000.00, "matched"),
            ("2024-01-14", "customers", 215, 215, None, None, "matched"),
        ],
    )


def get_scd_customers():
    """Slowly Changing Dimension Type 2 sample — 18 rows."""
    return (
        "scd_customers",
        ["scd_id", "customer_id", "name", "region", "segment", "effective_start", "effective_end", "is_current"],
        [
            (1, 1, "Alice Johnson", "North", "Standard", "2022-01-15", "2023-06-01", False),
            (2, 1, "Alice Johnson", "North", "Premium", "2023-06-01", "9999-12-31", True),
            (3, 2, "Bob Smith", "South", "Standard", "2022-03-22", "9999-12-31", True),
            (4, 3, "Carol Williams", "East", "Standard", "2021-11-10", "2022-08-15", False),
            (5, 3, "Carol Williams", "East", "Premium", "2022-08-15", "9999-12-31", True),
            (6, 4, "David Brown", "West", "Standard", "2023-01-05", "9999-12-31", True),
            (7, 5, "Eve Davis", "North", "Budget", "2022-07-18", "9999-12-31", True),
            (8, 6, "Frank Miller", "South", "Standard", "2021-06-30", "2022-01-01", False),
            (9, 6, "Frank Miller", "South", "Premium", "2022-01-01", "2023-09-01", False),
            (10, 6, "Frank Miller", "East", "Premium", "2023-09-01", "9999-12-31", True),
            (11, 7, "Grace Wilson", "East", "Standard", "2022-09-12", "9999-12-31", True),
            (12, 8, "Hank Moore", "West", "Budget", "2023-04-25", "9999-12-31", True),
            (13, 9, "Ivy Taylor", "North", "Standard", "2021-12-01", "2022-11-15", False),
            (14, 9, "Ivy Taylor", "North", "Premium", "2022-11-15", "9999-12-31", True),
            (15, 10, "Jack Anderson", "South", "Standard", "2022-05-14", "9999-12-31", True),
            (16, 17, "Quinn Lee", "North", "Standard", "2021-10-19", "2023-01-01", False),
            (17, 17, "Quinn Lee", "North", "Premium", "2023-01-01", "9999-12-31", True),
            (18, 20, "Tina Hall", "West", "Premium", "2021-09-08", "9999-12-31", True),
        ],
    )


# Registry of all datasets for easy iteration
ALL_DATASETS = [
    get_customers,
    get_products,
    get_sellers,
    get_orders,
    get_employees,
    get_departments,
    get_transactions,
    get_events,
    get_inventory_snapshots,
    get_pipeline_run_log,
    get_source_target_recon,
    get_scd_customers,
]
