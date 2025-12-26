import csv

def load_csv_as_2d_array(path: str):
    """
    Returns:
      - header: list[str]
      - data_2d: list[list[str]]  (2D array)
    """
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) < 2:
        raise ValueError("CSV has no data rows.")

    header = [h.strip() for h in rows[0]]
    data_2d = [[cell.strip() for cell in row] for row in rows[1:]]
    return header, data_2d


def array2d_to_dicts(header: list[str], data_2d: list[list[str]]):
    """
    Converts 2D array rows into list of dictionaries using header as keys.
    """
    records = []
    for row in data_2d:
        # pad if row shorter than header
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        rec = {header[i]: row[i] for i in range(len(header))}
        records.append(rec)

    summary = {"rows": len(records), "columns": header}
    return records, summary
import os

def clear_loaded_csv_from_memory(state: dict):
    """
    Clears in-memory CSV data held in a shared state dict.
    Expected keys: header, data_2d, csv_dicts
    """
    state["header"] = None
    state["data_2d"] = None
    state["csv_dicts"] = None

def delete_csv_file(path: str) -> bool:
    """
    Deletes the CSV file from disk.
    Returns True if deleted, False if file not found.
    """
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def get_csv_status(state: dict):
    if state["csv_dicts"] is None:
        return {
            "loaded": False,
            "rows": 0
        }
    return {
        "loaded": True,
        "rows": len(state["csv_dicts"])
    }
def clear_csv_file_contents(path: str) -> bool:
    """
    Clears the CSV file contents but keeps the header row.
    Returns True if cleared, False if file not found or empty.
    """
    import csv
    import os

    if not os.path.exists(path):
        return False

    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return False

    header = rows[0]

    # Rewrite file with only header
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

    return True
