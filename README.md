# 🐍 SnakeRAT – Educational Remote Access Tool

SnakeRAT is an **educational Remote Access Tool (RAT)** embedded inside a classic Snake game.  
The project demonstrates how attackers may disguise malicious payloads in legitimate applications,  
and how defenders can analyze such techniques in a controlled environment.  

⚠️ **Disclaimer:** This project is strictly for **educational and research purposes only**.  
Do not use it for any unauthorized access or malicious activity.  

---

## 🚀 Features
- 🎮 **Snake Game Interface** – Fun frontend that masks background network activity.
- 🌐 **Client-Server Communication** – Built using socket programming over TCP/IP.
- 🖥️ **Remote System Interaction** – Supports screen capture, webcam snapshots, and directory listing.
- 🔒 **Cross-Network Access** – Connectivity extended beyond localhost using Ngrok and port forwarding.
- 🛡️ **Cybersecurity Simulation** – Demonstrates common attack vectors for defense and analysis.

---

## 🛠️ Tech Stack
- **Programming Language:** Python  
- **Networking:** Socket Programming, TCP/IP, Port Forwarding, Ngrok  
- **System Access:** OpenCV (webcam), PyAutoGUI (screen capture), OS APIs (file operations)  
- **Security Tools:** Wireshark, Nmap (for analysis & testing)  

---

## 📂 Project Structure
SnakeRAT/
│── server.py # Server file that listens for incoming connections
│── client.py # Snake game + RAT functionality
│── requirements.txt # Python dependencies
│── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/navneet1517/SnakeRAT.git
   cd SnakeRAT
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Start the server:

bash
Copy code
python server.py
Run the client (game):

bash
Copy code
python client.py
For cross-network communication, configure Ngrok or port forwarding.

📸 Demo (Educational Simulation)
Run the server locally to listen for connections.

Launch the client game on another machine or VM.

Observe captured screenshots, webcam images, and directory listings on the server.

🔐 Ethical Usage
This project was built as part of cybersecurity research and education.
It can be used to understand:

How Remote Access Tools function at a low level.

How attackers embed payloads into normal applications.

How defenders can detect and mitigate such threats.

📚 Learning Outcomes
Socket programming and TCP/IP networking.

Client-server architecture and tunneling.

Remote system access simulation.

Cybersecurity principles: attack vectors and defensive strategies.

🧑‍💻 Author
Navneet Singh

GitHub: navneet1517

yaml
Copy code

---

