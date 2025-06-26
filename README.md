# The AI Agents Cookbook: Recipes & Prompts for Practice

A collection of practical, hands-on AI agent implementations designed for learning, practice, and experimentation.

This repository serves as a living library of AI agents. A core feature is that each agent is presented as a step-by-step tutorial, complete with the **full LLM prompt** used to build it. This offers a transparent and educational look into the development process.

---

## How to Use This Repository: Building the Agents

Each agent in this repository was developed using a single, targeted LLM prompt that instructs the model on the agent's role, its required capabilities, and the exact output format for the code files.

This unique approach gives you two primary ways to engage with the material:

1.  **Run Pre-built Agents Locally:** Follow the `Getting Started` guide to clone the repository and run the functional agents directly on your machine. This is ideal for quickly testing their capabilities.

2.  **Generate Agents from Scratch:** Navigate to any agent's directory, copy the full prompt (the "recipe") from its `PROMPT.md` file, and paste it into your preferred LLM (e.g., Gemini, ChatGPT, Claude). This allows you to generate the code yourself and see the prompt engineering in action.

Regardless of the method you choose, the repository is built on these core principles:

-   **Learn by Doing:** Gain hands-on experience by running, modifying, and extending the functional AI agents.
-   **Prompt-Driven Development:** Each agent includes the **key LLM prompt** used in its creation, allowing you to see exactly how they were engineered.
-   **Explore Practical Use Cases:** The agents are designed to solve real-world problems, from querying databases with natural language to automating research tasks.

---

## Available Agents

Each agent is located in the `agents/` directory. For detailed setup, usage instructions, and to view the **LLM creation prompt**, consult its specific README file.

| Agent | Description | Status |
| :--- | :--- | :--- |
| **AI SQL Agent** | Upload a CSV and ask questions in natural language. The agent generates and runs SQL queries to provide answers and visualizations. | ✅ Available |
| **Web Research Agent** | An agent that can browse the web to research a topic and generate a summary report. | ⏳ Planned |
| **Code Generation Agent**| An agent that assists in writing, debugging, and explaining code snippets in various languages. | ⏳ Planned |
| **[Your Next Agent Here]**| Have an idea for a new agent? Contributions are welcome. | ➕ Contribute |

---

## Getting Started (To Run Locally)

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
    Inside each agent's directory, you will find a `README.md` file with detailed instructions for installing dependencies and running the agent.

---

## Project Structure

To maintain organization, all agents should adhere to the following structure:

```
S-Agents-Practice/
├── agents/
│   ├── sql_agent/
│   │   ├── src/
│   │   ├── PROMPT.md <-- The full prompt (recipe) to build this agent
│   │   ├── requirements.txt
│   │   └── README.md <-- Agent-specific setup and usage
│   └── (your_new_agent)/
│       ├── src/
│       ├── PROMPT.md
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

When adding a new agent, please ensure it is in its own directory under `agents/` and includes its core `PROMPT.md` file and a detailed `README.md`.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

🌟 If you find this repository useful, please consider giving it a star! 🌟 