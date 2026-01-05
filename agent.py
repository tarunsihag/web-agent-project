# agent.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from datetime import datetime

class WebAgent:
    def __init__(self):
        self.driver = webdriver.Chrome()  # Make sure chromedriver is in PATH
        self.current_url = ""
        self.step_count = 0
        self.logs = []
        
    def open_website(self, url):
        """Open the target website"""
        print(f"[{datetime.now()}] Opening {url}")
        self.driver.get(url)
        self.current_url = url
        time.sleep(5)  # Wait for page load (increased to 5 seconds)
        self.take_screenshot("initial_page")
        return self.get_page_info()
    
    def get_page_info(self):
        """Extract basic page information"""
        info = {
            "title": self.driver.title,
            "url": self.driver.current_url,
            "timestamp": str(datetime.now()),
            "text_length": len(self.driver.page_source),
            "has_search": bool(self.driver.find_elements(By.TAG_NAME, "input")),
            "links_count": len(self.driver.find_elements(By.TAG_NAME, "a"))
        }
        print(f"[INFO] Page: {info['title']}, Links: {info['links_count']}")
        return info
    
    def take_screenshot(self, name):
        """Save screenshot for documentation"""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        filename = f"screenshots/{name}_{datetime.now().strftime('%H%M%S')}.png"
        self.driver.save_screenshot(filename)
        print(f"[SCREENSHOT] Saved: {filename}")
    
    def select_language(self, language="en"):
        """Select language on Wikipedia's language page"""
        try:
            print(f"[ACTION] Attempting to select {language} language...")
            # Try to find English language link
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                # Check if link contains language identifier
                href = link.get_attribute("href") or ""
                text = link.text.lower()
                
                if language == "en" and ("en.wikipedia.org" in href or text == "english"):
                    print(f"[ACTION] Found {language} link: {link.text}")
                    link.click()
                    time.sleep(5)  # Wait after language selection
                    try:
                        # Verify driver is still responsive
                        title = self.driver.title
                        self.take_screenshot("after_language_selection")
                        print(f"[INFO] Successfully navigated to: {title}")
                    except Exception as screenshot_error:
                        print(f"[WARNING] Screenshot/verification failed: {screenshot_error}")
                    return True
            
            print(f"[WARNING] Could not find {language} language link")
            return False
        except Exception as e:
            print(f"[ERROR] Language selection failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def close(self):
        """Clean shutdown"""
        self.driver.quit()
        print("[AGENT] Browser closed")
    
    def find_interactive_elements(self):
        """Find all clickable/usable elements"""
        elements = {
            "buttons": self.driver.find_elements(By.TAG_NAME, "button"),
            "links": self.driver.find_elements(By.TAG_NAME, "a"),
            "inputs": self.driver.find_elements(By.TAG_NAME, "input"),
            "forms": self.driver.find_elements(By.TAG_NAME, "form"),
        }
        
        # Filter to visible/usable elements
        interactive = []
        for elem_type, elem_list in elements.items():
            # For links, get more elements (first 100) since we need article links
            limit = 100 if elem_type == "links" else 10
            for elem in elem_list[:limit]:
                if elem.is_displayed() and elem.is_enabled():
                    text = elem.text[:50] if elem.text else elem.get_attribute("id") or elem.get_attribute("class")
                    interactive.append({
                        "type": elem_type,
                        "text": text,
                        "id": elem.get_attribute("id"),
                        "class": elem.get_attribute("class"),
                        "element": elem
                    })
        return interactive