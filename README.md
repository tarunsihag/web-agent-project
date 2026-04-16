# Semi-Autonomous Web Interaction Agent

A Python-based autonomous web agent that explores Wikipedia by intelligently navigating through articles, making decisions based on page content, and logging its journey.

## 🤖 Core Technologies

### LLM Integration
This project demonstrates **LLM-driven decision making** capabilities:
- **Current Implementation**: Rule-based decision logic (mock LLM behavior)
- **Architecture Ready**: Modular design allows seamless LLM integration via API
- **LLM Simulation**: Decision engine mimics intelligent reasoning patterns
- **API-Ready Structure**: Decision logic can be replaced with GPT/Claude API calls

### Python Backend
Built entirely with Python 3.12+ providing:
- **Modular Architecture**: Clean separation of concerns across multiple modules
- **Object-Oriented Design**: Classes for Agent, Decision Engine, and Logger
- **Asynchronous Capabilities**: Ready for async API calls to LLM providers
- **JSON-Based Communication**: Structured data flow suitable for REST APIs

### Selenium Web Automation
Full-featured browser automation using Selenium WebDriver:
- **Chrome WebDriver**: Programmatic browser control
- **JavaScript Execution**: Reliable element interaction
- **Screenshot Capture**: Visual documentation of agent behavior
- **Element Discovery**: Intelligent DOM traversal and filtering
- **Robust Error Handling**: Graceful fallbacks for automation failures

### REST-Style Architecture
Designed with REST principles for future API integration:
- **Stateless Operations**: Each decision is independent
- **Structured Data Exchange**: JSON for inputs/outputs
- **Clear Interfaces**: Well-defined contracts between components
- **Modular Endpoints**: Easy to expose as REST API endpoints
- **Scalable Design**: Ready for microservices architecture

## 🚀 Future Scope: GPT / Claude Integration

### Planned Enhancements

**1. LLM-Powered Decision Making**
- Replace rule-based logic with GPT-4 or Claude API calls
- Natural language reasoning for each navigation decision
- Context-aware exploration based on semantic understanding
- Dynamic goal setting and task completion

**2. Advanced Features**
- **Vision API Integration**: Use GPT-4 Vision or Claude 3 to analyze page screenshots
- **Multi-Agent Collaboration**: Multiple agents with different exploration strategies
- **Conversational Interface**: Chat with the agent to guide its exploration
- **Learning Capabilities**: Fine-tune models based on successful navigation patterns
- **Content Summarization**: Extract and summarize key insights from visited pages

**3. API-First Architecture**
- RESTful endpoints for agent control
- Webhook support for event notifications
- Real-time WebSocket updates during exploration
- OpenAPI/Swagger documentation
- Authentication and rate limiting

**4. Integration Possibilities**
```python
# Example: Future GPT Integration
decision = await openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "system",
        "content": "You are a web navigation agent..."
    }, {
        "role": "user", 
        "content": f"Current page: {page_info}. What should I do next?"
    }]
)
```

**5. Enhanced Capabilities**
- Multi-language support using LLM translation
- Sentiment analysis of content
- Fact extraction and knowledge graph building
- Adaptive behavior based on user feedback
- Integration with vector databases for semantic search

## 🏗️ Architecture

### System Overview

The project follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    (Orchestration Layer)                     │
└──────────────┬────────────────┬──────────────────────────────┘
               │                │
       ┌───────▼──────┐  ┌──────▼────────┐
       │   WebAgent   │  │ DecisionEngine│
       │  (agent.py)  │  │(decision_logic│
       │              │  │     .py)      │
       └───────┬──────┘  └──────┬────────┘
               │                │
               └────────┬───────┘
                        │
                 ┌──────▼──────┐
                 │ AgentLogger │
                 │ (logger.py) │
                 └─────────────┘
