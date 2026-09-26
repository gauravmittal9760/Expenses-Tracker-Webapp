# SpendWise — Smart Personal Expense Management & Financial Analytics Web Application

SpendWise is a modern Flask-based personal expense management and financial analytics web application designed to help users manage their expenses, income, budgets, savings goals, and financial activity through a secure and responsive interface.

The application also provides data-driven Machine Learning features for spending forecasting, unusual expense detection, and personalized financial insights.

---

## Features

### User Authentication & Security

- User Registration and Login
- Secure Password Hashing
- OTP Verification
- Two-Step Verification
- Forgot Password
- Forgot Username
- Security Question and Answer
- Login Activity Monitoring
- Account Security Management
- Password and Email Management

### Expense Management

- Add Expenses
- Edit Expenses
- Delete Expenses
- Expense Categories
- Expense Description
- Expense Date Tracking
- Expense Image Upload (cloud-hosted via Cloudinary)
- Expense Memory Gallery
- Search Expenses
- Search by Category
- Search by Amount
- Search by Date
- Filter Expenses by Date
- Sort Expenses by Amount
- Monthly Expense Reports
- Expense Management Center

### Budget, Income & Savings

- Monthly Budget Management
- Income Tracking
- Current Balance Monitoring
- Budget Warnings
- Savings Goals
- Savings-Oriented Financial Insights
- Budget and Income Editing

### Analytics & Machine Learning

- Analytics Dashboard
- Category-Wise Spending Analysis
- Expense Charts
- Expense Statistics
- Monthly Spending Analysis
- Expense Predictions
- 30-Day Spending Forecasting
- Machine Learning Based Spending Predictions
- Unusual Expense Detection
- Personalized Expense Insights
- Data-Driven Savings Recommendations
- Budget-Based Financial Insights

### Admin Panel

- Admin Authentication
- Admin Security Verification
- User Management
- View Registered Users
- View User Expenses
- Delete Users
- User Login Records
- Account Activity Monitoring
- Application Management
- Application Backup Features (includes cloud-hosted images, downloaded into the backup ZIP)
- Application Reset Features (also purges cloud-hosted images on full reset)

### Account & Additional Features

- Profile Picture Upload (cloud-hosted via Cloudinary)
- Account Details Management
- Notification Settings
- Currency Management
- Change Password
- Change Email
- Change Security Question
- Login Activity Center
- CSV Export
- Excel Export
- PDF Reports (with cloud-hosted receipt images embedded)
- Print Statements
- Responsive User Interface
- Dark Futuristic Design

---

## AI & Machine Learning

SpendWise uses free, local Machine Learning techniques to analyse historical expense data without requiring a paid OpenAI API.

### Random Forest Regression

Random Forest Regression is used to analyse historical spending patterns and generate a 30-day future spending forecast.

The forecasting system can use features derived from historical expense data, including:

- Day of Week
- Day of Month
- Month
- Previous-Day Spending
- Rolling Spending Patterns
- Historical Expense Trends

The prediction system becomes more meaningful as the application collects more historical expense records.

### Isolation Forest

Isolation Forest is used for unusual expense detection.

It analyses recorded transactions and identifies expenses that differ significantly from the user's normal spending behaviour.

The analysis can consider information such as:

- Expense Amount
- Expense Category
- Date-Based Features
- Historical Spending Behaviour

### Personalized Expense Insights

SpendWise combines financial and analytical information such as:

- Historical Expense Patterns
- Category-Wise Spending
- Recent Spending Trends
- Machine Learning Forecasts
- Unusual Expense Detection
- Budget Information
- Income Information

to generate personalized, data-driven financial insights and savings-oriented recommendations.

> The Machine Learning and insight features are designed to work without requiring a paid external AI API.

---

## Technology Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Mail
- Gunicorn

### Machine Learning & Data Analysis

- Scikit-learn
- Pandas
- NumPy
- Matplotlib

### Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Chart.js

### Database

- PostgreSQL
- Neon PostgreSQL for persistent cloud database hosting
- SQLite for supported local development scenarios

### Media & File Storage

- **Cloudinary** — cloud-hosted storage for all user-uploaded images (expense receipts and profile pictures)
- Pillow — image compression before embedding into PDFs
- OpenPyXL — Excel export
- FPDF — PDF report generation

### Deployment

- Render
- Vercel
- Neon PostgreSQL
- Cloudinary

---

## Database Architecture

SpendWise uses PostgreSQL for its production deployment database.

The current cloud deployment uses **Neon PostgreSQL**, allowing the application's user accounts, expenses, login records, budgets, savings goals, notification settings, and other application data to remain available independently of the web hosting platform.

The application connects to the database through the `DATABASE_URL` environment variable.

Sensitive configuration values such as database credentials, secret keys, email credentials, and administrator credentials are stored through environment variables rather than being committed to the GitHub repository.

