# main.py
from agent import WebAgent
from decision_logic import DecisionEngine
from logger import AgentLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    print("=== Starting Semi-Autonomous Web Interaction Agent ===")
    
    # Initialize components
    agent = WebAgent()
    logger = AgentLogger()
    engine = DecisionEngine(logger)
    
    try:
        # Step 1: Open English Wikipedia directly
        page_info = agent.open_website("https://en.wikipedia.org")
        logger.log_observation("page_loaded", page_info)
        
        step = 0
        max_steps = 10
        
        while step < max_steps:
            print(f"\n--- Step {step + 1}/{max_steps} ---")
            
            # Observe current page
            interactive = agent.find_interactive_elements()
            
            # Detect issues
            issues = engine.detect_issues(page_info)
            for issue in issues:
                logger.log_observation("issue_detected", issue)
            
            # Decide next action
            decision = engine.decide_next_action(page_info, interactive)
            # Convert target to string if it's a dictionary with element
            target_for_log = decision.get("target", "")
            if isinstance(target_for_log, dict) and "element" in target_for_log:
                target_for_log = target_for_log.get("text", "element")
            logger.log_action(decision["action"], target_for_log, decision["reasoning"])
            
            # Execute action
            if decision["action"] == "search":
                # Click on a link related to the search term
                try:
                    search_term = decision["value"].lower()
                    print(f"[ACTION] Looking for article link related to: {decision['value']}")
                    
                    # Filter for actual article links
                    article_links = []
                    for e in interactive:
                        if e["type"] != "links":
                            continue
                        href = e["element"].get_attribute("href") or ""
                        text = e["text"].strip()
                        
                        # Must have text, be a /wiki/ link, and not be special pages
                        if (text and len(text) > 2 and 
                            "/wiki/" in href and 
                            ":Special:" not in href and 
                            ":File:" not in href and
                            ":Help:" not in href and
                            "#" not in href.split("/wiki/")[-1] and
                            text.lower() not in ["edit", "talk", "read", "view"]):
                            article_links.append(e)
                    
                    print(f"[INFO] Found {len(article_links)} article links")
                    
                    # Try to find matching link
                    matching = [e for e in article_links if search_term in e["text"].lower()]
                    
                    if matching:
                        link = matching[0]
                        print(f"[ACTION] Clicking matching link: {link['text'][:50]}")
                    elif article_links:
                        import random
                        link = random.choice(article_links[:20])
                        print(f"[ACTION] Clicking random article: {link['text'][:50]}")
                    else:
                        print(f"[ERROR] No article links found")
                        time.sleep(5)
                    
                    if matching or article_links:
                        # Click the link with JavaScript for reliability
                        agent.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link["element"])
                        time.sleep(0.5)
                        agent.driver.execute_script("arguments[0].click();", link["element"])
                        time.sleep(5)  # 5 second wait
                    
                except Exception as e:
                    print(f"[ERROR] Link click failed: {type(e).__name__}: {str(e)[:100]}")
                    time.sleep(5)
                
            elif decision["action"] == "click":
                try:
                    decision["target"]["element"].click()
                    time.sleep(5)  # 5 second wait
                except:
                    print(f"[ERROR] Could not click element")
                    # Fallback: go back
                    agent.driver.back()
                    time.sleep(5)  # 5 second wait
                    
            elif decision["action"] == "go_back":
                agent.driver.back()
                time.sleep(5)  # 5 second wait
                
            elif decision["action"] == "navigate":
                agent.driver.get(decision["target"])
                time.sleep(5)  # 5 second wait
            
            # Update page info
            try:
                page_info = agent.get_page_info()
                agent.take_screenshot(f"step_{step}")
                print(f"[INFO] Step {step+1} completed successfully")
            except Exception as e:
                print(f"[ERROR] Failed to update page info: {e}")
                import traceback
                traceback.print_exc()
                break
            
            step += 1
            
    except Exception as e:
        print(f"[ERROR] Agent encountered an error: {e}")
        import traceback
        traceback.print_exc()
        logger.log_observation("error", str(e))
        
    finally:
        # Generate summary
        summary = logger.get_summary()
        print("\n=== Agent Finished ===")
        print(f"Total steps: {summary['total_steps']}")
        print(f"Actions taken: {summary['actions_taken']}")
        
        # Save final logs
        logger.save_logs()
        
        # Close browser
        agent.close()
        
        print("\nLogs saved to: agent_log.json")
        print("Screenshots saved to: screenshots/")

if __name__ == "__main__":
    main()