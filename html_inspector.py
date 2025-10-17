from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime

def setup_driver(headless=False):
    """Setup Chrome driver with anti-detection"""
    options = Options()
    if headless:
        options.add_argument('--headless')
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    return webdriver.Chrome(options=options)

def inspect_amazon():
    """Inspect Amazon and find working selectors"""
    print("=" * 70)
    print("🔍 AMAZON BEST SELLERS - HTML INSPECTOR")
    print("=" * 70)
    
    driver = setup_driver(headless=False)
    results = {
        'platform': 'Amazon',
        'url': 'https://www.amazon.com/Best-Sellers/zgbs',
        'inspectedAt': datetime.now().isoformat(),
        'selectors': {}
    }
    
    try:
        url = "https://www.amazon.com/Best-Sellers/zgbs"
        print(f"\n📍 Loading: {url}")
        driver.get(url)
        
        print("⏳ Waiting 5 seconds for page to load...")
        time.sleep(5)
        
        print("\n" + "=" * 70)
        print("🔎 TESTING PRODUCT CONTAINER SELECTORS")
        print("=" * 70)
        
        # Test different container selectors
        container_selectors = [
            '.p13n-sc-uncoverable-faceout',
            '[data-asin]',
            '.zg-carousel-general-faceout',
            '.zg-grid-general-faceout',
            '.zg-item-immersion',
            'div[id][class*="p13n"]'
        ]
        
        best_container = None
        max_elements = 0
        
        for selector in container_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                count = len(elements)
                
                status = "✅" if count > 0 else "❌"
                print(f"{status} '{selector}': {count} elements")
                
                if count > max_elements:
                    max_elements = count
                    best_container = selector
                    
                    # Save first element HTML for analysis
                    if count > 0:
                        results['selectors']['container'] = {
                            'selector': selector,
                            'count': count,
                            'sample_html': elements[0].get_attribute('outerHTML')[:800]
                        }
                
            except Exception as e:
                print(f"❌ '{selector}': Error - {str(e)}")
        
        if best_container:
            print(f"\n✨ BEST CONTAINER: '{best_container}' ({max_elements} elements)")
            
            # Now test child selectors within best container
            print("\n" + "=" * 70)
            print("🔎 TESTING CHILD SELECTORS (Title, Price, Image, Link)")
            print("=" * 70)
            
            containers = driver.find_elements(By.CSS_SELECTOR, best_container)[:3]  # Test first 3
            
            # Test title selectors
            title_selectors = [
                'span.aok-inline-block',
                '.p13n-sc-truncate',
                'span[class*="truncate"]',
                'div[class*="title"]',
                'img[alt]'  # Sometimes title is in image alt
            ]
            
            print("\n📝 TITLE SELECTORS:")
            for selector in title_selectors:
                found_count = 0
                for container in containers:
                    try:
                        elem = container.find_element(By.CSS_SELECTOR, selector)
                        if elem.text.strip() or elem.get_attribute('alt'):
                            found_count += 1
                    except:
                        pass
                
                status = "✅" if found_count > 0 else "❌"
                print(f"{status} '{selector}': Found in {found_count}/3 containers")
                
                if found_count > 0 and 'title' not in results['selectors']:
                    results['selectors']['title'] = selector
            
            # Test price selectors
            price_selectors = [
                '.a-price .a-offscreen',
                '.p13n-sc-price',
                'span[class*="price"]',
                '.a-price-whole'
            ]
            
            print("\n💰 PRICE SELECTORS:")
            for selector in price_selectors:
                found_count = 0
                for container in containers:
                    try:
                        elem = container.find_element(By.CSS_SELECTOR, selector)
                        if elem.text.strip() or elem.get_attribute('textContent'):
                            found_count += 1
                    except:
                        pass
                
                status = "✅" if found_count > 0 else "❌"
                print(f"{status} '{selector}': Found in {found_count}/3 containers")
                
                if found_count > 0 and 'price' not in results['selectors']:
                    results['selectors']['price'] = selector
            
            # Test image selectors
            print("\n🖼️  IMAGE SELECTORS:")
            for container in containers:
                try:
                    img = container.find_element(By.TAG_NAME, 'img')
                    print(f"✅ 'img': Found - src exists")
                    results['selectors']['image'] = 'img'
                    break
                except:
                    pass
            
            # Test link selectors
            print("\n🔗 LINK SELECTORS:")
            for container in containers:
                try:
                    link = container.find_element(By.CSS_SELECTOR, 'a.a-link-normal')
                    print(f"✅ 'a.a-link-normal': Found")
                    results['selectors']['link'] = 'a.a-link-normal'
                    break
                except:
                    pass
        
        print("\n" + "=" * 70)
        print("📊 AMAZON INSPECTION COMPLETE")
        print("=" * 70)
        
        input("\n⏸️  Press Enter to close browser and continue...")
        
    except Exception as e:
        print(f"\n❌ Error during inspection: {e}")
    finally:
        driver.quit()
    
    return results

