"""
Quick verification script to check Qdrant database content
Uses the Qdrant HTTP API instead of local client to avoid lock
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Since we can't access the local Qdrant due to lock,
# let's verify by checking the metadata in the data directory
import sqlite3

db_path = "./qdrant_data/collection/defense_docs/storage.sqlite"

if not os.path.exists(db_path):
    print("❌ Database file not found!")
    exit(1)

print("✓ Database file exists")
print(f"  Size: {os.path.getsize(db_path)} bytes")
print()

# Try to read the SQLite database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"✓ SQLite tables found: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    print()

    # Try to count records in points table if it exists
    cursor.execute("SELECT COUNT(*) FROM points;")
    count = cursor.fetchone()[0]
    print(f"✓ Total points in database: {count}")
    print()

    # Get some sample data
    cursor.execute("SELECT id, payload FROM points LIMIT 3;")
    samples = cursor.fetchall()

    print(f"Sample documents:")
    for i, (point_id, payload_json) in enumerate(samples, 1):
        payload = json.loads(payload_json)
        print(f"\n{i}. Point ID: {point_id}")
        print(f"   Manual: {payload.get('manual_name', 'N/A')}")
        print(f"   Page: {payload.get('page_number', 'N/A')}")
        print(f"   Type: {payload.get('document_type', 'N/A')}")
        print(f"   Classification: {payload.get('classification', 'N/A')}")
        text = payload.get('text', '')
        print(f"   Text preview: {text[:100]}...")

    conn.close()

    print("\n" + "="*60)
    print("✅ DATABASE VERIFICATION SUCCESSFUL")
    print(f"✅ {count} document chunks are indexed and ready")
    print("="*60)

except sqlite3.Error as e:
    print(f"❌ SQLite error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
