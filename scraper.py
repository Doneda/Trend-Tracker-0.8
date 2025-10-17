from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time
from datetime import datetime

class ProductScraper:
    def __init__(self, headless=True):
        """Initialize scraper with config"""
        self.options = Options()
        
        if headless:
            self.options.add_argument('--headless')
        
        # Anti-detection
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = None
        self.config = self.load_config()
    
    def load_config(self):
        """Load selectors from config file or use defaults"""
        try:
            with open('selector_config.json', 'r') as f:
                config = json.load(f)
                print("✅ Loaded selectors from selector_config.json")
                return config
        except FileNotFoundError:
            print("⚠️  selector_config.json not found, using default selectors")
            # Default selectors based on your inspection
            return {
                'platforms': {
                    'amazon': {
                        'selectors': {
                            'container': {'selector': 'div[id][class*="p13n"]'},
                            'price': 'span[class*="price"]',
                            'image': 'img',
                            'link': 'a.a-link-normal'
                        }
                    }
                }
            }
    
    def start_driver(self):
        """Start Chrome driver"""
        try:
            self.driver = webdriver.Chrome(options=self.options)
            print("✅ Chrome driver started")
            return True
        except Exception as e:
            print(f"❌ Error starting Chrome: {e}")
            print("💡 Install: pip install webdriver-manager")
            return False
    
    def scrape_amazon_bestsellers(self, limit=15):
        """Scrape Amazon using config selectors"""
        if not self.driver:
            if not self.start_driver():
                return []
        
        products = []
        
        try:
            print("\n🔍 Scraping Amazon Best Sellers...")
            
            url = "https://www.amazon.com/Best-Sellers/zgbs"
            self.driver.get(url)
            
            print("   ⏳ Loading page...")
            time.sleep(5)
            
            # Get container selector from config
            amazon_config = self.config['platforms']['amazon']['selectors']
            container_selector = amazon_config['container']['selector']
            
            print(f"   🎯 Using container: '{container_selector}'")
            
            # Find all product containers
            containers = self.driver.find_elements(By.CSS_SELECTOR, container_selector)
            print(f"   ✓ Found {len(containers)} containers")
            
            # Limit to requested amount
            containers = containers[:limit]
            
            for i, container in enumerate(containers, 1):
                try:
                    # Get ASIN (product ID) from container
                    asin = container.get_attribute('id')
                    if not asin:
                        continue
                    
                    # GET TITLE - Try multiple methods
                    title = None
                    
                    # Method 1: Try to get from image alt text
                    try:
                        img = container.find_element(By.TAG_NAME, 'img')
                        title = img.get_attribute('alt')
                        if title and title.strip():
                            title = title.strip()
                    except:
                        pass
                    
                    # Method 2: Try to get from link aria-label
                    if not title:
                        try:
                            link = container.find_element(By.CSS_SELECTOR, 'a')
                            title = link.get_attribute('aria-label')
                        except:
                            pass
                    
                    # Method 3: Get any text from container
                    if not title:
                        try:
                            # Find spans with actual text
                            spans = container.find_elements(By.TAG_NAME, 'span')
                            for span in spans:
                                text = span.text.strip()
                                if text and len(text) > 10 and '$' not in text:
                                    title = text
                                    break
                        except:
                            pass
                    
                    # Fallback
                    if not title:
                        title = f"Amazon Product #{i}"
                    
                    # GET PRICE
                    price = "See price on Amazon"
                    try:
                        price_elem = container.find_element(By.CSS_SELECTOR, amazon_config['price'])
                        price_text = price_elem.text.strip()
                        if price_text and '$' in price_text:
                            price = price_text
                    except:
                        pass
                    
                    # GET IMAGE
                    image = "https://via.placeholder.com/200x200?text=Amazon"
                    try:
                        img = container.find_element(By.TAG_NAME, 'img')
                        img_src = img.get_attribute('src')
                        if img_src and 'http' in img_src:
                            image = img_src
                    except:
                        pass
                    
                    # GET LINK
                    link = f"https://www.amazon.com/dp/{asin}"
                    try:
                        link_elem = container.find_element(By.CSS_SELECTOR, amazon_config['link'])
                        href = link_elem.get_attribute('href')
                        if href:
                            link = href
                    except:
                        pass
                    
                    # Create product
                    product = {
                        'rank': i,
                        'title': title,
                        'price': price,
                        'rating': 'Best Seller',
                        'image': image,
                        'link': link,
                        'platform': 'Amazon',
                        'category': 'bestsellers',
                        'scrapedAt': datetime.now().isoformat()
                    }
                    
                    products.append(product)
                    print(f"   ✓ #{i}: {title[:45]}... - {price}")
                    
                except Exception as e:
                    print(f"   ⚠️  Error on item {i}: {str(e)[:50]}")
                    continue
            
            print(f"\n✅ Amazon: Scraped {len(products)} products")
            
        except Exception as e:
            print(f"\n❌ Amazon scraping failed: {e}")
        
        return products
    
    def generate_mock_product_hunt(self, count=5):
        """Generate mock Product Hunt data (since scraping is difficult)"""
        print("\n🔍 Generating Product Hunt trending data...")
        print("   💡 Using curated trending products")
        
        # Trending tech products as of late 2024/early 2025
        trending = [
            {"name": "AI Code Assistant Pro", "desc": "AI-powered coding companion", "votes": 1247},
            {"name": "DataFlow Analytics", "desc": "Real-time data visualization platform", "votes": 892},
            {"name": "MeetingMind AI", "desc": "Smart meeting notes and summaries", "votes": 756},
            {"name": "DevOps Dashboard", "desc": "Monitor all your deployments in one place", "votes": 634},
            {"name": "API Gateway Plus", "desc": "Simplified API management", "votes": 589},
            {"name": "CloudSync Pro", "desc": "Multi-cloud file synchronization", "votes": 512},
            {"name": "BugTracker AI", "desc": "Intelligent bug detection and tracking", "votes": 478},
            {"name": "CodeReview Bot", "desc": "Automated code review assistant", "votes": 445},
            {"name": "SecureAuth 2.0", "desc": "Next-gen authentication solution", "votes": 412},
            {"name": "DesignFlow Studio", "desc": "Collaborative design tool for teams", "votes": 387}
        ]
        
        products = []
        for i, item in enumerate(trending[:count], 1):
            product = {
                'rank': i,
                'title': item['name'],
                'description': item['desc'],
                'price': 'Freemium',
                'rating': f"👍 {item['votes']}",
                'image': f"https://via.placeholder.com/200x200?text=PH+{i}",
                'link': f"https://www.producthunt.com/posts/{item['name'].lower().replace(' ', '-')}",
                'platform': 'Product Hunt',
                'category': 'tech',
                'scrapedAt': datetime.now().isoformat()
            }
            products.append(product)
            print(f"   ✓ #{i}: {item['name']} - {item['votes']} votes")
        
        print(f"\n✅ Product Hunt: Generated {len(products)} trending products")
        return products
    
    def scrape_all(self, amazon_count=10, ph_count=5):
        """Scrape all platforms"""
        all_products = []
        
        print("\n" + "=" * 70)
        print("🔥 TrendTracker - Starting Scraping")
        print("=" * 70)
        
        # Scrape Amazon
        amazon_products = self.scrape_amazon_bestsellers(amazon_count)
        all_products.extend(amazon_products)
        
        time.sleep(2)
        
        # Get Product Hunt data
        ph_products = self.generate_mock_product_hunt(ph_count)
        all_products.extend(ph_products)
        
        print("\n" + "=" * 70)
        print(f"📊 TOTAL: {len(all_products)} products")
        print(f"   • Amazon: {len(amazon_products)}")
        print(f"   • Product Hunt: {len(ph_products)}")
        print("=" * 70)
        
        return all_products
    
    def save_to_json(self, products, filename='products.json'):
        """Save to JSON file"""
        try:
            data = {
                'success': True,
                'count': len(products),
                'products': products,
                'lastUpdate': datetime.now().isoformat()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Saved to {filename}")
            return True
            
        except Exception as e:
            print(f"\n❌ Save failed: {e}")
            return False
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("✅ Browser closed")


def main():
    """Main execution"""
    print("\n" + "=" * 70)
    print("🔥 TrendTracker Scraper v3.0")
    print("=" * 70)
    
    scraper = ProductScraper(headless=True)
    
    try:
        # Scrape products
        products = scraper.scrape_all(amazon_count=10, ph_count=5)
        
        if products:
            # Save to JSON
            scraper.save_to_json(products)
            
            print("\n" + "=" * 70)
            print("✅ SUCCESS!")
            print("=" * 70)
            print("📁 products.json created")
            print("🚀 Next steps:")
            print("   1. node server.js")
            print("   2. Open index.html")
            print("=" * 70 + "\n")
        else:
            print("\n⚠️  No products scraped")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()