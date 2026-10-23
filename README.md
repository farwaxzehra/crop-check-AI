# 🌱 CropCheck AI

**AI-assisted crop symptom analysis for smarter inspection**

> Helping farmers explore possible causes of crop symptoms and decide what to inspect next, without pretending that one photo can guarantee a diagnosis.

## 👥 Team

- **Team name:** TechX
- **Member 1 — Backend and AI:** Rao Alishan
- **Member 2 — Frontend:** Rimsha
- **Member 3 — Shipping Lead and Deployment:** Syeda Farwa Zehra

## 📌 Overview & Summary

CropCheck AI is an AI-powered web application designed to help farmers investigate unusual crop symptoms. Users upload a crop photo and describe the symptoms they have observed.

The application analyses the available information and presents possible explanations, reasons those explanations may fit, and a practical checklist for further inspection.

Its main feature is presenting multiple plausible explanations rather than confidently claiming a single diagnosis. The goal is to help users decide what to inspect next and when to seek local agricultural expertise.

## 🎯 Problem Statement

Farmers may have difficulty distinguishing pest damage from disease symptoms, making it harder to decide what to inspect next. Our application uses AI to analyse a crop photo and reported symptoms, suggest possible causes, and recommend safe next steps for verification.

**How AI is used:** Image recognition or text classification, depending on the implemented model.

**Unique touch:** Multiple possible explanations and verification steps instead of one overconfident diagnosis.

## 🛠️ Tools & Technology Stack

| Technology | Purpose |
|---|---|
| React | Building the user interface |
| TypeScript | Type-safe frontend development |
| Vite | Frontend development and build tool |
| Tailwind CSS | Styling the interface |
| Python | Backend programming |
| FastAPI | Building the analysis API |
| Pydantic | Validating structured data |
| [Actual AI model/API] | Analysing the crop photo and symptom description |
| Git and GitHub | Version control and collaboration |
| Vercel | Frontend hosting |
| Render | Backend hosting |

**Architecture:** React frontend → FastAPI backend → AI model/API → structured result displayed to the user.

The AI API key is stored in the backend environment variables and is never exposed in frontend code.

## 🖥️ Output / Results Dashboard

The application guides users through a simple workflow:

1. **Upload a photo:** Select a clear image of the affected crop.
2. **Describe symptoms:** Enter observations such as spots, holes, discoloration, or other visible changes.
3. **Analyse:** Submit the information for AI-assisted analysis.
4. **Review possible causes:** See plausible explanations and why each may fit the reported evidence.
5. **Follow the inspection checklist:** Review observations that may help distinguish the possible causes.
6. **Choose safe next steps:** Get cautious guidance and an expert-review recommendation when needed.

### Expected results displayed

- Possible causes and their explanations
- Observations to check for each possibility
- An inspection checklist
- Safe next steps
- An indication when more information or expert review is needed

**Important:** Results are preliminary suggestions, not a confirmed crop diagnosis. The application should communicate uncertainty and should not invent confidence scores or guarantee that a particular cause is correct.

**Live application:** [Add deployed URL when verified]

**Screenshot:** [Add a screenshot of the actual working application here]

## 🚀 How to Run This Project Locally

### Prerequisites

Install the following before running the application:

- Git
- Python 3.11 or a version supported by the backend dependencies
- Node.js and npm
- A valid AI API key if required by the implemented model

### Step 1 — Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/farwaxzehra/crop-check-AI
cd CropCheck-AI
```



### Step 2 — Start the backend

Open a terminal in the repository root:

```bash
cd backend
python -m venv .venv
```

On Windows Command Prompt:

```bat
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file using the backend's `.env.example` as a guide. Add your own valid AI API key and any other required variables. Never commit this file.

Start FastAPI using the actual entry point in your backend. For example, if the application is in `app/main.py` and exposes `app = FastAPI()`:

```bash
uvicorn app.main:app --reload
```

Open the API documentation at:

`http://127.0.0.1:8000/docs`

### Step 3 — Start the frontend

Open a **second terminal** in the repository root:

```bash
cd frontend
npm install
```

Create the local frontend environment file using `frontend/.env.example`. Set the backend URL using the environment variable name expected by the actual frontend code. For example, a Vite app may use:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Only use this variable name if the frontend is configured to read it.

Start the frontend:

```bash
npm run dev
```

Open the local URL printed by Vite in your terminal, commonly:

`http://localhost:5173`

### Step 4 — Test the application

1. Open the frontend.
2. Upload a valid crop photo.
3. Enter a symptom description.
4. Submit the form.
5. Check that the result includes possible explanations and inspection steps.
6. Test invalid input and an AI service failure.

If your actual file structure or commands differ, follow the instructions in the corresponding `package.json`, `requirements.txt`, and backend entry point.

## 🌐 Deployment

- **Frontend:** [Add verified Vercel URL]
- **Backend:** [Add verified Render URL]
- **GitHub repository:** [Add repository URL]
- **Demo video:** [Add Google Drive video link]

The deployed frontend must connect to the deployed backend, and the application must work without requiring judges to log in.

## 📚 Credits & Resources

- **AI model/API:** [Add the actual model and provider used]
- **Datasets:** [List datasets and their sources, or state “No external dataset used” if accurate]
- **Libraries and other resources:** [List relevant libraries, models, documentation, and other resources]
- **Acknowledgements:** [Add relevant acknowledgements]

## 🔮 Future Improvements

- Support more crops and regional languages.
- Improve evaluation using verified agricultural examples.
- Add trusted, locally relevant agricultural resources.
- Improve guidance for unclear photos and insufficient information.
- Explore feedback from agricultural experts.

## ✅ Conclusion

CropCheck AI aims to make early crop-symptom investigation more accessible by combining image and symptom analysis with multiple possible explanations and a practical inspection checklist.

Rather than replacing agricultural experts, it helps farmers identify useful observations, consider alternative explanations, and decide on sensible next steps.

**Our goal is not to promise a perfect diagnosis. It is to help farmers ask better questions and inspect their crops more effectively.**
