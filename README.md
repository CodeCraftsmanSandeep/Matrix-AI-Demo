# Matrix-AI-Demo

**Matrix-AI-Demo** is a prototype system designed to demonstrate multi-document, multi-query analysis using LLMs. It aims to build a structured **Matrix** where each cell represents an answer from a Large Language Model (LLM) to a combination of a sub-query and an input document.

### 🔍 Key Features

* ✅ **Query Decomposition**
  Automatically breaks down the main query into multiple relevant sub-queries.

* 📂 **Multi-Document Support**
  Accepts up to 5 text files as input (support for other file types is planned).

* 🧠 **Matrix Generation**
  For each document and sub-query pair, a corresponding cell is generated containing the LLM’s response.

* 📌 **RAG-Style Citations**
  Incorporates a Retrieval-Augmented Generation (RAG)-like framework to cite source documents in the output.

---

### 🚀 Demo Usage

* Upload up to **5 `.txt` files**.
* Enter your **main query**.
* The system uses the **Groq free LLM API** to generate the response matrix.
* ⚠️ *Note:* Groq’s free API has rate limits — expect limitations on frequent or large-scale usage.
