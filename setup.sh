#!/bin/bash

echo "Setting up NYC Transit Hub Backend Services..."

# Array of services
services=("api-gateway" "transit-service" "favorites-service" "alerts-service" "accessibility-service" "localization-service")

for service in "${services[@]}"
do
    echo ""
    echo "========================================="
    echo "Setting up $service..."
    echo "========================================="
    
    cd "services/$service"
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate and install requirements
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Create instance directory
    mkdir -p instance
    
    # Initialize database
    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created for $service!')"
    
    deactivate
    cd ../..
done

echo ""
echo "✓ All services set up successfully!"
echo "Run 'python services/[service-name]/run.py' to start each service"