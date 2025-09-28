-- This script runs when the container starts for the first time
-- Grant additional permissions if needed
GRANT ALL PRIVILEGES ON DATABASE property_valuation TO django_user;

-- Create extensions that might be useful later
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "postgis"; -- For geographic data (optional)