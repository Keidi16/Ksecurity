## KSecurity 1.0
Linux Security Monitor is a project aimed at enhancing server security by monitoring Apache server logs and all system connections. The basic version of this tool provides two core functionalities:

1. **Apache Server Log Monitoring**
   - Detects and monitors potential fuzzing attacks against the Apache server running on port 80.
   - Keeps an eye on attempts to access restricted administrative files.

2. **System Connection Monitoring**
   - Monitors all connections, whether internal or external, to identify instances of Reverse Shells or Shell Reverses.
   - Provides vigilant oversight of these processes.

This project is designed to help bolster the security of your Linux server by actively identifying and responding to suspicious activities. It's an essential addition to your cybersecurity toolkit.

### Features:
- Real-time monitoring of Apache server logs.
- Detection and alerting of potential security threats.
- Comprehensive tracking of system connections.
- User-friendly and easily configurable.

### Installation

You can easily get started with KSecurity by following these steps:

1. Clone the repository to your local machine using Git:

```bash
git clone https://github.com/Keidi16/Ksecurity.git
pip install multiprocessing
pip install colorama
```
### Usage

To run KSecurity, follow these steps:

1. Make the `ksecurity.py` script executable by running the following command in your terminal:

```bash
chmod +x ksecurity.py
python3 ksecurity.py

