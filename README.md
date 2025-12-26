# ETL TOOL

## Overview

This project demonstrates an Advanced Database Management System (ADBMS) implementation that showcases data transformation between different database paradigms. It processes student enrollment data through a pipeline: CSV loading → MongoDB denormalized storage → data flattening → SQL Server normalized storage.

The system illustrates key database concepts including normalization, denormalization, data migration, and multi-database integration using Python.

## Features

- **CSV Data Loading**: Load enrollment data from CSV files into memory structures
- **MongoDB Integration**: Store data in denormalized documents with embedded subdocuments
- **SQL Server Integration**: Transform and store data in normalized relational tables
- **Data Pipeline**: Complete ETL (Extract, Transform, Load) workflow
- **Console Interface**: Interactive menu-driven application for data operations
- **Status Monitoring**: Real-time database status and record counts
- **Sample Data Generation**: Automated generation of realistic enrollment data

## Architecture

The project follows a data processing pipeline:

1. **CSV Input** → Flat enrollment records with all fields
2. **MongoDB Storage** → Denormalized student documents with embedded enrollments
3. **Data Flattening** → Convert back to flat records for SQL insertion
4. **SQL Server Storage** → Normalized tables (Students, Courses, Enrollments, etc.)

### Database Schemas

#### MongoDB (Denormalized)
```json
{
  "student_id": "S001",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "department": {
    "department_id": "D1",
    "name": "Computer Science"
  },
  "enrollments": [
    {
      "semester": "Spring-2025",
      "enroll_date": "2025-01-15",
      "grade": "A",
      "course": {
        "course_id": "C1",
        "title": "Database Systems",
        "credit_hours": 3
      },
      "instructor": {
        "instructor_id": "I1",
        "name": "Dr. Smith"
      }
    }
  ]
}
```

#### SQL Server (Normalized)
- **Departments**: department_id (PK), department_name
- **Students**: student_id (PK), student_name, email, phone, department_id (FK)
- **Instructors**: instructor_id (PK), instructor_name, department_id (FK)
- **Courses**: course_id (PK), course_title, credit_hours, department_id (FK), instructor_id (FK)
- **Enrollments**: student_id (FK), course_id (FK), semester, enroll_date, grade

## Prerequisites

- **Python 3.8+**
- **MongoDB** (running on localhost:27017)
- **Microsoft SQL Server** (with ODBC Driver 17 or 18)
- **Required Python packages**:
  - `pymongo` (MongoDB driver)
  - `pyodbc` (SQL Server ODBC driver)

## Installation & Setup

1. **Clone/Download the project**
   ```bash
   cd "c:/Users/IBBI/Desktop/adbms project"
   ```

2. **Install dependencies**
   ```bash
   pip install pymongo pyodbc
   ```

3. **Start MongoDB**
   - Ensure MongoDB is running on `localhost:27017`
   - Default database: `enrollment_db`
   - Default collection: `students`

4. **Setup SQL Server**
   - Ensure SQL Server is running on `localhost`
   - Create database: `EnrollmentDB`
   - Use Windows Authentication (Trusted Connection)
   - Install ODBC Driver 17 for SQL Server

5. **Generate sample data (optional)**
   ```bash
   python services/generate_csv.py
   ```
   This creates `data/enrollments.csv` with 150 sample enrollment records.

## Usage

### Running the Application

```bash
python main.py
```

### Console Menu Options

1. **Load CSV**: Load enrollment data from `data/enrollments.csv` into memory
2. **Insert MongoDB**: Store loaded data in MongoDB as denormalized documents
3. **Load from MongoDB**: Retrieve and flatten MongoDB data back to dictionaries
4. **Insert SQL Server**: Transform flattened data into normalized SQL tables
5. **View Status**: Display record counts from both databases
6. **Delete CSV**: Clear loaded data from memory

### Example Workflow

```
=== ADBMS Project Console ===
1) Load CSV (into 2D array -> dicts)
2) Insert MongoDB (denormalized) from loaded CSV dicts
3) Load data from MongoDB (flatten into dicts)
4) Insert MS SQL Server (normalized) from Mongo loaded dicts
5) View Status (Mongo + SQL)
6) Delete CSV (clear loaded CSV from memory)
0) Exit

Select option: 1
CSV Loaded Successfully.
2D Array shape: (150, 14)
Summary: {'rows': 150, 'columns': ['student_id', 'student_name', 'email', 'phone', 'department_id', 'department_name', 'course_id', 'course_title', 'credit_hours', 'instructor_id', 'instructor_name', 'semester', 'enroll_date', 'grade']}

Select option: 2
MongoDB inserted student documents (denormalized): 60

Select option: 3
Loaded and flattened 150 records from MongoDB into dictionaries.

Select option: 4
SQL Insert Summary: {'departments': 5, 'students': 60, 'instructors': 5, 'courses': 10, 'enrollments': 150}

Select option: 5
MongoDB Status: {'students_docs': 60, 'total_enrollments_embedded': 150}
SQL Server Status: {'Departments': 5, 'Students': 60, 'Instructors': 5, 'Courses': 10, 'Enrollments': 150}
```

## Project Structure

```
adbms project/
├── main.py                 # Main console application
├── config.py               # Database connection configurations
├── sql_test.py            # SQL Server connection test
├── mongo_test.py          # MongoDB connection test
├── data/
│   └── enrollments.csv    # Sample enrollment data
├── services/
│   ├── csv_loader.py      # CSV loading utilities
│   ├── generate_csv.py    # Sample data generator
│   ├── mongo_service.py   # MongoDB operations
│   └── sql_service.py     # SQL Server operations
└── README.md              # This file
```

## Key Components

### Services

- **`csv_loader.py`**: Handles CSV file reading and conversion to dictionaries
- **`mongo_service.py`**: MongoDB CRUD operations with denormalization logic
- **`sql_service.py`**: SQL Server operations with normalization and table management
- **`generate_csv.py`**: Generates realistic sample enrollment data

### Configuration

Database connections are configured in `config.py`:
- MongoDB: localhost:27017, database: enrollment_db, collection: students
- SQL Server: localhost, database: EnrollmentDB, Windows Authentication

## Testing

Run individual connection tests:

```bash
# Test MongoDB connection
python mongo_test.py

# Test SQL Server connection
python sql_test.py
```

## Data Flow

1. **CSV Loading**: Raw enrollment data loaded as list of dictionaries
2. **MongoDB Insertion**: Data grouped by student, enrollments embedded as arrays
3. **MongoDB Retrieval**: Documents flattened back to individual enrollment records
4. **SQL Insertion**: Flattened records normalized across multiple related tables

## Educational Value

This project demonstrates:
- Database design principles (normalization vs denormalization)
- ETL processes and data transformation
- Multi-database system integration
- Python database programming with different paradigms
- Real-world data modeling for educational institutions

## License

This project is for educational purposes. Feel free to modify and extend.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

- **MongoDB Connection Issues**: Ensure MongoDB is running on port 27017
- **SQL Server Connection Issues**: Verify ODBC driver installation and database permissions
- **Import Errors**: Install required packages with `pip install pymongo pyodbc`
- **Data Issues**: Regenerate sample data using `generate_csv.py` if needed