```

### Component Architecture

#### 1. **main.py** - Orchestration Layer
**Purpose**: Main entry point that coordinates all components

**Key Responsibilities**:
- Initializes all components (WebAgent, DecisionEngine, Logger)
- Manages the main execution loop
- Handles action execution based on decisions
- Coordinates error handling and graceful shutdown

**Flow**:
```
Start → Initialize Components → Open Website → Loop (Observe → Decide → Act) → Cleanup
```

#### 2. **agent.py** - Browser Control Layer
**Purpose**: Direct interaction with the web browser using Selenium

**Key Components**:
- `WebAgent` class: Main browser controller

**Methods**:
- `open_website(url)`: Opens target URL with 5-second wait
- `get_page_info()`: Extracts page metadata (title, URL, link count)
- `find_interactive_elements()`: Discovers clickable elements (buttons, links, inputs)
- `select_language(language)`: Handles language selection (if needed)
- `take_screenshot(name)`: Captures visual state for documentation
- `close()`: Clean browser shutdown

**Technical Details**:
- Uses Chrome WebDriver via Selenium
- Implements 5-second waits between all actions
- Captures up to 100 links per page for analysis
- Filters for visible and enabled elements only

#### 3. **decision_logic.py** - Intelligence Layer
**Purpose**: Makes autonomous decisions about what to do next

**Key Components**:
- `DecisionEngine` class: Decision-making brain

**Decision Rules** (Priority Order):

1. **Rule 1**: If on Wikipedia main page → Search for topic (by clicking related links)
2. **Rule 2**: If on search results → Click first valid article link
3. **Rule 3**: If on article page → Either:
   - 70% chance: Click random link to explore further
   - 30% chance: Go back to try different path
4. **Rule 4**: Default → Navigate back to English Wikipedia

**State Management**:
- Tracks visited URLs
- Maintains exploration state
- Uses randomization for varied behavior
- Predefined search terms: ["AI", "Python", "Machine Learning", "Space"]

**Decision Output Format**:
```python
{
    "action": "search" | "click" | "go_back" | "navigate",
    "target": element_or_url,
    "value": search_term (for search actions),
    "reasoning": "Human-readable explanation"
}
```

#### 4. **logger.py** - Observability Layer
**Purpose**: Comprehensive logging and tracking

**Key Components**:
- `AgentLogger` class: Event tracking and persistence

**Logging Types**:
- **Actions**: User-like interactions (clicks, navigation, search)
- **Observations**: Page states, errors, metadata

**Features**:
- JSON-formatted logs for programmatic access
- Timestamp tracking for all events
- Step numbering for execution flow
- Real-time console output
- Persistent storage to `agent_log.json`

**Log Entry Structure**:
```json
{
  "timestamp": "2026-01-05 22:00:00",
  "action": "click",
  "details": "Article link",
  "reasoning": "Exploring article...",
  "step": 1
}
```

#### 5. **config.py** - Configuration Layer
**Purpose**: Centralized configuration management

**Parameters**:
- `WEBSITE_URL`: Starting URL
- `MAX_STEPS`: Maximum actions per session (10)
- `SCREENSHOT_DIR`: Screenshot storage location
- `LOG_FILE`: Log file path

### Data Flow

```
1. Page Load
   ↓
2. Extract Page Info (title, URL, links)
   ↓
3. Find Interactive Elements (100 links, 10 buttons)
   ↓
4. Detect Issues (if any)
   ↓
5. Make Decision (based on page state + rules)
   ↓
6. Log Decision
   ↓
7. Execute Action
   - Search: Click matching/random article link
   - Click: JavaScript click with scroll
   - Navigate: Direct URL navigation
   - Go Back: Browser back button
   ↓
8. Wait 5 seconds
   ↓
9. Take Screenshot
   ↓
10. Repeat (until MAX_STEPS)
```

### Key Design Patterns

#### 1. **Strategy Pattern** (Decision Logic)
- Different strategies for different page types
- Encapsulated decision-making logic
- Easy to extend with new rules

#### 2. **Observer Pattern** (Logging)
- Logger observes all agent actions
- Decoupled logging from business logic
- Real-time event tracking

#### 3. **Facade Pattern** (WebAgent)
- Simplified interface to complex Selenium operations
- Hides browser automation complexity
- Clean API for orchestration layer

#### 4. **Command Pattern** (Actions)
- Actions represented as decision objects
- Uniform interface for different action types
- Easy to add new action types

### Error Handling Strategy

**Multi-Layer Approach**:

1. **Action Level**: Try-catch around individual actions with fallbacks
2. **Loop Level**: Catch and log errors, attempt to continue
3. **Session Level**: Graceful shutdown, save logs, close browser

**Specific Handlers**:
- Link click failures → Fallback to different link or skip
- Browser crashes → Log error and exit gracefully
- Element not found → Wait, retry, or skip
- JSON serialization → Convert objects to strings

### Performance Optimizations

1. **Smart Element Collection**: 
   - Limit to 100 links (most relevant)
   - Filter visible/enabled elements only
   - Skip navigation/system links

2. **JavaScript Execution**:
   - Use JS click for reliability
   - Scroll elements into view
   - Faster than native Selenium clicks

3. **Timed Waits**:
   - Consistent 5-second waits prevent race conditions
   - Balance between speed and reliability

4. **Screenshot Management**:
   - Timestamped filenames prevent overwrites
   - Organized in dedicated directory
   - Visual debugging aid

## 📁 Project Structure

```
autonomous-web-agent/
├── main.py              # Entry point & orchestration
├── agent.py             # Browser control & automation
├── decision_logic.py    # Decision making intelligence
├── logger.py            # Event logging & tracking
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── screenshots/         # Generated screenshots
│   └── *.png           # Timestamped captures
└── agent_log.json       # Execution logs
```

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher
- Google Chrome browser
- ChromeDriver (matching Chrome version)

### Setup

1. **Clone or download the project**
```bash
cd autonomous-web-agent
```

2. **Install dependencies**
```bash
pip install selenium
```

3. **Install ChromeDriver**
- Download from: https://chromedriver.chromium.org/
- Add to system PATH or place in project directory

## 💻 Usage

### Basic Execution

```bash
python main.py
```

### What Happens

1. Opens English Wikipedia homepage
2. Finds and clicks on article links (related to AI, Python, Machine Learning, Space)
3. Navigates through 10 steps with 5-second waits
4. Takes screenshots at each step
5. Logs all actions to `agent_log.json`
6. Gracefully closes browser and saves logs

### Output Files

- **Screenshots**: `screenshots/initial_page_HHMMSS.png`, `screenshots/step_0_HHMMSS.png`, etc.
- **Logs**: `agent_log.json` with complete execution history

## 📊 Example Output

```
=== Starting Semi-Autonomous Web Interaction Agent ===
[2026-01-05 22:00:00] Opening https://en.wikipedia.org
[INFO] Page: Wikipedia, the free encyclopedia, Links: 667
[SCREENSHOT] Saved: screenshots/initial_page_220000.png

