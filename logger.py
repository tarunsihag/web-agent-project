# logger.py
import json
from datetime import datetime

class AgentLogger:
    def __init__(self, log_file="agent_log.json"):
        self.log_file = log_file
        self.logs = []
        
    def log_action(self, action_type, details, reasoning=""):
        """Log an action with reasoning"""
        log_entry = {
            "timestamp": str(datetime.now()),
            "action": action_type,
            "details": details,
            "reasoning": reasoning,
            "step": len(self.logs) + 1
        }
        self.logs.append(log_entry)
        print(f"[LOG] Step {log_entry['step']}: {action_type} - {reasoning}")
        self.save_logs()
    
    def log_observation(self, observation_type, data):
        """Log something observed"""
        log_entry = {
            "timestamp": str(datetime.now()),
            "type": "observation",
            "observation": observation_type,
            "data": data
        }
        self.logs.append(log_entry)
        print(f"[OBSERVATION] {observation_type}: {data}")
    
    def save_logs(self):
        """Save logs to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
    
    def get_summary(self):
        """Generate simple summary"""
        actions = [log for log in self.logs if log.get("type") != "observation"]
        return {
            "total_steps": len(self.logs),
            "actions_taken": len(actions),
            "last_action": actions[-1] if actions else None
        }