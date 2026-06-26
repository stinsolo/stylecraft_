# Detailed Installation Guide

Follow these step-by-step instructions to get the Tailoring Management System running on your local machine.

---

## 1. System Requirements
* **Python**: 3.10.x or newer
* **Database**: SQLite3 (included in python)
* **Pip**: Latest version recommended
* **API Access**: A Clipdrop API account (optional, needed only for AI dress generation)

---

## 2. Step-by-Step Installation

### Step A: Clone the Repository
```bash
git clone https://github.com/your-username/tailoring.git
cd tailoring
```

### Step B: Setup Virtual Environment
* **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step C: Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step D: Setup Environment Settings
Create a `.env` file at the root of the repository:
```ini
DEBUG=True
SECRET_KEY=django-insecure-)fiiqdn9bx(_-pn&wl_mef6^4a5=+8zgup$nqs!e2a%ui)d3v_
CLIPDROP_API_KEY=your_clipdrop_api_token_here
```

> [!NOTE]
> Keep the production `SECRET_KEY` secret. The `.env` file is excluded from git commits via `.gitignore`.

### Step E: Database Migrations
Run the following Django management commands to prepare the SQLite schema database:
```bash
python tailoring/manage.py makemigrations
python tailoring/manage.py migrate
```

### Step F: Running the Server
Launch the development server:
```bash
python tailoring/manage.py runserver
```
Navigate to `http://127.0.0.1:8000` in your web browser.

---

## 3. Account Setup and Authentication

This application uses a custom user model and authentication system instead of standard Django built-in authentication views.

### Administrator Setup
To register your first system administrator:
1. Navigate to: `http://127.0.0.1:8000/admin_reg/`
2. Enter your email and a strong password.
3. Click "Submit". This registers the administrator account inside the database table `Admin_login`.
4. Log in at `http://127.0.0.1:8000/admin_log/`.

### Tailor Staff Setup
1. Log in as an Administrator.
2. Go to the Staff Registration view at `http://127.0.0.1:8000/staff_reg/`.
3. Input username, email, password, and gender.
4. Staff can now log in at `http://127.0.0.1:8000/staff/user_login`.

### Customer Setup
1. Go to the login page `http://127.0.0.1:8000/user/user_login`.
2. Click **Register** or navigate to `http://127.0.0.1:8000/user/userReg`.
3. Fill out the details (Username, Email, Password, Address, Gender).
4. Log in to start browsing custom templates, uploading measurements, and using the AI dress generator!
