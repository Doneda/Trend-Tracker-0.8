import schedule
import time
import json
import os
from datetime import datetime
from html_inspector import inspect_amazon, inspect_product_hunt
from scraper import ProductScraper

class AutoUpdater:
    def __init__(self):
        self.config_file = 'selector_config.json'
        self.log_file = 'update_log.json'
        self.last_config = self.load_config()
    
    def load_config(self):
        """Load current selector configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  No config found, will create on first run")
            return None
    
    def save_log(self, event_type, message, details=None):
        """Log events to file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'message': message,
            'details': details
        }
        
        # Load existing logs
        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Append new log
        logs.append(log_entry)
        
        # Keep only last 100 logs
        logs = logs[-100:]
        
        # Save
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"📝 [{event_type}] {message}")
    
    def compare_selectors(self, old_config, new_config):
        """Compare old and new selectors to detect changes"""
        if not old_config or not new_config:
            return {'changed': True, 'reason': 'First run or missing config'}
        
        changes = []
        
        for platform in ['amazon', 'productHunt']:
            old_sel = old_config.get('platforms', {}).get(platform, {}).get('selectors', {})
            new_sel = new_config.get('platforms', {}).get(platform, {}).get('selectors', {})
            
            # Compare each selector type
            for key in set(list(old_sel.keys()) + list(new_sel.keys())):
                old_val = old_sel.get(key)
                new_val = new_sel.get(key)
                
                if old_val != new_val:
                    changes.append({
                        'platform': platform,
                        'selector': key,
                        'old': old_val,
                        'new': new_val
                    })
        
        return {
            'changed': len(changes) > 0,
            'changes': changes,
            'count': len(changes)
        }
    
    def run_inspection(self):
        """Run HTML inspection to get current selectors"""
        print("\n" + "=" * 70)
        print("🔍 AUTO-UPDATE: Running HTML Inspection")
        print("=" * 70)
        
        try:
            # Run inspectors
            amazon_results = inspect_amazon()
            time.sleep(3)
            ph_results = inspect_product_hunt()
            
            # Create new config
            new_config = {
                'inspectedAt': datetime.now().isoformat(),
                'platforms': {
                    'amazon': amazon_results,
                    'productHunt': ph_results
                }
            }
            
            return new_config
            
        except Exception as e:
            self.save_log('ERROR', f'Inspection failed: {str(e)}')
            return None
    
    def update_scraper_code(self, changes):
        """
        Update scraper.py with new selectors
        (In production, you'd dynamically update the code or config)
        """
        print("\n🔧 Selector changes detected:")
        for change in changes:
            print(f"   • {change['platform']}.{change['selector']}")
            print(f"     Old: {change['old']}")
            print(f"     New: {change['new']}")
        
        # For now, we just save the new config
        # The scraper already reads from selector_config.json
        print("\n✅ Scraper will use new selectors from selector_config.json")
    
    def run_scraper(self):
        """Run the scraper with updated config"""
        print("\n🤖 Running scraper with updated configuration...")
        
        try:
            scraper = ProductScraper(headless=True)
            products = scraper.scrape_all(amazon_count=10, ph_count=5)
            
            if products:
                scraper.save_to_json(products)
                scraper.close()
                self.save_log('SUCCESS', f'Scraped {len(products)} products')
                return True
            else:
                scraper.close()
                self.save_log('WARNING', 'Scraper returned no products')
                return False
                
        except Exception as e:
            self.save_log('ERROR', f'Scraper failed: {str(e)}')
            return False
    
    def check_and_update(self):
        """Main update check and execution"""
        print("\n" + "=" * 70)
        print(f"🔄 AUTO-UPDATE CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Run inspection
        new_config = self.run_inspection()
        
        if not new_config:
            print("❌ Inspection failed, skipping update")
            return
        
        # Compare with previous config
        comparison = self.compare_selectors(self.last_config, new_config)
        
        if comparison['changed']:
            print(f"\n🚨 CHANGES DETECTED: {comparison.get('count', 'Unknown')} selector(s) changed")
            
            # Save new config
            with open(self.config_file, 'w') as f:
                json.dump(new_config, f, indent=2)
            
            self.save_log('CHANGE_DETECTED', 
                         f"{comparison.get('count')} selectors changed", 
                         comparison.get('changes'))
            
            # Update scraper
            if comparison.get('changes'):
                self.update_scraper_code(comparison['changes'])
            
            # Run scraper with new config
            success = self.run_scraper()
            
            if success:
                print("\n✅ Update complete and data refreshed")
                self.last_config = new_config
            else:
                print("\n⚠️  Update complete but scraping had issues")
        
        else:
            print("\n✅ No changes detected - selectors still valid")
            self.save_log('NO_CHANGE', 'Selectors unchanged')
            
            # Still run scraper to refresh data
            print("\n🔄 Refreshing data with existing selectors...")
            self.run_scraper()
        
        print("\n" + "=" * 70)
        print("✅ Auto-update cycle complete")
        print("=" * 70)
    
    def start_scheduled_updates(self):
        """Start the scheduler - runs every 48 hours"""
        print("\n" + "=" * 70)
        print("🤖 AUTO-UPDATER STARTED")
        print("=" * 70)
        print("📅 Schedule: Every 48 hours")
        print("🔍 Actions:")
        print("   1. Inspect HTML structure")
        print("   2. Detect selector changes")
        print("   3. Update configuration")
        print("   4. Run scraper with new config")
        print("=" * 70)
        
        # Run immediately on start
        print("\n🚀 Running initial check...")
        self.check_and_update()
        
        # Schedule for every 48 hours
        schedule.every(48).hours.do(self.check_and_update)
        
        print("\n⏰ Next check in 48 hours")
        print("💡 Press Ctrl+C to stop\n")
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n⚠️  Auto-updater stopped by user")
            self.save_log('STOPPED', 'Auto-updater stopped manually')


def main():
    """Main execution"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    TrendTracker Auto-Updater                     ║
║                                                                  ║
║  This intelligent system will:                                  ║
║  • Monitor website structure every 48 hours                     ║
║  • Detect when HTML selectors change                            ║
║  • Automatically update scraper configuration                   ║
║  • Refresh data with new selectors                              ║
║  • Log all changes for review                                   ║
║                                                                  ║
║  This is ADVANCED automation! 🚀                                ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    choice = input("\nStart auto-updater? (y/n): ").lower()
    
    if choice == 'y':
        updater = AutoUpdater()
        updater.start_scheduled_updates()
    else:
        print("\n✋ Auto-updater not started")
        print("💡 To start: python auto_updater.py")


if __name__ == "__main__":
    main()
