import sqlite3
from pathlib import Path

from evidence.schemas import EvidenceReport

from .models import SessionMetric


class SessionRepository:
    """Small local SQLite store for validated session metrics."""

    def __init__(self, database_path: str | Path = "tennis_tracker.db"):
        self.database_path = str(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS session_metrics (
                    session_id TEXT NOT NULL,
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    sample_count INTEGER NOT NULL,
                    confidence REAL NOT NULL,
                    PRIMARY KEY (session_id, metric)
                )
                """
            )

    def save_evidence(self, report: EvidenceReport) -> None:
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT OR REPLACE INTO session_metrics
                    (session_id, metric, value, sample_count, confidence)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    (report.session_id, item.evidence_id, float(item.value), item.sample_count, item.measurement_confidence)
                    for item in report.items
                    if isinstance(item.value, (int, float))
                ),
            )

    def get_metric_history(self, metric: str, limit: int = 3) -> list[SessionMetric]:
        if limit < 1:
            raise ValueError("limit must be positive")
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT session_id, metric, value, sample_count, confidence
                FROM session_metrics WHERE metric = ?
                ORDER BY rowid DESC LIMIT ?
                """,
                (metric, limit),
            ).fetchall()
        return [SessionMetric(row["session_id"], row["metric"], row["value"], row["sample_count"], row["confidence"]) for row in rows]