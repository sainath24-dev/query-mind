#!/usr/bin/env python3
"""
Seed Database Script
Initializes database schema and populates synthetic dataset.
"""
import subprocess
import sys
import os

def run():
    print("Initializing QueryMind schema...")
    res = subprocess.run([
        "./pg_env/bin/psql", "-h", "localhost", "-p", "5432", "-U", "postgres", "-d", "querymind", "-f", "database/schema.sql"
    ])
    if res.returncode != 0:
        print("Schema creation failed!")
        sys.exit(res.returncode)

    print("Generating synthetic data...")
    res = subprocess.run([sys.executable, "scripts/generate_dataset.py"])
    if res.returncode != 0:
        print("Data generation failed!")
        sys.exit(res.returncode)

    print("Database seeding completed successfully.")

if __name__ == "__main__":
    run()