def inspect_product_hunt():
    """Inspect Product Hunt and find working selectors"""
    print("\n\n")
    print("=" * 70)
    print("🔍 PRODUCT HUNT - HTML INSPECTOR")
    print("=" * 70)
    
    driver = setup_driver(headless=False)
    results = {
        'platform': 'Product Hunt',
        'url': 'https://www.producthunt.com/',
        'inspectedAt': datetime.now().isoformat(),
        'selectors': {}
    }
    
    try:
        url = "https://www.producthunt.com/"
        print(f"\n📍 Loading: {url}")
        driver.get(url)
        
        print("⏳ Waiting 5 seconds for page to load...")
        time.sleep(5)
        
        print("\n" + "=" * 70)
        print("🔎 TESTING PRODUCT CONTAINER SELECTORS")
        print("=" * 70)
        
        # Test different container selectors
        container_selectors = [
            'article',
            'div[data-test*="post"]',
            '[class*="Post"]',
            'div[class*="item"]',
            'section article'
        ]
        
        best_container = None
        max_elements = 0
        
        for selector in container_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                count = len(elements)
                
                status = "✅" if count > 0 else "❌"
                print(f"{status} '{selector}': {count} elements")
                
                if count > max_elements:
                    max_elements = count
                    best_container = selector
                    
                    if count > 0:
                        results['selectors']['container'] = {
                            'selector': selector,
                            'count': count,
                            'sample_html': elements[0].get_attribute('outerHTML')[:800]
                        }
                
            except Exception as e:
                print(f"❌ '{selector}': Error - {str(e)}")
        
        if best_container:
            print(f"\n✨ BEST CONTAINER: '{best_container}' ({max_elements} elements)")
            
            print("\n" + "=" * 70)
            print("🔎 TESTING CHILD SELECTORS")
            print("=" * 70)
            
            containers = driver.find_elements(By.CSS_SELECTOR, best_container)[:5]
            
            # Test title selectors
            title_selectors = [
                'h3',
                'h2',
                'h1',
                'a[href*="/posts/"]',
                '[class*="title"]'
            ]
            
            print("\n📝 TITLE SELECTORS:")
            for selector in title_selectors:
                found_count = 0
                for container in containers:
                    try:
                        elem = container.find_element(By.CSS_SELECTOR, selector)
                        if elem.text.strip():
                            found_count += 1
                    except:
                        pass
                
                status = "✅" if found_count > 0 else "❌"
                print(f"{status} '{selector}': Found in {found_count}/5 containers")
                
                if found_count > 0 and 'title' not in results['selectors']:
                    results['selectors']['title'] = selector
            
            # Test description
            print("\n📄 DESCRIPTION SELECTORS:")
            desc_selectors = ['p', 'span[class*="tagline"]', 'div[class*="description"]']
            for selector in desc_selectors:
                found_count = 0
                for container in containers:
                    try:
                        elem = container.find_element(By.CSS_SELECTOR, selector)
                        if elem.text.strip():
                            found_count += 1
                    except:
                        pass
                
                status = "✅" if found_count > 0 else "❌"
                print(f"{status} '{selector}': Found in {found_count}/5 containers")
                
                if found_count > 0 and 'description' not in results['selectors']:
                    results['selectors']['description'] = selector
            
            # Test link
            print("\n🔗 LINK SELECTORS:")
            for container in containers:
                try:
                    link = container.find_element(By.TAG_NAME, 'a')
                    print(f"✅ 'a': Found")
                    results['selectors']['link'] = 'a'
                    break
                except:
                    pass
        
        print("\n" + "=" * 70)
        print("📊 PRODUCT HUNT INSPECTION COMPLETE")
        print("=" * 70)
        
        input("\n⏸️  Press Enter to close browser...")
        
    except Exception as e:
        print(f"\n❌ Error during inspection: {e}")
    finally:
        driver.quit()
    
    return results

def save_results(amazon_results, ph_results):
    """Save inspection results to JSON"""
    data = {
        'inspectedAt': datetime.now().isoformat(),
        'platforms': {
            'amazon': amazon_results,
            'productHunt': ph_results
        }
    }
    
    with open('selector_config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 70)
    print("💾 RESULTS SAVED TO: selector_config.json")
    print("=" * 70)
    print("\nUse this file to update your scraper automatically!")

def main():
    print("\n")
    print("=" * 70)
    print("🔥 HTML INSPECTOR - Amazon & Product Hunt")
    print("=" * 70)
    print("\nThis tool will:")
    print("1. Open each website in a browser")
    print("2. Test different CSS selectors")
    print("3. Find which ones work")
    print("4. Save results to selector_config.json")
    print("\n" + "=" * 70)
    
    input("\nPress Enter to start inspection...")
    
    # Inspect both platforms
    amazon_results = inspect_amazon()
    ph_results = inspect_product_hunt()
    
    # Save to JSON
    save_results(amazon_results, ph_results)
    
    print("\n✅ Inspection complete! Check selector_config.json")
    print("📋 Copy the working selectors to your scraper.py")

if __name__ == "__main__":
    main()