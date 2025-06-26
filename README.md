# AI Agents Practice Repository

A collection of practical, hands-on AI agent implementations designed for learning, practice, and experimentation.

This repository serves as a living library of AI agents. Each agent is presented as a step-by-step tutorial, including the core LLM prompts used to build it, offering a transparent look into the development process.

---

## Guiding Principles

-   **Learn by Doing:** Gain hands-on experience by running, modifying, and extending functional AI agents.
-   **Prompt-Driven Development:** Each agent includes the key LLM prompts used in its creation.
-   **Practical Use Cases:** Explore agents that solve real-world problems, from querying databases with natural language to automating research tasks.

---

## Available Agents

Each agent is located in the `agents/` directory. For detailed setup, usage instructions, and the LLM prompts used to build the agent, consult its specific README file.

| Agent | Description | Status |
| :--- | :--- | :--- |
| **AI SQL Agent** | Upload a CSV and ask questions in natural language. The agent generates and runs SQL queries to provide answers and visualizations. | ✅ Available |
| **Web Research Agent** | An agent that can browse the web to research a topic and generate a summary report. | ⏳ Planned |
| **Code Generation Agent**| An agent that assists in writing, debugging, and explaining code snippets in various languages. | ⏳ Planned |
| **[Your Next Agent Here]**| Have an idea for a new agent? Contributions are welcome. | ➕ Contribute |

---

## Getting Started

Follow these steps to set up the repository on your local machine.

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Python](https://www.python.org/downloads/) 3.9+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/<your-github-username>/S-Agents-Practice.git
    cd S-Agents-Practice
    ```

2.  **Navigate to an Agent's Directory:**
    Each agent has its own environment and dependencies. Choose an agent and navigate to its folder. For example:
    ```bash
    cd agents/sql_agent
    ```

3.  **Follow the Agent-Specific Instructions:**
    Inside each agent's directory, you will find a `README.md` file with detailed instructions for installing dependencies, running the agent, and the LLM prompts used in its development.

---

## Project Structure

To maintain organization, all agents should adhere to the following structure:

```
S-Agents-Practice/
├── agents/
│   ├── sql_agent/
│   │   ├── src/
│   │   ├── requirements.txt
│   │   └── README.md <-- Detailed README with build prompts for the SQL agent
│   └── (your_new_agent)/
│       ├── ...
│       ├── requirements.txt
│       └── README.md
├── .gitignore
└── README.md <-- This is the main project README
```

---

## Contributing

If you have an idea for a new agent or an improvement, please follow these steps:

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/NewAgent`)
3.  Commit your Changes (`git commit -m 'Add: NewAgent for X'`)
4.  Push to the Branch (`git push origin feature/NewAgent`)
5.  Open a Pull Request

When adding a new agent, please ensure it is in its own directory under `agents/` and includes a `requirements.txt` and a detailed `README.md` with its core LLM prompts.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

🌟 If you find this repository useful, please give it a star! 🌟 