---

## Image & Media Storage (Cloudinary)

All user-uploaded images — expense receipts and profile pictures (including the admin profile picture) — are stored on **Cloudinary** instead of the application's local filesystem.

This is required for hosting on **Vercel**, whose serverless functions run on a **read-only filesystem** (only the OS temp directory is writable, and it does not persist between requests). Saving uploads with a local `file.save()` call works on a traditional host like Render but fails with an Internal Server Error on Vercel. Cloudinary removes this limitation entirely, so uploads, edits, and deletions all work identically on both Render and Vercel.

- New uploads (expense images, user profile pictures, admin profile picture) are uploaded directly to Cloudinary and only the returned `secure_url` is stored in the database.
- Deleting an expense, removing an image from an expense, or replacing a profile picture also removes the corresponding image from Cloudinary.
- PDF export downloads each receipt image from its Cloudinary URL on demand (into a temporary file) before embedding it in the generated report.
- Admin backup (`Full App Backup` / per-user backup) downloads all Cloudinary-hosted images into the backup ZIP so the archive remains a complete, self-contained copy.
- Legacy local image filenames (from before this migration) are still supported as a fallback wherever images are read, so existing records are not broken.

### Required Cloudinary Environment Variables

| Variable | Description |
|---|---|
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary account's cloud name |
| `CLOUDINARY_API_KEY` | Your Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Your Cloudinary API secret |

These must be set on **both** Render and Vercel (alongside `DATABASE_URL`, `SECRET_KEY`, etc.) — the application will not be able to store images without them.

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `SECRET_KEY` | Flask session secret key |
| `BREVO_API_KEY` | Brevo (Sendinblue) API key for transactional emails / OTPs |
| `MAIL_DEFAULT_SENDER` | Default sender email address |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |

None of these should ever be committed to the GitHub repository — configure them through Render's and Vercel's environment variable settings.

---

## Project Structure

```text
Expenses-Tracker-Webapp/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── readme.md
├── .gitignore
│
├── ml/
│   ├── __init__.py
│   ├── anomaly_detection.py
│   ├── feature_engineering.py
│   └── forecasting.py
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── all_expenses.html
│   ├── edit_expense.html
│   ├── edit_expense_list.html
│   ├── expense_predictions.html
│   ├── ai_insights.html
│   ├── analytics.html
│   ├── expense_charts.html
│   ├── expense_statistics.html
│   ├── budget_warnings.html
│   ├── expense_gallery.html
│   ├── admin_dashboard.html
│   └── ...
│
├── static/
│   ├── uploads/        (legacy local uploads, kept only as a fallback)
│   └── ...
│
└── Screenshots/
    ├── login.png
    ├── signup.png
    ├── dashboard.png
    └── admin.png
```

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/gauravmittal9760/expense-tracker-webapp.git
```

### 2. Go Into the Project Folder

```
cd expense-tracker-webapp
```

### 3. Create a Virtual Environment

```
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```
venv\Scripts\activate
```

### 5. Install Dependencies

```
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file (or configure your host's environment variable settings) with the values listed in [Environment Variables](#environment-variables), including the Cloudinary credentials.

### 7. Run the Application

```
python app.py
```

The application will then be available through the local Flask server.

---

## Machine Learning Requirements

For reliable ML forecasting, the application requires sufficient historical expense data.

The forecasting system recommends maintaining expense records across multiple dates so that meaningful spending patterns can be identified.

The anomaly detection system can analyse recorded transactions and identify potentially unusual spending behaviour.

---

## Screenshots

### Login Page

![Login Page](Screenshots/login.png)

### Signup Page

![Signup Page](Screenshots/signup.png)

### Dashboard

![Dashboard](Screenshots/dashboard.png)

### Admin Panel

![Admin Panel](Screenshots/admin.png)

---

## Deployment

SpendWise is deployed using both **Render** (with Gunicorn) and **Vercel**.

Image uploads (expense receipts, profile pictures, admin profile picture) are stored on **Cloudinary**, which makes the application's image handling fully compatible with Vercel's read-only serverless filesystem as well as Render's persistent one. Make sure the Cloudinary environment variables are configured on whichever platform(s) you deploy to.

The application supports production deployment using the dependencies specified in `requirements.txt`.

---

## Future Scope

Possible future improvements include:

* More advanced time-series forecasting
* Improved personalized financial recommendations
* Additional ML models
* Automatic expense categorization
* More advanced anomaly analysis
* Financial goal prediction
* Mobile application
* Improved notification and reminder system
* Advanced financial dashboards

---

## Project Author

**Gaurav Mittal**

B.Tech — Computer Science & Engineering

---

## Project

**SpendWise — Expense Tracker Web Application**

A major project focused on expense management, financial analytics, and Machine Learning based spending insights.