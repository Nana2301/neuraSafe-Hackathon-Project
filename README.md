# hackathon

AI Scam Checker mobile app

## Overview

NeuraSafe is an AI-powered scam detection system that allows users to analyze messages (e.g., from WhatsApp) and determine whether they are safe or potentially harmful. The system combines a Python-based AI backend with a Flutter mobile frontend to deliver real-time analysis and clear explanations.


## System Architecture

NeuraSafe is built with two main components:

1. AI Backend (Python)

Handles message analysis and prediction
Processes user input in real time
Returns classification results (safe or suspicious)
Provides reasoning behind each decision

2. Mobile Frontend (Flutter)

User interface for interacting with the system
Allows users to input and analyze messages
Displays results and AI-generated explanations
Runs on mobile devices or emulators

## Getting Started

Step 1: Set Up AI Backend

Activate the virtual environment
Navigate to the project directory
Run the Python application

Once started:

The backend server begins running
It listens for incoming message analysis requests
AI predictions are processed instantly

Step 2: Run the Flutter Frontend

Open the Flutter project
Select a target device (e.g., emulator)
Launch the emulator
Run the application

Once launched:

The app loads successfully
The NeuraSafe intro screen is displayed

## Application Flow

🔹 Intro Screen

Displays the NeuraSafe introduction
Explains the purpose of the app:
    Helping users check suspicious messages quickly and safely
User taps “Start Checking” to proceed

🔹 Main Screen

Users can:

Paste any message (e.g., WhatsApp text) into the input field
Click “Analyze Message”

Example Usage

Case 1: Normal Message

Input:
A regular, everyday message

Result:

Classified as Safe
AI explanation:
Follows normal communication patterns
No suspicious intent detected

Case 2: Suspicious Message

Input:
A message asking to borrow money

Result:

Classified as Suspicious
AI explanation:
Contains financial/loan-related bait
Common tactic used in scams to manipulate victims

## AI Decision Explanation

One key feature of NeuraSafe is transparency.
For every analysis, the system provides:

Clear classification (Safe / Suspicious)
A simple explanation of why the decision was made


🔄 Flexible testing (users can try multiple messages)

