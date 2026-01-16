"""
CSV Database Handler
Handles all CSV file operations with file locking for thread safety
"""

import pandas as pd
import os
import threading
from pathlib import Path
from typing import Optional, Any, Union
from datetime import datetime
import tempfile
import shutil
import logging
from contextlib import contextmanager
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Global lock dictionary for file-level locking
_file_locks: dict[str, threading.RLock] = {}
_lock_manager = threading.Lock()


def get_file_lock(file_path: str) -> threading.RLock:
    """Get or create a lock for a specific file"""
    with _lock_manager:
        if file_path not in _file_locks:
            _file_locks[file_path] = threading.RLock()
        return _file_locks[file_path]


class CSVHandler:
    """
    Handles CRUD operations for CSV files with thread-safe file locking.

    Supports two usage patterns:
    1. Direct instantiation: CSVHandler("users.csv")
    2. Table-based operations: CSVHandler() with table_name parameter
    """

    def __init__(self, csv_file: Optional[str] = None):
        """
        Initialize CSV handler

        Args:
            csv_file: Name of the CSV file (e.g., 'users.csv').
                     If None, methods require table_name parameter.
        """
        self.default_file = csv_file
        if csv_file:
            self.file_path = settings.CSV_DIR / csv_file
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self._lock = get_file_lock(str(self.file_path))
        else:
            self.file_path = None
            self._lock = None

    def _get_file_path(self, table_name: Optional[str] = None) -> Path:
        """Get file path for table or default file"""
        if table_name:
            return settings.CSV_DIR / f"{table_name}.csv"
        elif self.file_path:
            return self.file_path
        else:
            raise ValueError("Either csv_file in constructor or table_name parameter required")

    def _get_lock(self, table_name: Optional[str] = None) -> threading.RLock:
        """Get lock for table or default file"""
        if table_name:
            file_path = settings.CSV_DIR / f"{table_name}.csv"
            return get_file_lock(str(file_path))
        elif self._lock:
            return self._lock
        else:
            raise ValueError("Either csv_file in constructor or table_name parameter required")

    @contextmanager
    def _locked_operation(self, table_name: Optional[str] = None):
        """Context manager for locked file operations"""
        lock = self._get_lock(table_name)
        lock.acquire()
        try:
            yield
        finally:
            lock.release()

    def read(self, table_name: Optional[str] = None) -> pd.DataFrame:
        """Read CSV file and return DataFrame"""
        file_path = self._get_file_path(table_name)
        try:
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return pd.DataFrame()
                return pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return pd.DataFrame()

    def write(self, df: pd.DataFrame, table_name: Optional[str] = None) -> bool:
        """Write DataFrame to CSV file with atomic write"""
        file_path = self._get_file_path(table_name)
        temp_file = None
        try:
            with self._locked_operation(table_name):
                # Ensure directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Write to temporary file first (atomic write pattern)
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w',
                    delete=False,
                    suffix='.csv',
                    dir=str(file_path.parent)
                )
                df.to_csv(temp_file.name, index=False)
                temp_file.close()

                # Replace original file atomically
                shutil.move(temp_file.name, file_path)
                return True
        except Exception as e:
            logger.error(f"Error writing {file_path}: {e}")
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.remove(temp_file.name)
                except:
                    pass
            return False

    # ==========================================================================
    # CRUD OPERATIONS - New methods for route compatibility
    # ==========================================================================

    def create(self, table_name: str, data: dict[str, Any]) -> bool:
        """
        Create a new record in the specified table.

        Args:
            table_name: Name of the table (without .csv extension)
            data: Dictionary of column-value pairs

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if file_path.exists():
                    df = pd.read_csv(file_path)
                else:
                    df = pd.DataFrame()

                new_row = pd.DataFrame([data])
                df = pd.concat([df, new_row], ignore_index=True)

                # Write with atomic pattern
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w', delete=False, suffix='.csv',
                    dir=str(file_path.parent)
                )
                df.to_csv(temp_file.name, index=False)
                temp_file.close()
                shutil.move(temp_file.name, file_path)
                return True
        except Exception as e:
            logger.error(f"Error creating record in {table_name}: {e}")
            return False

    def read_all(self, table_name: str) -> list[dict[str, Any]]:
        """
        Read all records from a table.

        Args:
            table_name: Name of the table (without .csv extension)

        Returns:
            List of dictionaries representing all rows
        """
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return []
                df = pd.read_csv(file_path)
                # Replace NaN with None for JSON compatibility
                df = df.where(pd.notnull(df), None)
                return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error reading all from {table_name}: {e}")
            return []

    def read_by_id(self, table_name: str, id_value: Any, id_column: str) -> Optional[dict[str, Any]]:
        """
        Read a single record by ID.

        Args:
            table_name: Name of the table (without .csv extension)
            id_value: Value of the ID to find
            id_column: Name of the ID column

        Returns:
            Dictionary representing the row, or None if not found
        """
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return None
                df = pd.read_csv(file_path)
                if id_column not in df.columns:
                    return None

                # Handle type conversion for comparison
                df[id_column] = df[id_column].astype(str)
                id_value_str = str(id_value)

                matching = df[df[id_column] == id_value_str]
                if matching.empty:
                    return None

                # Replace NaN with None
                row = matching.iloc[0].where(pd.notnull(matching.iloc[0]), None)
                return row.to_dict()
        except Exception as e:
            logger.error(f"Error reading by ID from {table_name}: {e}")
            return None

    def update_by_id(self, table_name: str, id_value: Any, updates: dict[str, Any], id_column: str) -> bool:
        """
        Update a record by ID with atomic read-modify-write.

        Args:
            table_name: Name of the table
            id_value: Value of the ID to update
            updates: Dictionary of column-value pairs to update
            id_column: Name of the ID column

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return False

                df = pd.read_csv(file_path)
                if id_column not in df.columns:
                    return False

                # Handle type conversion
                df[id_column] = df[id_column].astype(str)
                id_value_str = str(id_value)

                mask = df[id_column] == id_value_str
                if not mask.any():
                    return False

                # Update matching rows
                for col, val in updates.items():
                    if col in df.columns:
                        df.loc[mask, col] = val
                    else:
                        df[col] = None
                        df.loc[mask, col] = val

                # Atomic write
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w', delete=False, suffix='.csv',
                    dir=str(file_path.parent)
                )
                df.to_csv(temp_file.name, index=False)
                temp_file.close()
                shutil.move(temp_file.name, file_path)
                return True
        except Exception as e:
            logger.error(f"Error updating by ID in {table_name}: {e}")
            return False

    def delete_by_id(self, table_name: str, id_value: Any, id_column: str) -> bool:
        """
        Delete a record by ID.

        Args:
            table_name: Name of the table
            id_value: Value of the ID to delete
            id_column: Name of the ID column

        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return False

                df = pd.read_csv(file_path)
                if id_column not in df.columns:
                    return False

                df[id_column] = df[id_column].astype(str)
                id_value_str = str(id_value)

                original_len = len(df)
                df = df[df[id_column] != id_value_str]

                if len(df) == original_len:
                    return False  # Nothing deleted

                # Atomic write
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w', delete=False, suffix='.csv',
                    dir=str(file_path.parent)
                )
                df.to_csv(temp_file.name, index=False)
                temp_file.close()
                shutil.move(temp_file.name, file_path)
                return True
        except Exception as e:
            logger.error(f"Error deleting by ID from {table_name}: {e}")
            return False

    def find_all(self, condition: dict[str, Any], table_name: Optional[str] = None) -> list[dict[str, Any]]:
        """
        Find all rows matching condition.

        Args:
            condition: Dictionary of column-value pairs to match
            table_name: Optional table name (uses default if not provided)

        Returns:
            List of matching records
        """
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return []

                df = pd.read_csv(file_path)
                if df.empty:
                    return []

                # Build mask for all conditions
                mask = pd.Series([True] * len(df))
                for col, val in condition.items():
                    if col in df.columns:
                        df[col] = df[col].astype(str)
                        mask &= (df[col] == str(val))

                result = df[mask]
                result = result.where(pd.notnull(result), None)
                return result.to_dict('records')
        except Exception as e:
            logger.error(f"Error finding in {self._get_file_path(table_name)}: {e}")
            return []

    # ==========================================================================
    # Legacy methods (for backward compatibility)
    # ==========================================================================

    def append(self, data: dict[str, Any], table_name: Optional[str] = None) -> bool:
        """Append a new row to CSV file"""
        if table_name:
            return self.create(table_name, data)
        try:
            with self._locked_operation():
                df = self.read()
                new_row = pd.DataFrame([data])
                df = pd.concat([df, new_row], ignore_index=True)
                return self.write(df)
        except Exception as e:
            logger.error(f"Error appending: {e}")
            return False

    def update(self, table_name_or_condition: Union[str, dict],
               id_or_updates: Any = None,
               updates_or_id_column: Any = None,
               id_column: Optional[str] = None) -> bool:
        """
        Update rows - supports both old and new calling conventions.

        Old: update(condition_dict, updates_dict)
        New: update(table_name, id_value, updates_dict, id_column)
        """
        # New API: update(table_name, id_value, updates, id_column)
        if isinstance(table_name_or_condition, str) and id_column is not None:
            return self.update_by_id(
                table_name=table_name_or_condition,
                id_value=id_or_updates,
                updates=updates_or_id_column,
                id_column=id_column
            )

        # Old API: update(condition, updates)
        condition = table_name_or_condition
        updates = id_or_updates

        try:
            with self._locked_operation():
                df = self.read()
                if df.empty:
                    return False

                mask = pd.Series([True] * len(df))
                for col, val in condition.items():
                    if col in df.columns:
                        mask &= (df[col] == val)

                for col, val in updates.items():
                    if col in df.columns:
                        df.loc[mask, col] = val

                return self.write(df)
        except Exception as e:
            logger.error(f"Error updating: {e}")
            return False

    def delete(self, condition: dict[str, Any], table_name: Optional[str] = None) -> bool:
        """Delete rows matching condition"""
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return False

                df = pd.read_csv(file_path)
                if df.empty:
                    return False

                mask = pd.Series([True] * len(df))
                for col, val in condition.items():
                    if col in df.columns:
                        mask &= (df[col] == val)

                df = df[~mask]

                temp_file = tempfile.NamedTemporaryFile(
                    mode='w', delete=False, suffix='.csv',
                    dir=str(file_path.parent)
                )
                df.to_csv(temp_file.name, index=False)
                temp_file.close()
                shutil.move(temp_file.name, file_path)
                return True
        except Exception as e:
            logger.error(f"Error deleting: {e}")
            return False

    def find(self, condition: Optional[dict[str, Any]] = None, table_name: Optional[str] = None) -> list[dict[str, Any]]:
        """Find rows matching condition"""
        if condition is None:
            return self.read_all(table_name) if table_name else []
        return self.find_all(condition, table_name)

    def find_one(self, condition: dict[str, Any], table_name: Optional[str] = None) -> Optional[dict[str, Any]]:
        """Find first row matching condition"""
        results = self.find(condition, table_name)
        return results[0] if results else None

    def generate_id(self, prefix: str, id_column: str, table_name: Optional[str] = None) -> str:
        """Generate unique ID with prefix"""
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return f"{prefix}001"

                df = pd.read_csv(file_path)
                if df.empty or id_column not in df.columns:
                    return f"{prefix}001"

                existing_ids = df[id_column].astype(str).tolist()
                numbers = []
                for id_val in existing_ids:
                    if id_val.startswith(prefix):
                        try:
                            num = int(id_val[len(prefix):])
                            numbers.append(num)
                        except ValueError:
                            continue

                next_num = max(numbers) + 1 if numbers else 1
                return f"{prefix}{next_num:03d}"
        except Exception as e:
            logger.error(f"Error generating ID: {e}")
            import uuid
            return f"{prefix}{uuid.uuid4().hex[:6].upper()}"

    def count(self, condition: Optional[dict[str, Any]] = None, table_name: Optional[str] = None) -> int:
        """Count rows matching condition"""
        results = self.find(condition, table_name)
        return len(results)

    def exists(self, condition: dict[str, Any], table_name: Optional[str] = None) -> bool:
        """Check if any row matches condition"""
        return self.count(condition, table_name) > 0

    def increment_field(self, table_name: str, id_value: Any, id_column: str,
                        field: str, amount: int = 1) -> bool:
        """
        Atomically increment a numeric field.

        Args:
            table_name: Name of the table
            id_value: ID of the record to update
            id_column: Name of the ID column
            field: Name of the field to increment
            amount: Amount to increment by (default 1)

        Returns:
            True if successful
        """
        try:
            file_path = self._get_file_path(table_name)
            with self._locked_operation(table_name):
                if not file_path.exists():
                    return False

                df = pd.read_csv(file_path)
                df[id_column] = df[id_column].astype(str)
                mask = df[id_column] == str(id_value)

                if not mask.any():
                    return False

                current_value = df.loc[mask, field].iloc[0]
                if pd.isna(current_value):
                    current_value = 0

                df.loc[mask, field] = int(current_value) + amount

                temp_file = tempfile.NamedTemporaryFile(
                    mode='w', delete=False, suffix='.csv',
                    dir=str(file_path.parent)
                )
                df.to_csv(temp_file.name, index=False)
                temp_file.close()
                shutil.move(temp_file.name, file_path)
                return True
        except Exception as e:
            logger.error(f"Error incrementing field: {e}")
            return False


# ==========================================================================
# Helper functions for common operations
# ==========================================================================

def get_users_handler() -> CSVHandler:
    """Get handler for users.csv"""
    return CSVHandler("users.csv")


def get_sessions_handler() -> CSVHandler:
    """Get handler for sessions.csv"""
    return CSVHandler("sessions.csv")


def get_scores_handler() -> CSVHandler:
    """Get handler for scores.csv"""
    return CSVHandler("scores.csv")


def get_mcq_questions_handler() -> CSVHandler:
    """Get handler for questions_mcq.csv"""
    return CSVHandler("questions_mcq.csv")


def get_descriptive_questions_handler() -> CSVHandler:
    """Get handler for questions_descriptive.csv"""
    return CSVHandler("questions_descriptive.csv")


def get_tournaments_handler() -> CSVHandler:
    """Get handler for tournaments.csv"""
    return CSVHandler("tournaments.csv")


def get_teams_handler() -> CSVHandler:
    """Get handler for teams.csv"""
    return CSVHandler("teams.csv")


def get_team_members_handler() -> CSVHandler:
    """Get handler for team_members.csv"""
    return CSVHandler("team_members.csv")


def get_avatars_handler() -> CSVHandler:
    """Get handler for avatars.csv"""
    return CSVHandler("avatars.csv")


def get_characters_handler() -> CSVHandler:
    """Get handler for characters.csv"""
    return CSVHandler("characters.csv")


def get_learning_history_handler() -> CSVHandler:
    """Get handler for learning_history.csv"""
    return CSVHandler("learning_history.csv")
