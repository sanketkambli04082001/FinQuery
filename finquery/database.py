import sqlite3
import json
import os

DB_FILENAME = os.environ.get("REPORTS_DB", "finquery.db")


class DataBaseManager:
    
    def __init__(self, db_path: str = DB_FILENAME):
        self.db_path = db_path
        self._create_tables()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        """
        Create the reports table and ensure it has columns for competitor_rows and pdf_text.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,
                    summary TEXT,
                    competitors TEXT,
                    competitor_rows TEXT,
                    chart_filename TEXT,
                    pdf_text TEXT,
                    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        except Exception as e:
            print("[DB ERROR] _create_tables:", e)
        finally:
            try:
                conn.close()
            except:
                pass

    def save_report(self, report_data):
        """
        Saves a report and returns the new id.
        report_data expects keys:
         - ticker (str)
         - summary (str)
         - competitors (list)
         - competitor_rows (list/dict)
         - chart_filename (str)
         - pdf_text (str)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            comps_str = json.dumps(report_data.get('competitors', []))
            comp_rows_str = json.dumps(report_data.get('competitor_rows', []))
            pdf_text = report_data.get('pdf_text', '') or ''

            cursor.execute("""
                INSERT INTO reports (ticker, summary, competitors, competitor_rows, chart_filename, pdf_text)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                report_data.get('ticker', 'UNKNOWN'),
                report_data.get('summary', ''),
                comps_str,
                comp_rows_str,
                report_data.get('chart_filename', ''),
                pdf_text
            ))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            print(f"--- [DB] Report saved successfully with ID: {new_id} ---")
            return new_id
        except Exception as e:
            print(f"--- [DB ERROR] save_report failed: {e}")
            try:
                conn.close()
            except:
                pass
            return None

    def get_report(self, report_id):
        """
        Fetch a single report by id. Returns a dict or None.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, ticker, summary, competitors, competitor_rows, chart_filename, pdf_text, analysis_date
                FROM reports WHERE id = ?
            """, (report_id,))
            row = cursor.fetchone()
            conn.close()
            if not row:
                return None

            def _safe_load(s):
                if not s:
                    return []
                try:
                    return json.loads(s)
                except Exception:
                    return []

            return {
                "id": row["id"],
                "ticker": row["ticker"],
                "summary": row["summary"],
                "competitors": _safe_load(row["competitors"]),
                "competitor_rows": _safe_load(row["competitor_rows"]),
                "chart_filename": row["chart_filename"] or "",
                "pdf_text": row["pdf_text"] or "",
                "analysis_date": row["analysis_date"]
            }
        except Exception as e:
            print(f"[DB ERROR] get_report failed for id={report_id}: {e}")
            try:
                conn.close()
            except:
                pass
            return None