--- Step 1/10 ---
[ACTION] Looking for article link related to: Machine Learning
[INFO] Found 44 article links
[ACTION] Clicking random article: Artificial Intelligence
[INFO] Step 1 completed successfully

--- Step 2/10 ---
[ACTION] Clicking link: Neural Network
...

=== Agent Finished ===
Total steps: 11
Actions taken: 10
Logs saved to: agent_log.json
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
WEBSITE_URL = "https://en.wikipedia.org"  # Starting URL
MAX_STEPS = 10                             # Actions per session
SCREENSHOT_DIR = "screenshots"             # Screenshot folder
LOG_FILE = "agent_log.json"               # Log file name
```

## 🎯 Features

- ✅ Autonomous navigation through Wikipedia
- ✅ Intelligent decision-making based on page content
- ✅ 5-second waits between all actions
- ✅ Automatic screenshot capture at each step
- ✅ Comprehensive JSON logging
- ✅ Error handling with graceful fallbacks
- ✅ JavaScript-based reliable clicking
- ✅ Article link filtering (skips navigation/system links)
- ✅ Random exploration for varied behavior

## 🛠️ Technical Stack

### Current Implementation
- **Language**: Python 3.12+ (Backend)
- **Browser Automation**: Selenium WebDriver (Chrome)
- **Browser**: Google Chrome with ChromeDriver
- **Data Format**: JSON for logs and data exchange
- **Image Format**: PNG for screenshots
- **Architecture**: Modular, REST-style design pattern

### LLM Integration (Future-Ready)
- **API Support**: Structured for OpenAI GPT or Anthropic Claude integration
- **Decision Logic**: Mock LLM behavior with rule-based reasoning
- **Async Ready**: Architecture supports async API calls
- **Prompt Engineering**: Designed for natural language instruction

## 📝 Extending the Agent

### Adding New Decision Rules

Edit `decision_logic.py`:

```python
def decide_next_action(self, page_info, interactive_elements):
    # Add your rule here
    if your_condition:
        return {
            "action": "your_action",
            "target": your_target,
            "reasoning": "Why this action"
        }
```

### Adding New Actions

Edit `main.py` in the action execution section:

```python
elif decision["action"] == "your_action":
    # Implement your action
    your_action_code()
    time.sleep(5)
```

### Changing Search Topics

Edit `decision_logic.py`:

```python
self.search_terms = ["Topic1", "Topic2", "Topic3", "Topic4"]
```

## 🐛 Troubleshooting

**Issue**: ChromeDriver not found
- **Solution**: Install ChromeDriver and add to PATH

**Issue**: Browser crashes during execution
- **Solution**: Check Chrome version matches ChromeDriver version

**Issue**: No article links found
- **Solution**: Check internet connection, Wikipedia may be down

**Issue**: Screenshots not saving
- **Solution**: Ensure `screenshots/` directory exists

## 📜 License

This project is open source and available for educational purposes.

## 👤 Author

Created as a demonstration of autonomous web agent architecture.

---

**Last Updated**: January 5, 2026