# 🦇 BATPAN VibeCoder (ver2.2.05)

[![Version](https://img.shields.io/badge/version-ver2.2.05-facc15?style=flat-square&labelColor=292524)](https://github.com/BATPANn/BP_VibeCoder)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![UI](https://img.shields.io/badge/UI-PyQt6-4ade80?style=flat-square)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/license-MIT-38bdf8?style=flat-square)](LICENSE)

**BATPAN VibeCoder** is a standalone desktop developer utility built with PyQt6 designed to package, filter, and format full source repositories, nested folders, and copied code snippets into clean, AI-ready Markdown or text representations.

Inspired by developer workflow tools like [FileCombiner](https://github.com/mehrhossin/FileCombiner), VibeCoder bundles fragmented codebases into clean context files for Large Language Models (ChatGPT, Claude, Gemini, DeepSeek, and local LLMs).

---

## 🚀 Why Use BATPAN VibeCoder?

* **Bypass Multi-File Upload Constraints:** Consolidate sprawling codebases into a single organized Markdown file equipped with syntax-highlighted code fences and an ASCII directory map.
* **Respect LLM Context Windows:** Automatically shard large repositories across 1 to 10 split parts to feed Large Language Models in sequential batches without truncation.
* **Instant Snippet Tagging:** Copy functions directly from your IDE and press `Ctrl + V` inside the application. VibeCoder parses the snippet, extracts the function or class signature, and labels it with an interactive tag chip.
* **Recursive Folder Drop:** Drop whole project directories into the drop zone; the scanner navigates subdirectories and isolates only files matching active extension rules.
* **Direct Clipboard Attachment:** Leverages Windows native file clipboard integration (`CF_HDROP`). Once bundled, press `Ctrl + V` directly inside AI web interfaces to attach the generated file.

---

## ✨ Core Features

* **Three Input Modalities:**
  * **Folder Path:** Traversal of local directories with optional subfolder scanning.
  * **Dropped Files & Folders:** Drag-and-drop workspace supporting bulk files and full folders.
  * **Pasted Snippets (`Ctrl + V`):** App-wide capture hotkey converting clipboard text into tagged virtual files.
* **YouTube-Style Tag Management:**
  * Interactive tags for managing active file extension filters.
  * Includes a single-click **"➕ All Common"** preset covering primary languages.
* **Intelligent Auto-Naming:**
  * Identifies `void`, `def`, `func`, `fn`, `class`, or arrow function signatures to automatically suggest relevant filenames.
* **Bilingual Interface:**
  * Full localization for **English** and **Persian (فارسی)** with dynamic LTR/RTL layout alignment.
* **Theme System:**
  * Single-click toggle between **Dark 🌙**, **Light ☀️**, and **System 💻** display modes.
* **Session Persistence:**
  * Automatically stores configurations, paths, active extensions, and custom tags in `settings.json`.

---

## 🛠️ Supported Language Fences

| Category | File Extensions |
| :--- | :--- |
| **Backend & Systems** | `.cs` (C#), `.cpp` / `.c` / `.h`, `.py` (Python), `.go` (Go), `.rs` (Rust), `.java`, `.php`, `.rb` (Ruby), `.swift`, `.kt` (Kotlin) |
| **Web & Frontend** | `.js` (JavaScript), `.ts` (TypeScript), `.html`, `.css` |
| **Data & Config** | `.json`, `.yaml` / `.yml`, `.xml`, `.sql` |
| **Scripts & Docs** | `.sh` (Bash), `.bat` (Batch), `.ps1` (PowerShell), `.md` (Markdown), `.txt` |

---

## 📥 Installation & Setup

### Prerequisites
* Python 3.10 or newer installed.

### Setup Steps
1. Clone the repository:
   ```bash
   git clone [https://github.com/BATPANn/BP_VibeCoder.git](https://github.com/BATPANn/BP_VibeCoder.git)
   cd BP_VibeCoder
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python BP_VibeCoder_v2.2.05.pyw
   ```
   *(Using the `.pyw` extension launches the GUI without an underlying terminal window.)*

---

## 📖 Quick Tutorial

```text
 ┌─────────────────┐       ┌────────────────────┐       ┌──────────────────┐
 │ 1. Choose Input │ ────> │ 2. Set Extensions  │ ────> │ 3. Combine Files │
 │ Folder/Drop/Tags│       │ Chips / Common All │       │ Filter Selection │
 └─────────────────┘       └────────────────────┘       └──────────────────┘
                                                                  │
                                                                  ▼
                                                        ┌──────────────────┐
                                                        │ 4. Ctrl+V in AI  │
                                                        │ Upload or Paste  │
                                                        └──────────────────┘
```

1. **Select an Input Mode:** Choose between **Folder Path**, **Dropped Files**, or **Pasted Snippets**.
2. **Configure Extension Filters:** Enter desired extensions and press `Enter`, or click **"➕ All Common"**.
3. **Configure Output:** Select `.md` or `.txt`, specify the target part count (1–10), and set clipboard routing (**Copy Content** or **Copy File**).
4. **Combine:** Click **⚡ Combine Files** to review the item checklist and finalize the output.
5. **Paste to AI:** Navigate to your AI chat interface and press `Ctrl + V` to attach the file or insert the combined output.

---

## ☕ Support & Donations

If BATPAN VibeCoder accelerates your development workflow, you can support continued updates via cryptocurrency:

* **USDT (TRC-20):** `YOUR_TRC20_WALLET_ADDRESS`
* **USDT (BEP-20 / ERC-20):** `YOUR_BEP20_WALLET_ADDRESS`

*(Please verify the chosen network matches before executing transactions.)*

---

## 📄 License

This project is distributed under the [MIT License](LICENSE).
