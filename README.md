
---

# 🎵 MKDL Player

A lightweight, high-performance music player built with **Python**, **PyQt6**, and **Pygame**. It features a minimalist dark interface, real-time Discord Rich Presence (RPC) integration, and ultra-low memory consumption (approx. **83MB**).

## ✨ Features

* **Discord Rich Presence**: Automatically displays your current track and elapsed time on your Discord profile.
* **Minimalist Design**: Clean, dark UI optimized for focus and low resource usage.
* **Broad Format Support**: Plays `.mp3`, `.flac`, and `.opus` files.
* **Linux Integration**: Includes a script to generate a `.desktop` entry for your application menu.

***Preview***:

<img width="598" height="239" alt="image" src="https://github.com/user-attachments/assets/316089da-65cd-4ad6-a90a-8cfd7bf8a0bc" />

In my application launcher (wofi):

<img width="579" height="321" alt="image" src="https://github.com/user-attachments/assets/fa649911-d0a7-404f-8dba-7fcd70bff5a7" />



## 🛠️ Installation

### 1. Prerequisites

Ensure you have Python installed, then install the required libraries:

```bash
pip install PyQt6 pygame pypresence

```
or 

```bash
pip install -r requirements.txt

```
### 2. Setup & Desktop Entry

To integrate the player into your Linux application menu, run the provided setup script:

```bash
chmod +x add-to-path.sh
./add-to-path.sh

```

This script detects your project path and creates a `mkdlplayer.desktop` file in `~/.local/share/applications/`.

## 🎮 Discord Rich Presence 

The application have Drp :3

**Preview:**

<img width="283" height="90" alt="image" src="https://github.com/user-attachments/assets/f60aa8b6-ef1e-4fba-9fd0-d5100a4b9cbf" />


## 📂 Project Structure

* `mkdlplayer.py`: The main application code.
* `add-to-path.sh`: Linux installation and desktop entry script.
* `assets/`: Folder containing the application icon (`logo.png`).

## 🚀 Usage

* **FILE**: Open a single audio file.
* **FOLDER**: Load an entire directory into the playlist.
* **REPEAT**: Toggle between single-track loop and standard playback.
* **VOL**: Adjustable volume slider.

---

Developed by: Ars-byte and Franckey02 :)
