#!/bin/bash

# CRM HCP System Database Setup Script

echo "🗄️  Setting up CRM HCP Database..."

# PostgreSQL Setup
if command -v psql &> /dev/null
then
    echo "📝 Creating PostgreSQL database..."
    psql -U postgres -c "CREATE DATABASE crm_hcp_db;"
    echo "✅ PostgreSQL database created successfully!"
else
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL or update DATABASE_URL in .env"
fi

# MySQL Setup (Alternative)
if command -v mysql &> /dev/null
then
    echo "📝 Creating MySQL database..."
    mysql -u root -e "CREATE DATABASE crm_hcp_db;"
    echo "✅ MySQL database created successfully!"
fi

echo "🎉 Database setup complete!"
echo "Update your .env file with the correct DATABASE_URL"
