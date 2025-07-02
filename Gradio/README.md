
# Gradio Day! – LLM UI Playground with OpenAI, Claude, and Gemini

Welcome to **Gradio Day**, a fun and practical notebook to help you build user interfaces using the **Gradio** framework and experiment with top LLMs like **OpenAI (GPT-4o-mini)**, **Claude 3 (Haiku)**, and optionally **Google Gemini**.

---

## 🎯 Purpose

This notebook demonstrates how to:
- Build quick, interactive UIs with **Gradio**
- Integrate with multiple LLM providers (OpenAI, Anthropic, Google)
- Compare responses from different models on the same prompt
- Generate content like company brochures from live web pages
- Stream model outputs for smoother UX

---

## ⚙️ What’s Happening

### ✅ Setup & API Configuration
- Loads API keys from `.env` file.
- Initializes OpenAI, Claude (Anthropic), and Google Gemini (optional).

### 💬 LLM Interaction Functions
- `message_gpt(prompt)`: Calls GPT-4o-mini via OpenAI
- `stream_gpt(prompt)`: Streams GPT responses
- `stream_claude(prompt)`: Streams Claude responses
- `stream_model(prompt, model)`: Unified function to stream from selected model

### 🖥️ Gradio Interfaces
- Basic UI to **shout text** (uppercase conversion)
- Chat interface for GPT and Claude using:
  - Textbox + Markdown output
  - Model dropdown selection
  - Streaming responses in real time
- Dark mode override option for accessibility testing

### 🌐 Bonus: Company Brochure Generator
- Scrapes a given company website
- Feeds the content into selected LLM (Claude or GPT)
- Generates a **markdown-formatted brochure** via streaming

---
## 📸 Some Screenshots from Testing

Here are a few snapshots from the Gradio interfaces in action:

### 🧪 Gemini Model UI for general queries
![image](https://github.com/user-attachments/assets/189e144b-20ac-43d6-9a39-09950e9f4eeb)

### 🤖 GPT Model UI for Brichure Generation
![image](https://github.com/user-attachments/assets/60d64e78-6ad4-4c8f-a655-52cdc5e7df20)






---

## 🙋‍♀  Final Note

I'm creating this repo primarily for my **personal learning and reference**, so I can revisit these concepts whenever needed.  
If it helps someone else along the way — that would genuinely make me happy! 😊  
Feel free to explore, modify, and build upon it. 


