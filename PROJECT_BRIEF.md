# CropCheck AI — Project Brief

## Overview
CropCheck AI helps farmers investigate possible causes of crop damage using AI.

## Problem Statement
Farmers may struggle to distinguish pest damage from plant diseases, making it difficult to decide what to inspect next.

## Solution
Users upload a crop photo and describe symptoms. AI suggests multiple possible causes and recommends safe steps to verify them.

## Main Features
- Upload a crop photo.
- Enter symptoms and optional crop name.
- Get multiple possible causes with explanations.
- View an inspection checklist and safe next steps.
- Show uncertainty instead of claiming a definite diagnosis.

## Tech Stack
- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Backend:** Python, FastAPI
- **AI:** Vision-capable AI API
- **Deployment:** Vercel and Render
- **Version Control:** Git and GitHub

## Team Responsibilities
- **Member 1:** Backend and AI integration
- **Member 2:** Frontend development
- **Member 3:** GitHub, integration, deployment, testing and submission

## API
`POST /api/analyze-crop`

Accepts a crop photo, symptoms, and an optional crop name.

## Safety
AI suggestions are not confirmed diagnoses. Users should verify symptoms and consult an agricultural expert when needed. API keys must remain secret.

## Deployment Links
- **Frontend:** To be added
- **Backend:** To be added

## Conclusion
CropCheck AI aims to help farmers make more informed decisions about crop damage through AI-assisted investigation and safe verification steps.
