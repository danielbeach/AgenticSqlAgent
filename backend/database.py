"""Database initialization and setup."""
import sqlite3
from pathlib import Path
from typing import Optional
import random
from datetime import datetime, timedelta


def init_database(db_path: str = "sales.db") -> None:
    """Initialize SQLite database with sales data."""
    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create sales_people table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            region TEXT NOT NULL,
            hire_date DATE NOT NULL,
            quota REAL NOT NULL
        )
    """)
    
    # Create sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sales_person_id INTEGER NOT NULL,
            sale_date DATE NOT NULL,
            amount REAL NOT NULL,
            product_category TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            FOREIGN KEY (sales_person_id) REFERENCES sales_people(id)
        )
    """)
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM sales_people")
    if cursor.fetchone()[0] == 0:
        # Insert sample sales people
        sales_people = [
            ("Alice Johnson", "alice.johnson@company.com", "North", "2022-01-15", 100000.0),
            ("Bob Smith", "bob.smith@company.com", "South", "2022-03-20", 120000.0),
            ("Carol Williams", "carol.williams@company.com", "East", "2021-11-10", 95000.0),
            ("David Brown", "david.brown@company.com", "West", "2023-02-01", 110000.0),
            ("Eva Davis", "eva.davis@company.com", "North", "2022-07-15", 105000.0),
            ("Frank Miller", "frank.miller@company.com", "South", "2021-09-05", 115000.0),
            ("Grace Wilson", "grace.wilson@company.com", "East", "2023-01-10", 98000.0),
            ("Henry Moore", "henry.moore@company.com", "West", "2022-05-22", 125000.0),
        ]
        
        cursor.executemany("""
            INSERT INTO sales_people (name, email, region, hire_date, quota)
            VALUES (?, ?, ?, ?, ?)
        """, sales_people)
        
        # Get sales person IDs
        cursor.execute("SELECT id FROM sales_people")
        sales_person_ids = [row[0] for row in cursor.fetchall()]
        
        # Generate sales data for the last 90 days
        product_categories = ["Electronics", "Clothing", "Food", "Furniture", "Books", "Toys"]
        customer_names = [
            "Acme Corp", "Tech Solutions", "Global Industries", "Mega Store",
            "City Retail", "Prime Services", "Elite Group", "Super Market",
            "Best Buy Co", "Top Shelf Inc", "Quality Goods", "Premium Brands"
        ]
        
        sales_data = []
        start_date = datetime.now() - timedelta(days=90)
        
        for day_offset in range(90):
            sale_date = start_date + timedelta(days=day_offset)
            # Generate 5-15 sales per day
            num_sales = random.randint(5, 15)
            
            for _ in range(num_sales):
                sales_person_id = random.choice(sales_person_ids)
                amount = round(random.uniform(100.0, 5000.0), 2)
                product_category = random.choice(product_categories)
                customer_name = random.choice(customer_names)
                
                sales_data.append((
                    sales_person_id,
                    sale_date.strftime("%Y-%m-%d"),
                    amount,
                    product_category,
                    customer_name
                ))
        
        cursor.executemany("""
            INSERT INTO sales (sales_person_id, sale_date, amount, product_category, customer_name)
            VALUES (?, ?, ?, ?, ?)
        """, sales_data)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")


def get_database_path(database_url: str) -> str:
    """Extract file path from SQLite database URL."""
    # Handle sqlite:///./sales.db or sqlite:///sales.db or sqlite:///./data/sales.db
    if database_url.startswith("sqlite:///"):
        path = database_url.replace("sqlite:///", "")
        # Handle relative paths
        if path.startswith("./"):
            return path
        # If no ./ prefix, add it for relative path
        if not path.startswith("/"):
            return f"./{path}"
        return path
    return database_url

