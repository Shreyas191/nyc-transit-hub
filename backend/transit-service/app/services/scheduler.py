from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(app):
    """Start background scheduler for periodic updates"""
    scheduler = BackgroundScheduler()
    
    def update_job():
        with app.app_context():
            print(f"Background job running - Real-time data is fetched on-demand via API")
    
    # Optional: You can add background jobs here if needed
    # For now, real-time data is fetched on-demand when API is called
    
    scheduler.start()
    print("Transit Service scheduler started")