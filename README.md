# Student Feedback Registration Form

A complete DevOps CA-2 project: web form with validation, automated Selenium testing, and Jenkins CI/CD pipeline.

---

## 📁 Project Structure

```
ca2/
├── index.html                  # HTML form (Sub-Task 1)
├── css/
│   └── style.css               # External CSS (Sub-Task 2)
├── js/
│   └── validation.js           # JavaScript validation (Sub-Task 3)
├── tests/
│   ├── test_feedback_form.py   # Selenium tests (Sub-Task 4)
│   └── requirements.txt        # Python dependencies
├── Jenkinsfile                 # Jenkins pipeline (Sub-Task 5)
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1. View the Form

Open `index.html` directly in any modern browser — no server required.

```
# Windows
start index.html

# macOS
open index.html
```

### 2. Run Selenium Tests Locally

**Prerequisites:** Python 3.x, pip, Google Chrome

```bash
# Install dependencies
pip install -r tests/requirements.txt

# Run all 7 test cases
python -m pytest tests/test_feedback_form.py -v

# Generate HTML report
python -m pytest tests/test_feedback_form.py -v --html=reports/test-report.html --self-contained-html
```

---

## ✅ Test Cases (Sub-Task 4)

| #   | Test Case                       | Description                                    |
| --- | ------------------------------- | ---------------------------------------------- |
| 1   | `test_page_loads`               | Form page opens; title & heading verified      |
| 2   | `test_valid_submission`         | All fields valid → success toast appears       |
| 3   | `test_empty_fields`             | Submit blank form → all 6 error messages shown |
| 4   | `test_invalid_email`            | Bad email → email validation error             |
| 5   | `test_invalid_mobile`           | Non-numeric mobile → mobile validation error   |
| 6   | `test_dropdown_selection`       | Each department option selectable and verified |
| 7   | `test_submit_and_reset_buttons` | Submit validates; Reset clears all fields      |

---

## 🔧 Jenkins Setup (Sub-Task 5)

### Step 1 — Install Jenkins

1. Download Jenkins from [jenkins.io](https://www.jenkins.io/download/)
2. Install and start Jenkins (default port: `8080`)
3. Complete initial setup wizard and install recommended plugins

### Step 2 — Install Required Plugins

- **JUnit Plugin** (usually pre-installed)
- **HTML Publisher Plugin** (for HTML test reports)
- **Pipeline Plugin** (usually pre-installed)

### Step 3 — Create a Pipeline Job

1. **New Item** → Enter a name (e.g., `Student-Feedback-Tests`) → Select **Pipeline** → OK
2. Under **Pipeline** section:
   - **Definition:** `Pipeline script from SCM`
   - **SCM:** Git
   - **Repository URL:** Your GitHub repo URL (or local path)
   - **Script Path:** `Jenkinsfile`
3. Click **Save**

### Step 4 — Run the Build

1. Click **Build Now**
2. View console output for real-time progress
3. After completion, check:
   - **Test Results** tab for pass/fail summary
   - **Archived Artifacts** for the HTML report

### Agent Prerequisites

The Jenkins agent must have:

- Python 3.x with `pip`
- Google Chrome installed
- Internet access (for `webdriver-manager` to download ChromeDriver)

---

## 📝 Validation Rules (Sub-Task 3)

| Field             | Validation Rule                              |
| ----------------- | -------------------------------------------- |
| Student Name      | Must not be empty                            |
| Email ID          | Must match standard email format             |
| Mobile Number     | Must be exactly 10 digits (numbers only)     |
| Department        | Must select a department from the dropdown   |
| Gender            | At least one radio button must be selected   |
| Feedback Comments | Must not be blank; minimum 10 words required |

---

## 🎨 Design Features (Sub-Task 2)

- **Glassmorphism** card with backdrop blur
- **Gradient background** with animated blobs
- **Google Fonts** (Inter) for modern typography
- **Custom radio buttons** and styled dropdown
- **Real-time validation** with inline error messages
- **Live word counter** on feedback textarea
- **Success toast** notification on valid submission
- **Fully responsive** design (mobile & desktop)
- Both **Internal CSS** (animations in `<style>`) and **External CSS** (`css/style.css`)

---

## 📄 License

This project is created for academic purposes (DevOps CA-2).
