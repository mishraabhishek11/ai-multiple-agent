# 🤖 AI Multiple Agent

A **Python multi-agent system** where a **Manager agent** coordinates three specialised worker agents — **Research**, **Coding** and **Reviewer**. The manager (an LLM) decides which worker should act next, and the loop continues until the reviewer approves the code or the revision limit is reached.

This project demonstrates a multi-agent workflow built from small, separate parts: shared state, a manager/orchestrator, worker agents and a review-and-revise loop.

---

## 🚀 Features

### 🧭 Manager Agent

- Reads the shared state (task, research, code, review, history, revision count)
- Decides **only the next worker** and returns a single word: `research`, `coding`, `review` or `finish`
- Stops when the review is `approved` or when `MAX_REVISIONS` (default 3) is reached
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

---

## 🛠 Tech Stack

### Core

- Python 3

### Libraries

- OpenAI Python SDK (any OpenAI-compatible endpoint)
- python-dotenv

---

## 📂 Project Structure

```
ai-multiple-agent/
├─ coding_agent.py     # Writes / revises Python code using research and reviewer feedback
├─ main.py             # Entry point (interactive)
├─ manager.py          # Manager agent: chooses the next worker and runs the loop
├─ research_agent.py   # Researches the task
├─ reviewer_agent.py   # Reviews the code and returns JSON status + feedback
├─ state.py            # Creates the shared state
└─ .env                # API configuration (not committed)
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

Create a `.env` file in the project root:

```
BASE_URL=<OpenAI-compatible API base URL>
API_KEY=<your API key>
MODEL=<chat model name>
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

Manager selected: research
Manager selected: coding
Manager selected: review
Manager selected: finish
```

1. Run `python main.py`
2. Type a task at the `Enter your task:` prompt
3. Watch each `Manager selected:` step
4. Read the final **RESEARCH**, **CODE** and **REVIEW** sections

---

## 🔁 How It Works

1. `main.py` takes the task and calls `run_manager` in `manager.py`
2. `state.py` creates the shared state: `task`, `research`, `code`, `review`, `history`, `revision_count`
3. The manager asks the LLM which worker should act next, based on the state
4. The selected worker runs and updates the state:
   - `research` → `research_agent.py` fills `research`
   - `coding` → `coding_agent.py` fills `code` (using reviewer feedback if present) and increments `revision_count`
   - `review` → `reviewer_agent.py` fills `review` with `status` and `feedback`
5. The loop repeats until the manager returns `finish`
6. `main.py` prints the research, code and review

```
research → coding → review ──approved──▶ finish
                      │
                needs_revision (up to MAX_REVISIONS)
                      ▼
                    coding
```

---

## ➕ Adding Your Own Agent

1. Create a new module with a function that takes the task or state and returns its result (see `research_agent.py`)
2. Add a field for its output in `state.py`
3. Add the worker name and decision rules to the prompt in `choose_worker`, and a matching branch in `run_manager`

---

## 🩺 Troubleshooting

| Error                                           | Cause and fix                                                                                        |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `Unknown worker: ...`                           | The manager model returned more than one word. Try a stronger model                                  |
| `json.JSONDecodeError` in the reviewer          | The model did not return pure JSON (for example it wrapped it in a code fence). Try a stronger model |
| `openai.AuthenticationError` / connection error | Check `BASE_URL`, `API_KEY` and `MODEL` in `.env`                                                    |

---

## 🎯 Learning Objectives

- Multi-agent orchestration with a manager agent
- Specialised worker agents with focused prompts
- Shared state passed between agents
- Review-and-revise loops with a revision limit
- Structured JSON output from an LLM

---

## 🔮 Future Enhancements

- A `requirements.txt` to pin dependencies
- Retry and validation when the reviewer returns invalid JSON
- Validate the manager's choice before dispatching
- Execute the generated code and feed errors back to the coding agent
- Tests for the state and the manager loop
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
