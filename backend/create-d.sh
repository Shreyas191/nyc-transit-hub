# Navigate to backend folder
cd "/Users/shreyaskaldate/Desktop/NYC Transit Hub/backend"

# Create instance directories for all services
for service in alerts-service transit-service favorites-service accessibility-service localization-service; do
    mkdir -p "$service/instance"
    echo "✓ Created instance directory for $service"
done