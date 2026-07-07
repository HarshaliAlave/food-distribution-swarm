# 🌱 EcoFeast — AI Control Tower

**Autonomous Surplus Supply Chains. Zero Waste Value Chains.**

EcoFeast is an agentic multi-agent system (built with **LangGraph** + **Streamlit**, powered by **Groq**) that autonomously matches localized retail food surplus with nearby non-profits, plans courier routing, and generates ESG/compliance reports — with minimal human intervention.

> An AI dispatcher that redistributes surplus food autonomously — matched, routed, and verified in real time, with zero manual coordination.

**🔗 Live App: [ecofeast.streamlit.app](https://ecofeast.streamlit.app/)**

---

## ✨ Key Features

- **Goal-driven autonomy** — a single inventory update triggers a coordinated multi-agent response across the dispatch network.
- **Live swarm monitoring** — every agent decision and courier state change is visible on a real-time dashboard.
- **Evidence-grounded logistics** — routing driven by live coordinate mapping and cargo/storage parameters.
- **Dual-tenant views** — separate portals for commercial restaurants and receiving non-profits.
- **ESG optimization tracking** — automatic carbon-aversion (kg CO₂) and tax write-off estimates.

## 🖼️ Screenshots

Screenshots of the running app live in [`screenshots/`](./screenshots).

<!-- Example, once your files are in the folder:
![Landing page](./screenshots/landing.png)
-->

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Agent orchestration | LangGraph |
| LLM inference | Groq API |
| Language | Python |

## 📂 Project Structure

```
food-distribution-swarm/
├── app.py                  # Streamlit entry point
├── graph.py                 # LangGraph agent/state-machine definitions
├── requirements.txt
├── screenshots/              # App screenshots
├── project-docs/             # Lean Canvas, Concept Note, Pitch Deck
│   ├── EcoFeast_Lean_Canvas.pdf
│   ├── EcoFeast_Concept_Note.docx
│   └── EcoFeast.pptx
├── .env                      # Local secrets (NOT committed — see below)
├── .gitignore
├── LICENSE
└── README.md
```

## 🔑 Getting Your Groq API Key

1. Sign up / log in at [console.groq.com](https://console.groq.com).
2. Go to **API Keys** → **Create API Key**.
3. Copy the key — you'll need it below.

## 🚀 Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/food-distribution-swarm.git
cd food-distribution-swarm

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Run the app
streamlit run app.py
```

## ☁️ Deploying on Streamlit Community Cloud

1. Push this repo to GitHub (see below — **make sure `.env` is not included**).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** → select this repository, branch (`main`), and main file path (`app.py`).
4. Before deploying, open **Advanced settings → Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
5. Click **Deploy**. Streamlit Cloud will build and host the app; your key stays private in the Secrets manager and is never in the repo.

In `app.py` / `graph.py`, read the key like this so it works both locally and on Streamlit Cloud:

```python
import os
import streamlit as st

groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
```

## 📄 Project Docs

Full context on the problem, solution, and business model is in [`project-docs/`](./project-docs):
- **Lean Canvas** — [`EcoFeast_Lean_Canvas.pdf`](https://github.com/HarshaliAlave/food-distribution-swarm/blob/main/project-docs/EcoFeast_Lean_Canvas.pdf)
- **Concept Note** — [`EcoFeast_Concept_Note.docx`](https://github.com/HarshaliAlave/food-distribution-swarm/blob/main/project-docs/EcoFeast_Concept_Note.docx)
- **Pitch Deck** — [`EcoFeast.pptx`](https://github.com/HarshaliAlave/food-distribution-swarm/blob/main/project-docs/EcoFeast.pptx)

## 📜 License

Copyright © 2026 Harshali Sushant Alave

This project is licensed under the **Apache License 2.0** — see [`LICENSE`](./LICENSE) for details.

## 🔗 Links

- **Live Demo:** [ecofeast.streamlit.app](https://ecofeast.streamlit.app/)
- **GitHub Repository:** [github.com/HarshaliAlave/food-distribution-swarm](https://github.com/HarshaliAlave/food-distribution-swarm)
