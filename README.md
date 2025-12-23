# Expense Management System

A Flask-based Expense Management System that helps organizations manage employees, projects, expenses, revenue, and financial reports through a web-based interface.

## FEATURES

* **Employee Management:** Add, edit, and view employee details.
* **Project Management:** Create and manage projects; view project-wise information.
* **Expense Tracking:** Record and manage expenses; associate expenses with projects.
* **Revenue Management:** Track revenue records; monitor financial performance.
* **Reports and Forecasting:** Generate financial reports; view expense and revenue forecasts.
* **User Interface:** Clean interface using HTML, CSS, and Jinja2 templates.

## TECH STACK

| Component | Technology |
| :--- | :--- |
| **Backend** | Python (Flask) |
| **Frontend** | HTML, CSS, Jinja2 |
| **Database** | SQLite |
| **ORM** | SQLAlchemy |
| **Forms** | Flask-WTF |

## PROJECT STRUCTURE

```text
Expense-Management-System/
├── app.py
├── config.py
├── models.py
├── routes.py
├── forms.py
├── Requirements.txt
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── employees.html
│   ├── edit_employee.html
│   ├── projects.html
│   ├── view_project.html
│   ├── expenses.html
│   ├── revenue.html
│   ├── report.html
│   └── forecast.html
└── README.md

```


## INSTALLATION AND SETUP

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/Expense-Management-System.git
cd Expense-Management-System
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
```
Step 3: Activate the Virtual Environment
Windows:

```bash


venv\Scripts\activate
```

Linux / macOS:

```bash

source venv/bin/activate
```
Step 4: Install Dependencies
```bash

pip install -r Requirements.txt
```
Step 5: Run the Application
```bash


python app.py
```
Step 6: Open in Browser
```bash

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
```
