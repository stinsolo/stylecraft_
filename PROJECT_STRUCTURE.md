# Project Architecture & Directory Structure

This document outlines the organization of the codebase, the roles of various Django apps, the structure of HTML templates, and the relationship between database tables.

---

## Codebase Directory Structure

```text
tailoring/
│
├── Admin/                  # Administrator app
├── staff/                  # Staff/Tailor app
├── user/                   # Customer app
│
├── Templates/              # HTML templates
├── static/                 # CSS, JS, images
├── media/                  # Uploaded files (if used)
│
├── tailoring/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── README.md
├── INSTALLATION.md
├── PROJECT_STRUCTURE.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
└── CODE_OF_CONDUCT.md

---

## Database Models & Relationships

The database system is organized across three primary applications:

### 1. Admin App Models (`Admin/models.py`)
* **`Admin_login`**:
  * Fields: `email` (primary key), `password`.
  * Purpose: Stores credentials for admin portals.
* **`upload_templates`**:
  * Fields: `image1`, `image2`, `image3`, `price`, `description`, `item_name`.
  * Purpose: Standard design choices uploaded by administrators for customers to pick.

### 2. Staff App Models (`staff/models.py`)
* **`Staff_reg`**:
  * Fields: `username`, `email`, `password`, `status`.
  * Purpose: Tailors and staff records.

### 3. User App Models (`user/models.py`)
* **`User_Reg`**:
  * Fields: `username`, `email` (primary key), `password`, `address`, `gender`.
  * Purpose: Customer registration table.
* **`Upload_details`**:
  * Fields: `username` (ForeignKey to `User_Reg`), and measurement fields: `waist`, `hips`, `bust`, `chestgirth`, `neck`, `shoulder`, `sleeve`, `bicep`, `wrist`, `back_waist_length`.
  * Purpose: Persistent customer measurement profiles.
* **`Order_table`**:
  * Fields: `item_name` (ForeignKey to `upload_templates`), `status`, `make_sts`, `username` (ForeignKey to `User_Reg`), `image1`, `image2`, `image3`, and measurement fields.
  * Purpose: Customer order catalog with specific measurements and reference design uploads.
* **`OrderStatus`**:
  * Fields: `order` (ForeignKey to `Order_table`), `status` (integer state), `staff` (ForeignKey to `Staff_reg`), `rate`.
  * Purpose: Links specific orders to tailors and tracks the stages from placement to delivery.

---

## Templates Structure

Templates are divided into three user space namespaces matching the backend modules:
* `/Templates/Admin/`: Interfaces to configure templates, add staff, review reports, and audit feedback.
* `/Templates/Staff/`: Interface for tailors to view their queue and update task states.
* `/Templates/User/`: Shop layouts, payment simulation screens, measurement configuration pages, and AI dress generation tools.
