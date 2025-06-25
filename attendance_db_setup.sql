-- attendance_db_setup.sql

-- IMPORTANT: Replace 'your_secure_password' with a strong password of your choice.
-- Ensure this password matches the DB_PASS in your app.py Flask file.

-- 1. Create the database
-- If the database already exists, this command will throw an error.
-- You can optionally add 'DROP DATABASE IF EXISTS attendance_db;' before this,
-- but be extremely careful as it will delete all existing data.
CREATE DATABASE attendance_db;

-- 2. Create a new user (recommended for security)
-- If the user already exists, this will throw an error.
CREATE USER attendance_user WITH PASSWORD 'abhash';

-- 3. Grant privileges on the database to the new user
GRANT ALL PRIVILEGES ON DATABASE attendance_db TO attendance_user;

-- 4. Connect to the newly created database
-- This command is for psql. If running from another client like pgAdmin,
-- you would connect to the database first, then run the table creation commands.
\c attendance_db;

-- 5. Create the 'users' table to store enrolled individuals
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    -- Store face encoding as TEXT, which will be a JSON string representation of the numpy array
    encoding TEXT NOT NULL
);

-- 6. Create the 'attendance' table to log attendance records
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Add an index for faster lookups on user_id in attendance table
CREATE INDEX idx_attendance_user_id ON attendance (user_id);

-- Optional: Add an index for faster lookups on timestamp in attendance table
CREATE INDEX idx_attendance_timestamp ON attendance (timestamp DESC);

-- You can also set ownership for better security if desired
ALTER TABLE users OWNER TO attendance_user;
ALTER TABLE attendance OWNER TO attendance_user;
ALTER DATABASE attendance_db OWNER TO attendance_user;

-- Confirmation message
SELECT 'Database and tables created successfully for attendance_db!' AS status;
