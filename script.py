import csv
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os

load_dotenv()


db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "host": os.getenv("DB_HOST")
}

try:
    with psycopg2.connect(**db_config) as connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            file_path = "voter-file.csv"
            county_query = "SELECT id, number FROM counties"
            cursor.execute(county_query)
            counties = {}
            for county in cursor.fetchall():
                counties[county["number"]] = {
                    "id": county["id"]
                }
            with open(file_path, newline='', encoding='utf-8') as voter_file:
                reader = csv.DictReader(voter_file)
                for row in reader:
                    
                    # Address insertion

                    county_id = counties[row["COUNTY_NUMBER"]]["id"] 
                    address = row["RESIDENTIAL_ADDRESS1"]
                    unit_number = row["RESIDENTIAL_SECONDARY_ADDR"] or None
                    city = row["RESIDENTIAL_CITY"]
                    state = row["RESIDENTIAL_STATE"]
                    zip_code = row["RESIDENTIAL_ZIP"]
                    zip_code_plus4 = row["RESIDENTIAL_ZIP_PLUS4"] or None
                    country = row["RESIDENTIAL_COUNTRY"] or None
                    postal_code = row["RESIDENTIAL_POSTALCODE"] or None

                    address_query = """
                    INSERT INTO residential_addresses (county_id, address, unit_number, city, state, zip_code, zip_code_plus4, country, postal_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """
                    address_values = [county_id, address, unit_number, city, state, zip_code, zip_code_plus4, country, postal_code]
                    cursor.execute(address_query, address_values)
                    
                    # Resident insertion

                    residential_address_id = cursor.fetchone()[0]
                    first_name = row["FIRST_NAME"]
                    middle_name = row["MIDDLE_NAME"] or None
                    last_name = row["LAST_NAME"]
                    name_suffix = row["SUFFIX"] or None
                    date_of_birth = row["DATE_OF_BIRTH"]

                    resident_query = """
                    INSERT INTO residents (residential_address_id, first_name,  middle_name, last_name, name_suffix, date_of_birth)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """
                    resident_values = [residential_address_id, first_name, middle_name, last_name, name_suffix, date_of_birth]
                    cursor.execute(resident_query, resident_values)

                    # Voter insertion

                    voter_id = row["SOS_VOTERID"]
                    resident_id = cursor.fetchone()[0]

                    voter_query = """
                    INSERT INTO voters (voter_id, resident_id)
                    VALUES (%s, %s)
                    """
                    voter_values = [voter_id, resident_id]
                    cursor.execute(voter_query, voter_values)

                    # Table verification

                cursor.execute("SELECT * FROM counties")
                county_rows = cursor.fetchall()

                cursor.execute("SELECT * FROM residential_addresses")
                addresses_rows = cursor.fetchall()

                cursor.execute("SELECT * FROM residents")
                residents_rows = cursor.fetchall()

                cursor.execute("SELECT * FROM voters")
                voters_rows = cursor.fetchall()

                print()
                print("County Table")
                print()
                for row in county_rows:
                    print(row)
                print()
                print("Residential Address Table")
                print()
                for row in addresses_rows:
                    print(row)
                print()
                print("Residents Table")
                print()
                for row in residents_rows:
                    print(row)
                print()
                print("Voters Table")
                print()
                for row in voters_rows:
                    print(row)
                print()
                    
except (FileNotFoundError, PermissionError, OSError) as file_err:
    print("File error:", file_err)
except csv.Error as csv_err:
    print("CSV parsing error:", csv_err)
except (psycopg2.IntegrityError,
        psycopg2.DataError,
        psycopg2.ProgrammingError,
        psycopg2.DatabaseError) as db_err:
    print("Database error:", db_err)
except Exception as e:
    print("Unexpected error:", e)





