# 🤖 AI Multiple Agent

A **Python multi-agent system** where a **Manager agent** coordinates three specialised worker agents — **Research**, **Coding** and **Reviewer**. The manager (an LLM) decides which worker should act next, and the loop continues until the reviewer approves the code or the revision limit is reached.

The project also includes the pieces a real agent system needs around the LLM: centralised configuration, a shared LLM client with retries and timeouts, input validation, per-agent tool permissions and logging.

---

## 🚀 Features

### 🧭 Manager Agent

- Reads the shared state (task, research, code, review, history, revision count)
- Decides **only the next worker** and returns a single word: `research`, `coding`, `review` or `finish`
- Stops when the review is `approved` or when `MAX_REVISIONS` is reached
- Raises a clear `Unknown worker` error if the model returns anything else

### 🔎 Research Agent

- Gathers important concepts, key facts and relevant examples for the task
- Keeps the output concise so the coding agent can use it directly

### 💻 Coding Agent

- Writes Python code from the task and the research
- On later rounds it also receives the reviewer's feedback and corrects the reported problems
- Returns a short explanation plus the complete code

### ✅ Reviewer Agent

- Checks correctness, syntax, logic, missing issues and possible improvements
- Returns strict JSON: `{"status": "approved" | "needs_revision", "feedback": "..."}`

### 🔁 Revision Loop

- `needs_revision` sends the feedback back to the coding agent, then the code is reviewed again
- A `MAX_REVISIONS` safety limit prevents endless loops

### 🛡 Validation

- `validate_task` rejects empty tasks and tasks longer than 5000 characters
- Whitespace is trimmed before the task enters the workflow
- `main.py` catches the `ValueError` and prints a `Validation error` message

### 🔐 Permissions

- `permissions.py` holds a `TOOL_PERMISSIONS` map of which agent may use which tool (`research`, `coding`, `review`, `manager`)
- `is_tool_allowed(agent_name, tool_name)` returns whether a call is allowed; unknown agents get no tools (deny by default)
- `demonstrate_permissions()` prints an ALLOWED / DENIED table as a demo

### 📋 Logging

- `logger.py` configures one shared `agent` logger with timestamp, level and message
- Logs the manager's start, each worker choice, warnings when the revision limit is hit, and every LLM attempt, success and failure

### 🔌 Shared LLM Client

- `llm.py` exposes `call_llm(messages)`, used by every agent
- Applies a request timeout and retries failed calls up to `MAX_RETRIES` times with a growing wait (2s, 4s, ...)
- Raises `RuntimeError` after the final failed attempt

### ⚙ Central Configuration

- `config.py` loads settings from `.env` with sensible defaults (a local Ollama endpoint)

| Variable        | Default                     | Purpose                          |
| --------------- | --------------------------- | -------------------------------- |
| `MODEL`         | `qwen3:1.7b`                | Chat model name                  |
| `BASE_URL`      | `http://localhost:11434/v1` | OpenAI-compatible API base URL   |
| `API_KEY`       | `ollama`                    | API key                          |
| `MAX_REVISIONS` | `8`                         | Max coding revisions             |
| `MAX_RETRIES`   | `3`                         | LLM call attempts before failing |
| `TIMEOUT`       | `60`                        | LLM request timeout in seconds   |

---

## 🛠 Tech Stack

### Core

- Python 3

### Libraries

- OpenAI Python SDK (any OpenAI-compatible endpoint, including local Ollama)
- python-dotenv
- `logging` (standard library)

---

## 📂 Project Structure

```
ai-multiple-agent/
├─ agent
│  ├─ manager.py          # Manager agent: chooses the next worker and runs the loop
│  └─ state.py            # Creates the shared state
├─ workers
│  ├─ coding_agent.py     # Writes / revises Python code using research and reviewer feedback
│  ├─ research_agent.py   # Researches the task
│  └─ reviewer_agent.py   # Reviews the code and returns JSON status + feedback
├─ config.py              # Environment-based settings and defaults
├─ llm.py                 # Shared LLM client with timeout and retries
├─ logger.py              # Shared logger
├─ main.py                # Entry point (interactive)
├─ permissions.py         # Per-agent tool permissions
├─ validation.py          # Task input validation
└─ .env                   # API configuration (not committed)
```

---

## ⚙ Installation & Setup

### 1⃣ Clone the repository

