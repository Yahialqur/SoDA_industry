# SoDA Industry Email Automation Script

An automated email script for sending SoDA Industry Emails

## How to use

1. Clone this repository
2. Create and activate a Python virtual environment (recommended):

```bash
# Create a virtual environment (macOS / zsh)
python3 -m venv venv
# Activate the virtual environment
source venv/bin/activate
```

3. Install required Python packages:
```bash
# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Setup

### 1. Create Environment File

Create a `.env` file in the same directory as [email_script.py](email_script.py) and add the following, with your email and password:

```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password-here
```

### 2. Prepare Your CSV File

Create a CSV file (e.g., `recipients.csv`) with the following format:

```csv
Name,Company,Email Address
John Doe,Microsoft,john.doe@microsoft.com
Jane Smith,Google,jane.smith@google.com
Bob Johnson,Amazon,bob.johnson@amazon.com
```

**Required columns**:
- `Name`: Full name of the recipient
- `Company`: Company name (used in email personalization)
- `Email Address`: Recipient's email address

### 4. Add Your Sponsorship Package

Place your PDF sponsorship package in the same directory as the script and name it `SoDA_Sponsorship_Package.pdf`, or update the `ATTACHMENT_PATH` variable in [email_script.py:26](email_script.py#L26) to match your file name.

## Usage

### Basic Usage

1. Update the CSV file path in [email_script.py:164](email_script.py#L164):
```python
CSV_FILE = "recipients.csv"  # Change this to your CSV file path
```

2. Run the script:
```bash
python email_script.py
```