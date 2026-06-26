# Project Architecture & Directory Structure

This document outlines the organization of the codebase, the roles of various Django apps, the structure of HTML templates, and the relationship between database tables.

---

## Codebase Directory Structure

```text
tailoring/
│
├── tailoring/                  # Main project directory
│   │
│   ├── tailoring/              # Inner project configuration files
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py         # Django settings, security & file dirs
│   │   ├── urls.py             # Global URL dispatch config
│   │   └── wsgi.py             # WSGI configuration
│   │
│   ├── Admin/                  # Admin functions and management
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Admin_login, Addi_staff, upload_templates models
│   │   ├── urls.py             # Admin endpoints (/staff_reg/, /add_temp/, etc.)
│   │   └── views.py            # Logic for templates upload, staff updates, assignments
│   │
│   ├── staff/                  # Tailor / Worker app
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # Staff_reg model
│   │   ├── urls.py             # Staff endpoints (/user_login, /staff_home)
│   │   └── views.py            # Dashboards and order progression logic
│   │
│   ├── user/                   # Customer app
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py           # User_Reg, Upload_details, Order_table, OrderStatus
│   │   ├── urls.py             # Customer endpoints (/place_order, /generate_dress)
│   │   └── views.py            # AI integration, measurement uploads, orders, payment
│   │
│   ├── Templates/              # HTML Templates directory
│   │   ├── Admin/              # Admin pages (e.g. viewstaff.html, addtemplates.html)
│   │   ├── Staff/              # Tailor pages (e.g. staffhome.html, update_order_status.html)
│   │   └── User/               # Client pages (e.g. ai.html, userhome.html, order.html)
│   │
│   ├── static/                 # Static asset delivery directory
│   │   ├── css/                # Client styles stylesheets
│   │   ├── js/                 # Interactions Javascript files
│   │   └── generated_images/   # Store generated AI PNG outputs
│   │
│   ├── media/                  # Media files root (stores uploaded designs)
│   │   └── Uploads/            # Uploaded templates images folder
│   │
│   ├── manage.py               # Django manage script
│   └── db.sqlite3              # Local SQLite Database file (excluded in .gitignore)
│
├── .env.example                # Example configuration template file
├── .gitignore                  # Exclusion file for git commits
├── requirements.txt            # Package list requirements
├── LICENSE                     # Software license (MIT)
├── README.md                   # Repository overview guide
├── INSTALLATION.md             # Running and deploying documentation
└── PROJECT_STRUCTURE.md        # Current architectural guide
```

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
