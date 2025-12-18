# MediQ - AI Healthcare Assistant

This project is an AI-powered healthcare assistant developed based on the MIMIC & MedQuAD clinical dataset, which contains thousands of real, de-identified ICU records. By learning from this rich medical source, the model gains a more grounded understanding of symptoms, diagnoses, and treatment patterns, allowing it to provide clearer explanations, symptom checking, and general medical support.

<p align="center">
  <img src="https://github.com/user-attachments/assets/0ec198fb-5301-4ad7-8ac2-4fcb1cf20a38"
       alt="Login"
       width="590"/>
</p>
<p align="center"><em>Figure 1. Login Screen</em></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/cded8793-c895-4c9b-a16d-7a4eb28403a6"
       alt="UI"
       width="590"/>
</p>
<p align="center"><em>Figure 2. Main Chat UI</em></p>

## Overall Architecture
<p align="center">
  <img src="https://github.com/user-attachments/assets/d0de20bc-41cd-41f9-9819-3ae61c2011a2"
       alt="architecture"
       width="590"/>
</p>
<p align="center"><em>Figure 3. System Architecture</em></p>

# MediQ - Healthcare Assistant
Health assistant that tracks symptoms, schedules medication, and provides concise wellness suggestions using a fine-tuned LLaMA 2 model plus a .NET front-end.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup: Python API](#setup-python-api)
  - [Configure Environment](#configure-environment)
  - [Configure Model & Data](#configure-model--data)
  - [Configure Database](#configure-database)
  - [Configure Translation (optional)](#configure-translation-optional)
  - [Run the API](#run-the-api)
  - [API Usage](#api-usage)
- [Setup: .NET Web App](#setup-net-web-app)
  - [Restore & Build](#restore--build)
  - [Configure API Endpoint](#configure-api-endpoint)
  - [Run the Web App](#run-the-web-app)
- [Data Notes](#data-notes)
- [Troubleshooting](#troubleshooting)


# Project Structure
- `app.py`: FastAPI entry point for text generation.
- `data/`: MedQuAD XML QA datasets (multiple sub-sources).
  - `Dataset-MedQuAD/*`: XML QA per source (CancerGov, GARD, MPlus, etc.).
  - `readme.txt`: Dataset notes.
- `database/`: SQL scripts for schema and demo data.
- `model/`: Fine-tuning notebook and documentation for LLaMA 2 7B.
- `utils/`: Helpers for DB access, input filtering, translation.
- `Web Application/`: ASP.NET Core solution (front-end and shared business objects).
  - `WebApplication1/`: Main web project (controllers, views, static assets).
  - `BusinessObjects/`: Shared models and build outputs.
- `LICENSE`: Project license.

## Prerequisites
- Python 3.10+ and `pip`
- .NET SDK 8.0+ (for `Web Application/WebApplication1`)
- SQL Server or Azure SQL (update the connection string in `utils/db.py`)
- Local LLaMA 2 7B chat model in Hugging Face format
- Git LFS if pulling large model artifacts via Git

## Setup: Python API
FastAPI service in `app.py` runs the LLaMA model and logs chat history to SQL Server.

### Configure Environment
Create a virtual environment and install dependencies:
```
python -m venv .venv
.venv\Scripts\activate          # PowerShell on Windows
pip install --upgrade pip
pip install fastapi "uvicorn[standard]" transformers torch langdetect sqlalchemy pyodbc google-generativeai
```

### Configure Model & Data
- Set `model_path` in `app.py` to the folder containing your merged LLaMA 2 7B model (Hugging Face format). The default path is Linux-style; change it for Windows.
- The `data/` folder already contains MedQuAD XML samples; no action needed to run the API, but you can replace or extend the dataset as needed.

### Configure Database
- Update `DB_CONNECTION` in `utils/db.py` to point to your SQL Server/Azure SQL instance.
- If the schema is missing, run `database/HeathCareDatabase.sql` to create tables, then optionally seed with `database/demo_data.sql`.

### Configure Translation (optional)
Set your Google Generative AI key (used in `utils/translate.py`):
```
$env:GEMINI_API_KEY = "<your_google_generative_ai_key>"
```
You can also hardcode the key in `utils/translate.py` (not recommended for production).

### Run the API
From the repo root:
```
.venv\Scripts\activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
The service enables CORS for common localhost ports (see `origins` in `app.py`).

### API Usage
- Endpoint: `POST /generate`
- Request body:
```
{ "text": "Your question here" }
```
- Flow: input is validated (`utils/filter.py`), language is detected, text is translated to English if needed, chat history is pulled from SQL, the model generates a reply, and the response is translated back to Vietnamese if the original input was Vietnamese. Returns `response`, `lang`, `session_id`.

## Setup: .NET Web App
ASP.NET Core app in `Web Application/WebApplication1` serves as the front-end.

### Restore & Build
```
cd "Web Application/WebApplication1"
dotnet restore
dotnet build
```

### Configure API Endpoint
Point the web app to the FastAPI service (default `http://localhost:8000`). Update the base URL in `appsettings*.json` or controller code as applicable.

### Run the Web App
```
dotnet run
```
Then open the shown URL (typically `https://localhost:7063` or `http://localhost:5000`).

## Data Notes
- `data/Dataset-MedQuAD` is large and already included here. If you clone without LFS and miss files, fetch them separately or sync from the original MedQuAD source.
- The Python API does not require you to load all XMLs at startup; they are supporting assets for fine-tuning or extensions.

## Troubleshooting
- Model path errors: ensure `model_path` points to a valid Hugging Face-formatted directory and that `torch` can load it (GPU recommended).
- SQL connectivity: verify `DB_CONNECTION`, firewall rules, and that the `ChatMessages` table exists (created by `HeathCareDatabase.sql`).
- Translation failures: set `GEMINI_API_KEY` or disable translation logic for testing.
- Port conflicts: change `--port` for FastAPI or the Kestrel port in the .NET app settings.
  
