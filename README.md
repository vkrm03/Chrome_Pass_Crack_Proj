# 🔐 Chrome Saved Password Cracking Tool

> **For Educational & Research Purposes Only**  
This project demonstrates how saved passwords in Google Chrome can be extracted and decrypted from the local system.  
It is intended **only** for cybersecurity learning, awareness, and penetration testing in controlled environments.

---

## ⚡ Overview

Google Chrome stores saved login credentials in a local SQLite database (`Login Data`).  
Older versions used simple DPAPI encryption (Windows) or Keychain (Mac).  
**But newer versions (post-Chrome 80)** now use **AES-GCM encryption** with a master key stored in the `Local State` file.  

This tool:
- Extracts saved login data (URLs, usernames, encrypted passwords).  
- Fetches the AES master key from `Local State`.  
- Decrypts the encrypted password using DPAPI / AES-GCM.  
- Displays cracked credentials in a readable format.  

---

## 🛠 Features
- Works with older and newer Chrome versions (pre/post v80).  
- Cross-platform support (Windows / Linux / Mac).  
- Password decryption via DPAPI (Windows) or AES-GCM (all OS).  
- Export results as plaintext or CSV.  

---

## 📂 How it Works
1. Locate Chrome profile directory:
   - Windows: `%LOCALAPPDATA%\Google\Chrome\User Data\Default`
   - Linux: `~/.config/google-chrome/Default`
   - MacOS: `~/Library/Application Support/Google/Chrome/Default`

2. Extract encrypted passwords from the `Login Data` SQLite DB.  

3. Fetch AES encryption key:
   - Windows: From `Local State` (DPAPI-protected key).  
   - MacOS: From Keychain.  
   - Linux: From `gnome-keyring` or `kwallet`.  

4. Decrypt password blobs:
   - Pre-Chrome 80 → DPAPI.  
   - Post-Chrome 80 → AES-GCM with DPAPI-unwrapped master key.  

---

## 🚀 Usage

```bash
git clone https://github.com/your-username/chrome-password-cracker.git
cd chrome-password-cracker

# Install requirements
pip install -r requirements.txt

# Run the tool
python chrome_password_cracker.py
