from services.csv_loader import (
    load_csv_as_2d_array,
    array2d_to_dicts,
    clear_loaded_csv_from_memory,
    delete_csv_file,
)
from services.mongo_service import (
    insert_denormalized_students,
    load_mongo_as_flat_records,
    status as mongo_status,
    delete_all_mongo_data,
    delete_one_student_mongo,
)
from services.sql_service import (
    insert_normalized,
    status as sql_status,
    delete_all_sql_data,
    delete_one_student_sql,
)

CSV_PATH = "data/enrollments.csv"


def print_menu():
    print("\n=== ADBMS ETL Console ===")
    print("1) Load CSV (2D array → dictionaries)")
    print("2) Insert MongoDB (denormalized)")
    print("3) Load data from MongoDB (flatten into dictionaries)")
    print("4) Insert MS SQL Server (normalized) from Mongo-loaded dictionaries")
    print("5) View Status (CSV memory + Mongo + SQL)")
    print("6) Delete CSV")
    print("7) Delete MongoDB (ALL data)")
    print("8) Delete MS SQL (ALL data)")
    print("9) Delete SINGLE record")
    print("0) Exit")


def get_csv_status(state: dict):
    if state["csv_dicts"] is None:
        return {"loaded": False, "rows": 0}
    return {"loaded": True, "rows": len(state["csv_dicts"])}


def print_single_delete_menu():
    print("\n--- Delete SINGLE Record ---")
    print("1) Delete single record from MongoDB")
    print("2) Delete single record from MS SQL")
    print("0) Back")


def main():
    # Central state (memory stage tracking)
    state = {
        "header": None,
        "data_2d": None,
        "csv_dicts": None,     # after CSV -> dict transform
        "mongo_dicts": None,   # after Mongo -> flatten transform
    }

    while True:
        print_menu()
        choice = input("Select option: ").strip()

        # 1) Load CSV -> 2D array -> dicts
        if choice == "1":
            header, data_2d = load_csv_as_2d_array(CSV_PATH)
            csv_dicts, summary = array2d_to_dicts(header, data_2d)

            state["header"] = header
            state["data_2d"] = data_2d
            state["csv_dicts"] = csv_dicts

            print("CSV Loaded Successfully.")
            print("2D Array shape:", (len(data_2d), len(header)))
            print("Summary:", summary)

        # 2) Insert MongoDB (denormalized) from CSV dicts
        elif choice == "2":
            if not state["csv_dicts"]:
                print("Load CSV first (Option 1).")
                continue

            inserted = insert_denormalized_students(state["csv_dicts"])
            print(f"MongoDB inserted {inserted} student documents (denormalized).")

        # 3) Load MongoDB (flatten) -> dicts in memory
        elif choice == "3":
            state["mongo_dicts"] = load_mongo_as_flat_records()
            print(f"Loaded {len(state['mongo_dicts'])} flattened records from MongoDB.")

        # 4) Insert SQL (normalized) from mongo_dicts
        elif choice == "4":
            if not state["mongo_dicts"]:
                print("Load MongoDB data first (Option 3).")
                continue

            info = insert_normalized(state["mongo_dicts"])
            print("SQL Insert Summary:", info)

        # 5) View Status (include CSV memory status)
        elif choice == "5":
            csv_status = get_csv_status(state)

            print("\n--- STATUS REPORT ---")
            if csv_status["loaded"]:
                print(f"CSV Status: LOADED in memory ({csv_status['rows']} rows)")
            else:
                print("CSV Status: REMOVED from memory")

            print("MongoDB Status:", mongo_status())
            print("SQL Server Status:", sql_status())

        # 6) Delete CSV (memory + optional file delete)
        elif choice == "6":
            print("\n--- Delete CSV ---")
            print("1) Clear CSV data from memory")
            print("2) Delete CSV file from disk")
            print("0) Back")
            sub = input("Select option: ").strip()

            if sub == "1":
                clear_loaded_csv_from_memory(state)
                print("CSV data cleared from memory.")
            elif sub == "2":
                ok = delete_csv_file(CSV_PATH)
                if ok:
                    clear_loaded_csv_from_memory(state)
                    print(f"CSV file deleted from disk: {CSV_PATH}")
                else:
                    print("CSV file not found on disk.")
            elif sub == "0":
                pass
            else:
                print("Invalid option.")

        # 7) Delete MongoDB (ALL)
        elif choice == "7":
            deleted = delete_all_mongo_data()
            # Also clear mongo-loaded memory because source is deleted
            state["mongo_dicts"] = None
            print(f"MongoDB: deleted {deleted} document(s).")

        # 8) Delete MSSQL (ALL)
        elif choice == "8":
            delete_all_sql_data()
            print("SQL Server: all data deleted from all tables.")

        # 9) Delete SINGLE record
        elif choice == "9":
            while True:
                print_single_delete_menu()
                sub = input("Select option: ").strip()

                if sub == "0":
                    break

                sid = input("Enter student_id (e.g., S001): ").strip()

                if sub == "1":
                    deleted = delete_one_student_mongo(sid)
                    # mongo_dicts may now be stale; safest is to clear it
                    state["mongo_dicts"] = None
                    print(f"MongoDB: deleted {deleted} document(s) for student_id={sid}")

                elif sub == "2":
                    delete_one_student_sql(sid)
                    print(f"SQL Server: deleted student + enrollments (if existed) for student_id={sid}")

                else:
                    print("Invalid option.")

        # 0) Exit
        elif choice == "0":
            print("Exiting application.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
