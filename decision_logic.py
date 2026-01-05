# decision_logic.py
import random

class DecisionEngine:
    def __init__(self, logger):
        self.logger = logger
        self.state = "start"  # start, searching, exploring, error
        self.visited_urls = []
        self.search_terms = ["AI", "Python", "Machine Learning", "Space"]
        
    def decide_next_action(self, page_info, interactive_elements):
        """Decide what to do next based on current page"""
        
        # Rule 1: If on Wikipedia English main page, search for something
        if "en.wikipedia.org" in page_info["url"] and "Wikipedia" in page_info["title"] and "free encyclopedia" in page_info["title"]:
            term = random.choice(self.search_terms)
            self.state = "searching"
            return {
                "action": "search",
                "target": "search_input",
                "value": term,
                "reasoning": f"On main page. Searching for '{term}' to explore content."
            }
        
        # Rule 2: If on search results, click first valid link
        elif "Search" in page_info["title"]:
            # Find first article link (not language links, not images)
            article_links = [e for e in interactive_elements 
                           if e["type"] == "links" 
                           and "mw-redirect" not in str(e.get("class", ""))
                           and e["text"].strip()]
            
            if article_links:
                link = article_links[0]
                self.state = "exploring"
                return {
                    "action": "click",
                    "target": link,
                    "reasoning": f"On search results. Clicking first article: {link['text'][:30]}"
                }
        
        # Rule 3: If on article page, either click random link or go back
        elif len(page_info["title"].split(" - ")) > 1:  # Article page pattern
            if random.random() < 0.7:  # 70% chance to explore further
                valid_links = [e for e in interactive_elements 
                             if e["type"] == "links" 
                             and e["text"].strip()
                             and "//" not in e.get("text", "")]  # Avoid external links
                
                if valid_links:
                    link = random.choice(valid_links[:5])  # Pick from first 5
                    return {
                        "action": "click",
                        "target": link,
                        "reasoning": f"Exploring article. Clicking link: {link['text'][:30]}"
                    }
            
            # 30% chance to go back or search again
            self.state = "searching"
            return {
                "action": "go_back",
                "reasoning": "Random decision to go back and try different path."
            }
        
        # Rule 4: Default - search on English Wikipedia instead of going back to main
        return {
            "action": "navigate",
            "target": "https://en.wikipedia.org",
            "reasoning": "Default action: Return to English Wikipedia main."
        }
    
    def detect_issues(self, page_info):
        """Simple issue detection"""
        issues = []
        
        # Check for error indicators
        if page_info["text_length"] < 1000:
            issues.append("Page seems very short - possible loading issue")
        
        error_indicators = ["404", "Error", "Not Found", "Page doesn't exist"]
        page_text = ""  # Would extract from driver in real implementation
        
        for indicator in error_indicators:
            if indicator in page_info["title"]:
                issues.append(f"Error detected: {indicator}")
                
        return issues