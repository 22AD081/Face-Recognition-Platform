# Face-Recognition-Platform

This is a browser-based Face Recognition Platform with Real-Time AI Q&A using RAG (Retrieval-Augmented Generation). The project is organized into three main components:

---

## 🔧 Project Structure

face-rag-platform/
│
├── face_backend/ # Handles face registration and recognition
│
├── face-rag-client/ # Frontend React application for user interface
│
├── rag_engine/ # Retrieval-Augmented Generation system using LangChain, FAISS, and OpenAI
│
└── .gitignore # Specifies untracked files to ignore

---

##  Components

### 1. `face_backend/`
- Built using Flask.
- Responsible for face registration and recognition.
- Uses the `face_recognition` library to match user faces in real-time.

### 2. `face-rag-client/`
- React-based frontend interface.
- Enables user interaction with both face recognition and Q&A components.

### 3. `rag_engine/`
- Implements a RAG (Retrieval-Augmented Generation) system.
- Uses:
  - **LangChain** for pipeline construction.
  - **FAISS** for vector search.
  - **OpenAI GPT** for answering user questions based on retrieved context.

---

##  Current Status
-  Project structure set up
-  Backend, frontend, and RAG components initialized
-  Connected to GitHub

This project is a part of a hackathon run by https://katomaran.com 
