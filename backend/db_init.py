import sqlite3
import os

def init_db(db_path="data/supply_chain.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Suppliers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rating REAL CHECK(rating >= 0 AND rating <= 5),
        certification_status TEXT,
        contact_info TEXT,
        location TEXT
    )
    ''')

    # Create Parts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Parts (
        part_id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_number TEXT UNIQUE NOT NULL,
        description TEXT,
        supplier_id INTEGER,
        lead_time_days INTEGER,
        unit_cost REAL,
        stock_quantity INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES Suppliers (supplier_id)
    )
    ''')

    # Create WorkOrders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS WorkOrders (
        wo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER,
        status TEXT CHECK(status IN ('Open', 'In Progress', 'Blocked', 'Completed')),
        priority TEXT CHECK(priority IN ('Low', 'Medium', 'High', 'Critical')),
        due_date TEXT,
        notes TEXT,
        FOREIGN KEY (part_id) REFERENCES Parts (part_id)
    )
    ''')

    # Clear existing data for fresh seed
    cursor.execute('DELETE FROM WorkOrders')
    cursor.execute('DELETE FROM Parts')
    cursor.execute('DELETE FROM Suppliers')

    # Seed Suppliers
    suppliers = [
        ('AeroTech Dynamics', 4.8, 'AS9100D Certified', 'contact@aerotech.com', 'Seattle'),
        ('Global Machining Solutions', 4.2, 'ISO 9001', 'sales@globalmachining.com', 'Detroit'),
        ('Precision Forgings', 3.9, 'Pending AS9100', 'info@precisionforgings.com', 'Cleveland'),
        ('Quantum Electronics', 4.9, 'NADCAP Certified', 'support@quantumelectronics.com', 'San Jose')
    ]
    cursor.executemany('INSERT INTO Suppliers (name, rating, certification_status, contact_info, location) VALUES (?, ?, ?, ?, ?)', suppliers)

    # Fetch supplier IDs
    cursor.execute('SELECT name, supplier_id FROM Suppliers')
    supplier_map = {row[0]: row[1] for row in cursor.fetchall()}

    # Seed Parts
    parts = [
        ('PT-1001', 'Titanium Compressor Blade', supplier_map['AeroTech Dynamics'], 45, 1250.00, 120),
        ('PT-1002', 'Landing Gear Actuator', supplier_map['Global Machining Solutions'], 90, 8500.00, 15),
        ('PT-1003', 'Avionics Display Unit', supplier_map['Quantum Electronics'], 30, 4200.00, 40),
        ('PT-1004', 'Inconel Fastener Set', supplier_map['Precision Forgings'], 14, 25.50, 5000),
        ('PT-1005', 'Fuel Injector Assembly', supplier_map['AeroTech Dynamics'], 60, 3100.00, 35)
    ]
    cursor.executemany('INSERT INTO Parts (part_number, description, supplier_id, lead_time_days, unit_cost, stock_quantity) VALUES (?, ?, ?, ?, ?, ?)', parts)

    # Fetch part IDs
    cursor.execute('SELECT part_number, part_id FROM Parts')
    part_map = {row[0]: row[1] for row in cursor.fetchall()}

    # Seed Work Orders
    work_orders = [
        (part_map['PT-1001'], 'In Progress', 'High', '2026-04-15', 'Machining phase 2 completed.'),
        (part_map['PT-1002'], 'Blocked', 'Critical', '2026-03-25', 'Awaiting raw material certification from supplier.'),
        (part_map['PT-1003'], 'Completed', 'Medium', '2026-03-01', 'Final QA passed. Ready for assembly.'),
        (part_map['PT-1004'], 'Open', 'Low', '2026-05-10', 'Routine stock replenishment.'),
        (part_map['PT-1005'], 'In Progress', 'High', '2026-04-05', 'Assembly started.'),
        (part_map['PT-1001'], 'Blocked', 'High', '2026-03-20', 'Machine calibration issue holding up production.')
    ]
    cursor.executemany('INSERT INTO WorkOrders (part_id, status, priority, due_date, notes) VALUES (?, ?, ?, ?, ?)', work_orders)

    conn.commit()
    conn.close()
    print(f"Database successfully initialized and seeded at {db_path}")

if __name__ == "__main__":
    init_db()