```
git clone https://github.com/mishraabhishek11/ai-multiple-agent.git
cd ai-multiple-agent
```

### 2⃣ Create and activate a virtual environment

```
python -m venv .venv
.venv\Scripts\activate
```

### 3⃣ Install dependencies

```
pip install openai python-dotenv
```

### 4⃣ Configure environment variables

Create a `.env` file in the project root. All values are optional; the defaults target a local Ollama server:

```
BASE_URL=<OpenAI-compatible API base URL>
API_KEY=<your API key>
MODEL=<chat model name>
MAX_REVISIONS=3
MAX_RETRIES=3
TIMEOUT=60
```

### 5⃣ Run the system

```
python main.py
```

---

## 🧑‍💻 Usage

```
==================================================
 INTELLIGENT MULTI-AGENT SYSTEM
==================================================

Enter your task: Write a function that checks if a number is prime

2026-11-05 10:00:00 | INFO | Starting manager for task: ...
Manager selected: research
Manager selected: coding
Manager selected: review
Manager selected: finish
```

1. Run `python main.py`
2. Type a task at the `Enter your task:` prompt
3. Watch each `Manager selected:` step and the log lines
4. Read the final **RESEARCH**, **CODE** and **REVIEW** sections

---

## 🔁 How It Works

1. `main.py` takes the task and calls `run_manager` in `agent/manager.py`
2. `validation.py` checks and trims the task
3. `agent/state.py` creates the shared state: `task`, `research`, `code`, `review`, `history`, `revision_count`
4. The manager asks the LLM (through `llm.py`) which worker should act next, based on the state
5. The selected worker runs and updates the state:
   - `research` → `workers/research_agent.py` fills `research`
   - `coding` → `workers/coding_agent.py` fills `code` (using reviewer feedback if present) and increments `revision_count`
   - `review` → `workers/reviewer_agent.py` fills `review` with `status` and `feedback`
6. Every step is logged through `logger.py`
7. The loop repeats until the manager returns `finish`

```
research → coding → review ──approved──▶ finish
                      │
                needs_revision (up to MAX_REVISIONS)
                      ▼
                    coding
```

---

## ➕ Adding Your Own Agent

1. Create a new module in `workers/` with a function that calls `call_llm` (see `workers/research_agent.py`)
2. Add a field for its output in `agent/state.py`
3. Add the agent and its allowed tools to `TOOL_PERMISSIONS` in `permissions.py`
4. Add the worker name and decision rules to the prompt in `choose_worker`, and a matching branch in `run_manager`

---

## 🩺 Troubleshooting

| Error                                     | Cause and fix                                                                                                                              |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `Validation error: Task cannot be empty.` | The task was blank. Enter a task                                                                                                           |
| `Validation error: Task is too long.`     | The task is over 5000 characters. Shorten it                                                                                               |
| `Unknown worker: ...`                     | The manager model returned more than one word. Try a stronger model                                                                        |
| `json.JSONDecodeError` in the reviewer    | The model did not return pure JSON (for example it wrapped it in a code fence). Try a stronger model                                       |
| `LLM request failed after N attempts.`    | The endpoint is unreachable or timed out. Check `BASE_URL`, `API_KEY`, `MODEL` and that the server is running (for example `ollama serve`) |

---

## 🎯 Learning Objectives

- Multi-agent orchestration with a manager agent
- Specialised worker agents with focused prompts
- Shared state passed between agents
- Review-and-revise loops with a revision limit
- Input validation, retries, timeouts and logging around LLM calls
- Permission-based access control for agent tools

---

## 🔮 Future Enhancements

- A `requirements.txt` to pin dependencies
- Enforce `is_tool_allowed` when agents call tools (currently a standalone check and demo)
- Retry and validation when the reviewer returns invalid JSON
- Validate the manager's choice before dispatching
- Write logs to a file
- Execute the generated code and feed errors back to the coding agent
- Tests for validation, permissions and the manager loop
- Web or chat interface

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch  
   git checkout -b feature/your-feature

3. Commit changes  
   git commit -m "feat(scope): your message"

4. Push changes  
   git push origin feature/your-feature

5. Open Pull Request

---

## 👨‍💻 Author

Abhishek Mishra  
GitHub: https://github.com/mishraabhishek11

---

## ⭐ Support

Give a ⭐ if you like this project!
