# 📖 eNoval: Terminal Novel Reader

[简体中文](README.md) | [日本語](README_jp.md)

A lightweight, pure Python terminal novel reader designed for command-line enthusiasts. It supports `.txt` novel files, offering core functionalities like chapter recognition, reading progress saving, bookmarking, and chapter search, allowing you to enjoy an immersive reading experience right in your terminal!

![screenshot](assets/screenshot.png) <!-- You can add a screenshot here -->

---

## ✨ Key Features

-   **Smart Pagination**: Dynamically adjusts content display based on terminal size for optimal reading layout.
-   **Chapter Recognition**: Automatically extracts chapter titles using regular expressions (supports forms like "Chapter", "Section", "Episode", etc.).
-   **Progress Management**: Automatically saves reading progress, ensuring you can always return to where you left off.
-   **Bookmark Functionality**: Easily mark and resume specific chapters for convenient review.
-   **Quick Navigation**: Supports chapter search and jump, quickly locating desired content.
-   **Internationalization (i18n) Support**: Supports multi-language interface (Chinese, English, Japanese) for enhanced user experience.
-   **Configuration Settings**: Easily configure application settings like default language via `config.yaml`.
-   **Unified Command Style**: Adopts a `>>>` style command prompt, simple and easy to use.
-   **Offline Availability**: No internet connection required, enjoy reading anytime, anywhere.

---

## 📦 Installation & Usage

This project recommends using the [`uv`](https://github.com/astral-sh/uv) package manager, which is faster and more efficient than `pip`.

### 🛠️ Install uv

You can install `uv` using the following methods:

**Standalone Installers**:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Install via PyPI**:

```bash
# With pip
pip install uv
# Or with pipx
pipx install uv
```

If installed via the standalone installer, `uv` can update itself to the latest version:

```bash
uv self update
```

For more details and alternative installation methods, please refer to the [official uv installation documentation](https://astral.sh/uv/install).

### 🚀 Quick Start

1.  **Install Dependencies**:

    ```bash
    uv init
    uv add rich pyyaml
    ```

2.  **Prepare Novel Files**:

    Place your `.txt` novel files into the `library/` folder in the project root directory.

3.  **Launch Reader**:

    ```bash
    uv run main.py
    ```

---

## 📷 Example

```text
📘 My Novel.txt — Page 3 / 158

This is the main content...
This is the main content...
This is the main content...

>>> [n]Next Page [p]Previous Page [q]Quit [g]Go to Page [m]Table of Contents [j]Jump to Chapter [c]Clear Progress [b]Chapter Bookmark
```

---

## 📚 Command Guide

| Command        | Function Description         |
| :------------- | :--------------------------- |
| `n` or Enter   | Read next page               |
| `p`            | Return to previous page      |
| `g`            | Jump to specified page number|
| `m`            | View book's table of contents|
| `j`            | Jump to specified chapter number |
| `b`            | Mark current chapter as bookmark |
| `c`            | Clear current book's reading progress |
| `s`            | Enter settings menu (e.g., change language) |
| `q`            | Save progress and exit reader |

---

## 📂 Project Structure

```
.
├── main.py           # Main program entry point
├── config.yaml       # Configuration file for settings like default language
├── progress.yaml     # Auto-generated reading progress save file
├── library/          # Directory for .txt novel files
├── lang/             # Directory for multi-language translation files
│   ├── en.json
│   ├── jp.json
│   └── zh-cn.json
├── assets/           # Directory for screenshots and other resources (optional)
```

---

## 🛠️ Tech Stack

-   **Python 3.8+**
-   **[Rich](https://github.com/Textualize/rich)**: For beautifying terminal output, providing rich colors and styles.
-   **PyYAML**: For storing reading progress data in YAML format.
-   **Standard Libraries**: `os`, `re`, `shutil`, `textwrap`.

---

## 📜 License

This project is released under the MIT License. Please refer to the `LICENSE` file for details.

MIT License © 2025 [Rinkio-Lab](https://github.com/Rinkio-Lab/)

---

## 🤝 Contribution

Thank you for your interest in eNoval! If you have any suggestions or would like to contribute code, feel free to submit a Pull Request or open an Issue. Let's work together to push the terminal reading experience to the extreme! 💪📚