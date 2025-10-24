DROP TABLE IF EXISTS voters CASCADE;
DROP TABLE IF EXISTS residents CASCADE;
DROP TABLE IF EXISTS counties CASCADE;
DROP TABLE IF EXISTS residential_addresses CASCADE;

CREATE TABLE counties (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    number TEXT UNIQUE NOT NULL
);

CREATE TABLE residential_addresses (
    id SERIAL PRIMARY KEY,
    county_id INT NOT NULL REFERENCES counties(id),
    address TEXT,
    unit_number TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    zip_code_plus4 TEXT,
    country TEXT,
    postal_code TEXT
);

CREATE TABLE residents (
    id SERIAL PRIMARY KEY,
    residential_address_id INT NOT NULL REFERENCES residential_addresses(id),
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    name_suffix TEXT,
    date_of_birth TEXT
    
);

CREATE TABLE voters (
    id SERIAL PRIMARY KEY,
    voter_id TEXT,
    resident_id INT NOT NULL REFERENCES residents(id)
);