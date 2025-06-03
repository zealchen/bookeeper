import sqlite3
import click
import pandas as pd
from datetime import datetime
from pathlib import Path
from prettytable import PrettyTable

DEFAULT_DB = "my.db"
CATEGORIES = [
    "Food", "Transport", "Housing", "Utilities",
    "Entertainment", "Shopping", "Healthcare", "Education", "Other"
]

def get_db_connection(db_path):
    return sqlite3.connect(db_path)

def ensure_table_exists(db_path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            UNIQUE(date, amount, category)
        )
    ''')
    conn.commit()
    conn.close()

@click.group()
def cli():
    """Simple bookkeeping tool."""
    pass

@cli.command(name="init-db")
@click.option('--db-path', default=DEFAULT_DB, show_default=True, help="Path to the SQLite database")
def init_db(db_path):
    """Initialize the database with table structure."""
    ensure_table_exists(db_path)
    click.echo(f"✅ Initialized database at {db_path}")

@cli.command(name="import-record")
@click.option('--date', required=True, help='Date of the record in YYYY-MM-DD format')
@click.option('--amount', required=True, type=float, help='Amount spent')
@click.option('--category', required=True, type=click.Choice(CATEGORIES), help='Spending category')
@click.option('--note', default='', help='Additional note')
@click.option('--db-path', default=DEFAULT_DB, show_default=True, help="Path to the SQLite database")
def import_record(date, amount, category, note, db_path):
    """Import a new record into the database."""
    try:
        datetime.strptime(date, "%Y-%m-%d")  # validate date
        ensure_table_exists(db_path)
        conn = get_db_connection(db_path)
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO records (date, amount, category, note)
                VALUES (?, ?, ?, ?)
            ''', (date, amount, category, note))
            conn.commit()
            click.echo("✅ Record imported successfully.")
        except sqlite3.IntegrityError:
            click.echo("⚠️ Duplicate record found. Import skipped.")
        finally:
            conn.close()
    except Exception as e:
        click.echo(f"❌ Error importing record: {e}")

@cli.command(name="export-records")
@click.option('--output', default='ledger_export.xlsx', help='Excel filename to export')
@click.option('--db-path', default=DEFAULT_DB, show_default=True, help="Path to the SQLite database")
def export_records(output, db_path):
    """Export all records to an Excel file."""
    try:
        ensure_table_exists(db_path)
        conn = get_db_connection(db_path)
        df = pd.read_sql_query("SELECT date, amount, category, note FROM records", conn)
        df.to_excel(output, index=False)
        click.echo(f"✅ Records exported to {output}")
    except Exception as e:
        click.echo(f"❌ Error exporting to Excel: {e}")
    finally:
        conn.close()
        

@cli.command(name="report")
@click.option('--start', required=True, help='Start date (inclusive) in YYYY-MM-DD')
@click.option('--end', required=True, help='End date (inclusive) in YYYY-MM-DD')
@click.option('--db-path', default=DEFAULT_DB, show_default=True, help="Path to the SQLite database")
def report(start, end, db_path):
    """Show records between two dates and summarize by category."""
    try:
        # 日期校验
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        ensure_table_exists(db_path)
        conn = get_db_connection(db_path)
        df = pd.read_sql_query('''
            SELECT date, amount, category, note
            FROM records
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
        ''', conn, params=(start, end))

        if df.empty:
            click.echo("⚠️ No records found for the specified date range.")
            return

        # 输出所有明细
        detail_table = PrettyTable()
        detail_table.field_names = ["Date", "Amount", "Category", "Note"]
        for _, row in df.iterrows():
            detail_table.add_row([row["date"], f"{row['amount']:.2f}", row["category"], row["note"]])
        click.echo("\n📋 Records:")
        click.echo(detail_table)

        # 分类汇总
        summary = df.groupby("category")["amount"].sum()
        summary_table = PrettyTable()
        summary_table.field_names = ["Category", "Total Amount"]
        for category, total in summary.items():
            summary_table.add_row([category, f"${total:.2f}"])

        click.echo("\n📊 Category Summary:")
        click.echo(summary_table)

        total_all = df["amount"].sum()
        click.echo(f"\n💰 Total Amount: ${total_all:.2f}")

    except Exception as e:
        click.echo(f"❌ Error generating report: {e}")


if __name__ == '__main__':
    cli()
