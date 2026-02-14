"""
Indeed Job Auto-Application Bot
Built for: Sakina Shrestha
Purpose: Automatically apply to 50+ jobs per day on Indeed
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    NoSuchWindowException,
    WebDriverException,
    StaleElementReferenceException
)
import time
import json
import os
import random
from datetime import datetime

# ==================== YOUR INFORMATION ====================
USER_INFO = {
    "full_name": "Sakina Shrestha",
    "first_name": "Sakina",
    "last_name": "Shrestha",
    "email": "sakustha12@gmail.com",
    "alt_email": "sashr5@morgan.edu",

    # Indeed Login (for external applications)
    "indeed_email": "sakustha12@gmail.com",  # Your Indeed account email
    "indeed_password": "",  # <-- ADD YOUR INDEED PASSWORD HERE
    "phone": "6673048390",
    "formatted_phone": "667-304-8390",
    "address": "2 E Joppa Rd, Apt 1170",
    "city": "Towson",
    "state": "MD",
    "zip_code": "21286",
    "country": "United States",
    "linkedin": "https://www.linkedin.com/in/sakina-shrestha-474775273/",
    "portfolio": "https://SakinaShrestha111.github.io",
    "github": "https://github.com/Sakinastha",
    
    # Education
    "degree": "Bachelor of Science",
    "major": "Computer Science",
    "university": "Morgan State University",
    "graduation_month": "December",
    "graduation_year": "2025",
    "gpa": "3.96",
    
    # Work Experience
    "years_experience": "2",
    "current_company": "Morgan State University",
    "current_title": "Research Assistant",
    
    # Work Authorization (IMPORTANT for F-1 OPT)
    "work_authorized_us": "yes",  # Yes, currently on F-1 OPT
    "require_sponsorship_now": "no",  # No sponsorship needed NOW (on OPT)
    "require_sponsorship_future": "yes",  # YES for future H-1B
    "visa_status": "F-1 OPT",
    
    # Preferences
    "willing_to_relocate": "yes",
    "willing_remote": "yes",
    "salary_expectation": "70000",
    
    # Demographics (for EEO questions)
    "gender": "Female",
    "race": "Asian",
    "ethnicity": "Not Hispanic or Latino",
    "veteran": "No",
    "disability": "No",
    "lgbtq": "Decline to self-identify",  # Changed for privacy
    
    # Resume path - UPDATE THIS!
    "resume_path": "/Users/sakina/Downloads/Sakina_Shrestha_resume.pdf",

    # Account Creation (for external career sites)
    "job_app_password": "JobSeeker2025!",  # Dedicated password for job sites ONLY

    # Skills & Technologies (for screening questions)
    "programming_languages": ["Python", "Java", "JavaScript", "SQL", "C++", "R"],
    "frameworks": ["React", "Django", "Flask", "Node.js", "TensorFlow", "PyTorch"],
    "tools": ["Git", "Docker", "AWS", "Linux", "VS Code", "Jupyter", "Tableau"],

    # Availability
    "start_date": "Immediately",
    "notice_period": "2 weeks",
    "available_hours": "Full-time",

    # Additional Answers for screening questions
    "willing_to_travel": "yes",
    "travel_percentage": "25",
    "has_drivers_license": "yes",
    "has_vehicle": "yes",
    "background_check_ok": "yes",
    "drug_test_ok": "yes",
    "night_shift_ok": "yes",
    "weekend_ok": "yes",
    "overtime_ok": "yes",
    "us_citizen": "no",
    "clearance_eligible": "no",
    "age_18_or_older": "yes",
}

# Job search configuration - CAST A WIDE NET!
JOB_KEYWORDS = [
    # Software Engineering
    "software engineer entry level",
    "software developer new grad",
    "full stack developer",
    "backend engineer",
    "frontend engineer",
    "python engineer",
    
    # AI/ML/Data
    "AI engineer",
    "machine learning engineer",
    "data scientist",
    "data engineer",
    "data analyst",
    "business analyst",
    "BI analyst",
    
    # DevOps/Infrastructure
    "devops engineer",
    "cloud engineer",
    "systems engineer",
    "infrastructure engineer",
    "site reliability engineer",
    
    # QA/Testing
    "QA engineer",
    "software tester",
    "automation engineer",
    "test engineer",
    
    # Other IT Roles
    "IT support",
    "technical support",
    "database administrator",
    "cybersecurity analyst",
    "security engineer",
    
    # Project/Product Management
    "technical project manager",
    "project coordinator",
    "product analyst",
    "scrum master",
    
    # Consulting
    "IT consultant",
    "technology analyst",
    "solutions engineer"
]

LOCATIONS = ["Remote", "United States"]  # Wide open - anywhere in the US!

# ==================== CONFIGURATION ====================
APPLIED_JOBS_FILE = "applied_jobs.json"
SESSION_STATE_FILE = "session_state.json"
FAILED_JOBS_FILE = "failed_jobs.json"
MAX_APPLICATIONS_PER_SESSION = 50

# ==================== SMART QUESTION ANSWERS DATABASE ====================
# This database maps common screening question keywords to appropriate answers
QUESTION_ANSWERS = {
    # Experience & Skills
    "years of experience": USER_INFO["years_experience"],
    "years experience": USER_INFO["years_experience"],
    "programming languages": ", ".join(USER_INFO["programming_languages"]),
    "coding languages": ", ".join(USER_INFO["programming_languages"]),
    "tools and technologies": ", ".join(USER_INFO["tools"]),
    "frameworks": ", ".join(USER_INFO["frameworks"]),

    # Availability
    "start date": USER_INFO["start_date"],
    "when can you start": USER_INFO["start_date"],
    "available to start": "yes",
    "earliest start": USER_INFO["start_date"],
    "notice period": USER_INFO["notice_period"],
    "two weeks notice": "yes",

    # Work Preferences
    "salary expectation": USER_INFO["salary_expectation"],
    "expected salary": USER_INFO["salary_expectation"],
    "desired salary": USER_INFO["salary_expectation"],
    "minimum salary": USER_INFO["salary_expectation"],
    "willing to travel": USER_INFO["willing_to_travel"],
    "travel required": USER_INFO["willing_to_travel"],
    "percent travel": USER_INFO["travel_percentage"],
    "travel percentage": USER_INFO["travel_percentage"],
    "willing to relocate": USER_INFO["willing_to_relocate"],
    "open to relocation": USER_INFO["willing_to_relocate"],
    "remote work": USER_INFO["willing_remote"],
    "work remotely": USER_INFO["willing_remote"],
    "hybrid": "yes",
    "on-site": "yes",
    "in-office": "yes",

    # Background & Legal
    "background check": USER_INFO["background_check_ok"],
    "criminal background": USER_INFO["background_check_ok"],
    "drug test": USER_INFO["drug_test_ok"],
    "drug screen": USER_INFO["drug_test_ok"],
    "driver's license": USER_INFO["has_drivers_license"],
    "drivers license": USER_INFO["has_drivers_license"],
    "valid license": USER_INFO["has_drivers_license"],
    "own vehicle": USER_INFO["has_vehicle"],
    "reliable transportation": "yes",

    # Work Schedule
    "night shift": USER_INFO["night_shift_ok"],
    "evening shift": USER_INFO["night_shift_ok"],
    "weekend": USER_INFO["weekend_ok"],
    "overtime": USER_INFO["overtime_ok"],
    "full-time": "yes",
    "full time": "yes",
    "part-time": "no",
    "part time": "no",
    "hours per week": "40",

    # Age & Eligibility
    "18 years": USER_INFO["age_18_or_older"],
    "over 18": USER_INFO["age_18_or_older"],
    "at least 18": USER_INFO["age_18_or_older"],
    "21 years": "yes",
    "over 21": "yes",

    # Education
    "highest degree": f"{USER_INFO['degree']} in {USER_INFO['major']}",
    "education level": USER_INFO["degree"],
    "gpa": USER_INFO["gpa"],
    "graduation": f"{USER_INFO['graduation_month']} {USER_INFO['graduation_year']}",
    "graduation date": f"{USER_INFO['graduation_month']} {USER_INFO['graduation_year']}",

    # Work Authorization (F-1 OPT specific)
    "authorized to work": USER_INFO["work_authorized_us"],
    "legally authorized": USER_INFO["work_authorized_us"],
    "work authorization": USER_INFO["work_authorized_us"],
    "eligible to work": USER_INFO["work_authorized_us"],
    "require sponsorship now": USER_INFO["require_sponsorship_now"],
    "need sponsorship": USER_INFO["require_sponsorship_now"],
    "currently require": USER_INFO["require_sponsorship_now"],
    "future sponsorship": USER_INFO["require_sponsorship_future"],
    "will you require": USER_INFO["require_sponsorship_future"],
    "h-1b": USER_INFO["require_sponsorship_future"],
    "h1b": USER_INFO["require_sponsorship_future"],
    "us citizen": USER_INFO["us_citizen"],
    "u.s. citizen": USER_INFO["us_citizen"],
    "permanent resident": "no",
    "green card": "no",
    "security clearance": USER_INFO["clearance_eligible"],

    # Technical Skills (Yes/No detection)
    "python": "yes",
    "java": "yes",
    "javascript": "yes",
    "sql": "yes",
    "c++": "yes",
    "react": "yes",
    "node": "yes",
    "aws": "yes",
    "docker": "yes",
    "git": "yes",
    "linux": "yes",
    "machine learning": "yes",
    "data analysis": "yes",
    "tensorflow": "yes",
    "pandas": "yes",
    "excel": "yes",
    "tableau": "yes",
    "agile": "yes",
    "scrum": "yes",

    # Generic positive responses
    "comfortable with": "yes",
    "experience with": "yes",
    "familiar with": "yes",
    "proficient in": "yes",
    "knowledge of": "yes",
    "ability to": "yes",
    "willing to": "yes",
    "agree to": "yes",
    "acknowledge": "yes",
    "confirm": "yes",
    "understand": "yes",
}

# ATS System Detection Patterns
ATS_PATTERNS = {
    "workday": ["workday.com", "myworkdayjobs.com", "wd1", "wd3", "wd5"],
    "greenhouse": ["greenhouse.io", "boards.greenhouse.io"],
    "lever": ["lever.co", "jobs.lever.co"],
    "icims": ["icims.com", "careers-"],
    "taleo": ["taleo.net", "taleo.com"],
    "bamboohr": ["bamboohr.com"],
    "jobvite": ["jobvite.com", "jobs.jobvite.com"],
    "smartrecruiters": ["smartrecruiters.com"],
    "ashby": ["ashbyhq.com"],
    "ultipro": ["ultipro.com"],
}

# Delay settings (in seconds) for anti-detection
MIN_DELAY = 1.0
MAX_DELAY = 3.0
PAGE_LOAD_DELAY = 3.0

class IndeedAutoApplier:
    def __init__(self):
        self.driver = None
        self.applied_jobs = self.load_applied_jobs()
        self.failed_jobs = self.load_failed_jobs()
        self.applications_today = 0
        self.skipped_jobs = 0
        self.errors_count = 0
        self.external_apps = 0  # Track external application attempts
        self.current_keyword_index = 0
        self.current_location_index = 0
        self.current_job_index = 0
        self.session_start_time = datetime.now()
        self.original_window = None  # Store original Indeed window handle

    # ==================== UTILITY METHODS ====================

    def log(self, message, level="INFO"):
        """Print timestamped log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def random_delay(self, min_sec=None, max_sec=None):
        """Add random delay for anti-detection"""
        min_sec = min_sec or MIN_DELAY
        max_sec = max_sec or MAX_DELAY
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def random_scroll(self):
        """Perform random scroll behavior"""
        if not self.is_browser_alive():
            return
        try:
            scroll_amount = random.randint(100, 400)
            direction = random.choice([1, -1])
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount * direction})")
            self.random_delay(0.3, 0.8)
        except Exception:
            pass

    # ==================== BROWSER HEALTH CHECKS ====================

    def is_browser_alive(self):
        """Check if browser window is still open and responsive"""
        if self.driver is None:
            return False
        try:
            # Try to access window handle - will fail if browser closed
            _ = self.driver.current_window_handle
            _ = self.driver.title
            return True
        except (NoSuchWindowException, WebDriverException):
            return False
        except Exception:
            return False

    def safe_browser_operation(self, operation, *args, error_msg="Browser operation failed", **kwargs):
        """Wrapper for safe browser operations with error handling"""
        if not self.is_browser_alive():
            self.log("Browser closed - cannot perform operation", "ERROR")
            return None
        try:
            return operation(*args, **kwargs)
        except StaleElementReferenceException:
            self.log(f"Element no longer exists: {error_msg}", "WARN")
            return None
        except NoSuchWindowException:
            self.log("Browser window was closed", "ERROR")
            return None
        except WebDriverException as e:
            self.log(f"Browser error: {str(e)[:50]}", "ERROR")
            return None
        except Exception as e:
            self.log(f"{error_msg}: {str(e)[:50]}", "WARN")
            return None

    # ==================== SESSION & STATE MANAGEMENT ====================

    def load_applied_jobs(self):
        """Load previously applied jobs to avoid duplicates"""
        if os.path.exists(APPLIED_JOBS_FILE):
            try:
                with open(APPLIED_JOBS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                self.log("Could not load applied jobs file, starting fresh", "WARN")
        return {}

    def load_session_state(self):
        """Load previous session state for recovery"""
        if os.path.exists(SESSION_STATE_FILE):
            try:
                with open(SESSION_STATE_FILE, 'r') as f:
                    state = json.load(f)
                    # Only restore if session is from today
                    if state.get("date") == datetime.now().strftime("%Y-%m-%d"):
                        self.current_keyword_index = state.get("keyword_index", 0)
                        self.current_location_index = state.get("location_index", 0)
                        self.applications_today = state.get("applications_today", 0)
                        self.log(f"Resumed session: {self.applications_today} apps already done today")
                        return True
            except (json.JSONDecodeError, IOError):
                pass
        return False

    def save_session_state(self):
        """Save current session state for recovery"""
        state = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "keyword_index": self.current_keyword_index,
            "location_index": self.current_location_index,
            "applications_today": self.applications_today,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(SESSION_STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
        except IOError:
            pass
    
    def save_applied_job(self, job_url, job_title, company):
        """Save applied job to tracking file"""
        self.applied_jobs[job_url] = {
            "title": job_title,
            "company": company,
            "applied_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(APPLIED_JOBS_FILE, 'w') as f:
                json.dump(self.applied_jobs, f, indent=2)
        except IOError as e:
            self.log(f"Could not save applied job: {e}", "WARN")

    def load_failed_jobs(self):
        """Load previously failed jobs for tracking"""
        if os.path.exists(FAILED_JOBS_FILE):
            try:
                with open(FAILED_JOBS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                self.log("Could not load failed jobs file, starting fresh", "WARN")
        return {}

    def save_failed_job(self, job_url, job_title, company, reason):
        """Save failed job to tracking file for manual follow-up"""
        self.failed_jobs[job_url] = {
            "title": job_title,
            "company": company,
            "reason": reason,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(FAILED_JOBS_FILE, 'w') as f:
                json.dump(self.failed_jobs, f, indent=2)
            self.log(f"Logged failed job for manual follow-up: {reason}")
        except IOError as e:
            self.log(f"Could not save failed job: {e}", "WARN")

    def setup_driver(self):
        """Initialize undetected Chrome driver"""
        self.log("Launching browser with anti-detection...")

        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        try:
            # Use undetected-chromedriver - automatically handles detection evasion
            self.driver = uc.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            self.log("Browser launched successfully!")
            return True
        except Exception as e:
            self.log(f"Failed to launch browser: {e}", "ERROR")
            return False

    def login_to_indeed(self):
        """
        Log in to Indeed account for external applications.
        Returns True if login successful or already logged in.
        """
        if not self.is_browser_alive():
            return False

        # Check if password is configured
        if not USER_INFO.get("indeed_password"):
            self.log("Indeed password not configured - external apps may require manual login", "WARN")
            return False

        try:
            self.log("Logging in to Indeed...")

            # Go to Indeed login page
            self.driver.get("https://secure.indeed.com/account/login")
            self.random_delay(2.0, 3.0)

            # Check if already logged in (redirects to homepage or shows account)
            if "secure.indeed.com" not in self.driver.current_url:
                self.log("Already logged in to Indeed!")
                return True

            # Find and fill email field
            email_field = None
            email_selectors = [
                "input[name='__email']",
                "input[type='email']",
                "input#ifl-InputFormField-3",
                "input[data-testid='login-email-input']",
            ]

            for selector in email_selectors:
                fields = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if fields:
                    email_field = fields[0]
                    break

            if not email_field:
                self.log("Could not find email field", "WARN")
                return False

            # Enter email
            email_field.clear()
            email_field.send_keys(USER_INFO["indeed_email"])
            self.random_delay(0.5, 1.0)

            # Find and click continue/next button
            continue_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'Continue') or contains(text(), 'Sign in') or contains(text(), 'Next')]")

            if continue_buttons:
                continue_buttons[0].click()
                self.random_delay(2.0, 3.0)

            # Find and fill password field
            password_field = None
            password_selectors = [
                "input[name='__password']",
                "input[type='password']",
                "input#ifl-InputFormField-7",
            ]

            for selector in password_selectors:
                fields = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if fields:
                    password_field = fields[0]
                    break

            if not password_field:
                self.log("Could not find password field - may need manual login", "WARN")
                return False

            # Enter password
            password_field.clear()
            password_field.send_keys(USER_INFO["indeed_password"])
            self.random_delay(0.5, 1.0)

            # Click sign in button
            signin_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'Sign in') or contains(text(), 'Log in') or @type='submit']")

            if signin_buttons:
                signin_buttons[0].click()
                self.random_delay(3.0, 5.0)

            # Check if login was successful
            if "secure.indeed.com" not in self.driver.current_url or "login" not in self.driver.current_url.lower():
                self.log("Successfully logged in to Indeed!")
                return True
            else:
                # Check for error messages
                errors = self.driver.find_elements(By.CSS_SELECTOR, "[class*='error'], [class*='alert']")
                if errors:
                    self.log(f"Login error: {errors[0].text[:50]}", "WARN")
                else:
                    self.log("Login may have failed - check browser", "WARN")
                return False

        except Exception as e:
            self.log(f"Login error: {str(e)[:40]}", "WARN")
            return False

    def check_if_logged_in(self):
        """Check if user is logged in to Indeed."""
        if not self.is_browser_alive():
            return False

        try:
            # Look for account/profile indicators
            account_indicators = self.driver.find_elements(By.CSS_SELECTOR,
                "[data-testid='account-menu'], [class*='account'], [class*='profile-icon']")

            return len(account_indicators) > 0

        except Exception:
            return False

    def search_jobs(self, keyword, location="Remote"):
        """Search for jobs on Indeed with optimal filters"""
        if not self.is_browser_alive():
            return False

        # Build search URL with filters for new grads and recent postings
        base_url = "https://www.indeed.com/jobs"
        params = {
            "q": keyword,
            "l": location,
            "fromage": "3",  # Past 3 days for freshest jobs
            "sort": "date",  # Sort by most recent
            "explvl": "entry_level",  # Entry level filter
        }

        # Build query string
        query_string = "&".join([f"{k}={v.replace(' ', '+')}" for k, v in params.items()])
        search_url = f"{base_url}?{query_string}"

        try:
            self.driver.get(search_url)
            self.random_delay(PAGE_LOAD_DELAY, PAGE_LOAD_DELAY + 1)
            self.random_scroll()
            print(f"\n{'='*70}")
            self.log(f"SEARCH: {keyword} | {location}")
            print(f"{'='*70}")
            return True
        except Exception as e:
            self.log(f"Search failed: {str(e)[:50]}", "ERROR")
            return False
    
    def get_job_listings(self):
        """Extract job listings from current page"""
        if not self.is_browser_alive():
            return []
        try:
            self.random_delay(1.5, 2.5)
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
            self.log(f"Found {len(job_cards)} jobs on this page")
            return job_cards[:15]
        except NoSuchWindowException:
            self.log("Browser closed while getting listings", "ERROR")
            return []
        except Exception as e:
            self.log(f"Error getting listings: {str(e)[:40]}", "WARN")
            return []
    
    def extract_job_details(self, job_card):
        """Extract details from a job card"""
        if not self.is_browser_alive():
            return None
        try:
            title = job_card.find_element(By.CSS_SELECTOR, "h2.jobTitle span").text
            company = job_card.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']").text
            location = job_card.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']").text

            # Try to get salary
            try:
                salary = job_card.find_element(By.CSS_SELECTOR, "div.salary-snippet").text
            except Exception:
                salary = "Not listed"

            # Get job link
            link_element = job_card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
            job_url = link_element.get_attribute("href").split('?')[0]  # Clean URL

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "url": job_url,
                "element": job_card
            }
        except StaleElementReferenceException:
            return None
        except NoSuchWindowException:
            return None
        except Exception:
            return None
    
    def display_job(self, job, job_num=0, total_jobs=0):
        """Display job details to user with progress info"""
        print(f"\n{'─'*70}")
        if total_jobs > 0:
            print(f"  JOB {job_num}/{total_jobs} | Apps today: {self.applications_today}/{MAX_APPLICATIONS_PER_SESSION}")
        print(f"{'─'*70}")
        print(f"  Title:    {job['title']}")
        print(f"  Company:  {job['company']}")
        print(f"  Location: {job['location']}")
        print(f"  Salary:   {job['salary']}")
        print(f"{'─'*70}")
    
    def click_job(self, job):
        """Click on job to open details"""
        if not self.is_browser_alive():
            return False
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", job['element'])
            self.random_delay(0.5, 1.0)
            job['element'].click()
            self.random_delay(2.0, 3.5)
            return True
        except StaleElementReferenceException:
            self.log("Job element expired, skipping", "WARN")
            return False
        except NoSuchWindowException:
            self.log("Browser closed", "ERROR")
            return False
        except Exception as e:
            self.log(f"Click error: {str(e)[:40]}", "WARN")
            return False
    
    def detect_application_type(self):
        """
        Detect the type of application available for this job.
        Returns: "easy_apply", "external", or "none"
        """
        if not self.is_browser_alive():
            return "none"
        try:
            # Strategy 1: Check for Indeed Easy Apply wrapper (most reliable)
            indeed_apply_wrapper = self.driver.find_elements(By.CSS_SELECTOR,
                ".ia-IndeedApplyButton, [class*='IndeedApply'], [data-testid*='indeedApply']")

            if indeed_apply_wrapper:
                self.log("Indeed Easy Apply available")
                return "easy_apply"

            # Strategy 2: Find buttons by text content (use .text property, not XPath text())
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in all_buttons:
                btn_text = btn.text.lower().strip()
                if btn_text in ["apply now", "easily apply", "apply"]:
                    # Check if it's NOT an external link (no target="_blank")
                    target = btn.get_attribute("target") or ""
                    onclick = btn.get_attribute("onclick") or ""
                    href = btn.get_attribute("href") or ""

                    # If it has target="_blank" or opens external URL, it's external
                    if "_blank" in target or "window.open" in onclick:
                        self.log("External application detected (button opens new tab)")
                        return "external"

                    # Check if button is inside an anchor that goes external
                    try:
                        parent_anchor = btn.find_element(By.XPATH, "./ancestor::a")
                        if parent_anchor:
                            anchor_href = parent_anchor.get_attribute("href") or ""
                            if "indeed.com" not in anchor_href and anchor_href.startswith("http"):
                                self.log("External application detected (parent link)")
                                return "external"
                    except Exception:
                        pass

                    self.log("Easy Apply available")
                    return "easy_apply"

            # Strategy 3: Check for "Apply on company site" (external)
            external_indicators = self.driver.find_elements(By.XPATH,
                "//*[contains(text(), 'Apply on company') or contains(text(), 'company site')]")

            if external_indicators:
                self.log("External application detected (company site)")
                return "external"

            # Strategy 4: Check for external apply links
            apply_links = self.driver.find_elements(By.CSS_SELECTOR,
                "a[href*='apply'], a[href*='career']")

            for link in apply_links:
                link_text = link.text.lower()
                link_href = link.get_attribute("href") or ""
                if "apply" in link_text and "indeed.com" not in link_href:
                    self.log("External application link found")
                    return "external"

            self.log("No application method found")
            return "none"

        except NoSuchWindowException:
            return "none"
        except Exception as e:
            self.log(f"Error detecting application type: {str(e)[:30]}", "WARN")
            return "none"

    # ==================== WINDOW MANAGEMENT ====================

    def switch_to_new_window(self, timeout=10):
        """
        Switch to newly opened window/tab.
        Returns True if successful, False otherwise.
        """
        if not self.is_browser_alive():
            return False

        try:
            current_handle = self.driver.current_window_handle
            all_handles = self.driver.window_handles

            # If there's already more than one window, switch to the newest one
            if len(all_handles) > 1:
                # Find a window that's not the current one
                for handle in all_handles:
                    if handle != current_handle and handle != self.original_window:
                        self.driver.switch_to.window(handle)
                        self.random_delay(2.0, 3.0)  # Wait for page to load
                        self.log(f"Switched to new window: {self.driver.current_url[:50]}...")
                        return True

                # If no different window found, try switching to any other window
                for handle in all_handles:
                    if handle != current_handle:
                        self.driver.switch_to.window(handle)
                        self.random_delay(2.0, 3.0)
                        self.log(f"Switched to window: {self.driver.current_url[:50]}...")
                        return True

            # Wait for new window to appear
            start_time = time.time()
            while time.time() - start_time < timeout:
                current_handles = set(self.driver.window_handles)

                if len(current_handles) > 1:
                    for handle in current_handles:
                        if handle != current_handle and handle != self.original_window:
                            self.driver.switch_to.window(handle)
                            self.random_delay(2.0, 3.0)
                            self.log(f"Switched to new window: {self.driver.current_url[:50]}...")
                            return True

                time.sleep(0.5)

            self.log("No new window opened", "WARN")
            return False

        except NoSuchWindowException:
            self.log("Window was closed", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error switching windows: {str(e)[:30]}", "WARN")
            return False

    def return_to_indeed(self):
        """
        Close current external tab and return to original Indeed window.
        """
        if not self.is_browser_alive():
            return False

        try:
            # Close current window if it's not the original
            current_window = self.driver.current_window_handle
            if self.original_window and current_window != self.original_window:
                self.driver.close()
                self.driver.switch_to.window(self.original_window)
                self.log("Returned to Indeed")
                self.random_delay(1.0, 2.0)
                return True
            return True  # Already on original window

        except NoSuchWindowException:
            # Try to switch to any remaining window
            try:
                remaining_windows = self.driver.window_handles
                if remaining_windows:
                    self.driver.switch_to.window(remaining_windows[0])
                    self.original_window = remaining_windows[0]
                    return True
            except Exception:
                pass
            return False
        except Exception as e:
            self.log(f"Error returning to Indeed: {str(e)[:30]}", "WARN")
            return False

    def detect_captcha(self):
        """Detect if a captcha is present on the page."""
        if not self.is_browser_alive():
            return False

        try:
            captcha_indicators = [
                "//iframe[contains(@src, 'recaptcha')]",
                "//iframe[contains(@src, 'captcha')]",
                "//div[contains(@class, 'captcha')]",
                "//div[contains(@class, 'recaptcha')]",
                "//*[contains(@id, 'captcha')]",
                "//img[contains(@alt, 'captcha')]",
                "//*[contains(text(), 'verify you are human')]",
                "//*[contains(text(), 'not a robot')]",
            ]

            for xpath in captcha_indicators:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    self.log("CAPTCHA detected!")
                    return True

            return False

        except Exception:
            return False

    # ==================== ATS DETECTION ====================

    def detect_ats_system(self):
        """
        Detect which Applicant Tracking System (ATS) the external site uses.
        Returns: ATS name string or "unknown"
        """
        if not self.is_browser_alive():
            return "unknown"

        try:
            current_url = self.driver.current_url.lower()
            page_source = self.driver.page_source.lower()

            # Check URL patterns
            for ats_name, patterns in ATS_PATTERNS.items():
                for pattern in patterns:
                    if pattern in current_url:
                        self.log(f"Detected ATS: {ats_name.upper()}")
                        return ats_name

            # Check page source for ATS indicators
            if "workday" in page_source or "workdaycdn" in page_source:
                return "workday"
            if "greenhouse" in page_source:
                return "greenhouse"
            if "lever" in page_source:
                return "lever"
            if "icims" in page_source:
                return "icims"
            if "taleo" in page_source:
                return "taleo"
            if "bamboohr" in page_source:
                return "bamboohr"
            if "jobvite" in page_source:
                return "jobvite"
            if "smartrecruiters" in page_source:
                return "smartrecruiters"

            return "unknown"

        except Exception as e:
            self.log(f"Error detecting ATS: {str(e)[:30]}", "WARN")
            return "unknown"

    # ==================== ACCOUNT HANDLING ====================

    def handle_account_requirement(self):
        """
        Handle account creation/login requirements on external sites.
        Strategy: LinkedIn Sign-In > Google Sign-In > Create Account
        Returns: True if handled successfully, False otherwise
        """
        if not self.is_browser_alive():
            return False

        try:
            self.random_delay(1.5, 2.5)

            # Strategy 1: Try LinkedIn Sign-In
            linkedin_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'LinkedIn') or contains(@aria-label, 'LinkedIn')]" +
                " | //a[contains(@href, 'linkedin') and contains(text(), 'Sign')]" +
                " | //button[contains(@class, 'linkedin')]" +
                " | //*[contains(@id, 'linkedin') and (contains(text(), 'Sign') or contains(text(), 'Apply'))]")

            if linkedin_buttons:
                try:
                    linkedin_buttons[0].click()
                    self.log("Clicked LinkedIn Sign-In")
                    self.random_delay(3.0, 5.0)
                    # Check if we're now on LinkedIn auth page
                    if "linkedin.com" in self.driver.current_url:
                        self.log("LinkedIn auth page - may need manual login")
                        return True
                except Exception:
                    pass

            # Strategy 2: Try Google Sign-In
            google_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'Google') or contains(@aria-label, 'Google')]" +
                " | //a[contains(@href, 'google') and contains(text(), 'Sign')]" +
                " | //button[contains(@class, 'google')]" +
                " | //*[contains(@id, 'google') and contains(text(), 'Sign')]")

            if google_buttons:
                try:
                    google_buttons[0].click()
                    self.log("Clicked Google Sign-In")
                    self.random_delay(3.0, 5.0)
                    return True
                except Exception:
                    pass

            # Strategy 3: Create new account
            return self.create_account_on_site()

        except Exception as e:
            self.log(f"Error handling account: {str(e)[:30]}", "WARN")
            return False

    def create_account_on_site(self):
        """
        Create a new account on the career site using email + password.
        Returns: True if account created or login successful, False otherwise
        """
        if not self.is_browser_alive():
            return False

        try:
            # Look for registration/sign up forms
            signup_buttons = self.driver.find_elements(By.XPATH,
                "//a[contains(text(), 'Create') or contains(text(), 'Sign up') or contains(text(), 'Register')]" +
                " | //button[contains(text(), 'Create') or contains(text(), 'Sign up') or contains(text(), 'Register')]")

            if signup_buttons:
                try:
                    signup_buttons[0].click()
                    self.random_delay(2.0, 3.0)
                except Exception:
                    pass

            # Fill registration form fields
            self.smart_fill_form()

            # Look for password field specifically
            password_fields = self.driver.find_elements(By.CSS_SELECTOR,
                "input[type='password']")

            for pwd_field in password_fields:
                try:
                    pwd_field.clear()
                    pwd_field.send_keys(USER_INFO["job_app_password"])
                    self.random_delay(0.3, 0.6)
                except Exception:
                    continue

            # Confirm password field (if exists)
            confirm_pwd = self.driver.find_elements(By.XPATH,
                "//input[@type='password' and (contains(@name, 'confirm') or contains(@id, 'confirm') or contains(@name, 'verify'))]")

            if confirm_pwd:
                try:
                    confirm_pwd[0].clear()
                    confirm_pwd[0].send_keys(USER_INFO["job_app_password"])
                except Exception:
                    pass

            # Click create/submit button
            submit_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'Create') or contains(text(), 'Submit') or contains(text(), 'Sign up') or contains(text(), 'Register')]" +
                " | //input[@type='submit']")

            if submit_buttons:
                try:
                    submit_buttons[0].click()
                    self.log("Account creation attempted")
                    self.random_delay(3.0, 5.0)
                    return True
                except Exception:
                    pass

            return True  # Continue anyway, form might not need account

        except Exception as e:
            self.log(f"Error creating account: {str(e)[:30]}", "WARN")
            return False

    def fill_text_field(self, field, value):
        """Helper to fill a text field with human-like typing"""
        try:
            field.clear()
            field.send_keys(value)
            self.random_delay(0.2, 0.5)
        except StaleElementReferenceException:
            pass
        except Exception:
            pass

    # ==================== SMART UNIVERSAL FORM FILLER ====================

    def smart_fill_form(self):
        """
        Universal intelligent form filler that can handle ANY form structure.
        Uses multiple detection strategies to identify and fill fields.
        """
        if not self.is_browser_alive():
            return False

        try:
            self.random_delay(1.0, 2.0)

            # Find all visible input fields
            inputs = self.driver.find_elements(By.CSS_SELECTOR,
                "input:not([type='hidden']):not([type='submit']):not([type='button']):not([type='checkbox']):not([type='radio']), " +
                "textarea, select")

            for field in inputs:
                try:
                    # Skip if field is not visible or already filled
                    if not field.is_displayed():
                        continue

                    current_value = field.get_attribute("value") or ""
                    if len(current_value) > 2:  # Already has content
                        continue

                    # Gather all field identification information
                    field_info = self.get_field_identification(field)

                    # Determine the appropriate value
                    value = self.match_field_to_value(field_info)

                    if value:
                        if field.tag_name == "select":
                            self.smart_select_option(field, value)
                        else:
                            self.fill_text_field(field, value)

                except StaleElementReferenceException:
                    continue
                except Exception:
                    continue

            # Handle radio buttons and checkboxes
            self.smart_answer_questions()

            # Handle file uploads (resume)
            self.upload_resume()

            return True

        except Exception as e:
            self.log(f"Smart fill error: {str(e)[:30]}", "WARN")
            return False

    def get_field_identification(self, field):
        """
        Gather all possible identification information for a field.
        Returns a combined string of all identifiers for matching.
        """
        try:
            identifiers = []

            # Basic attributes
            identifiers.append(field.get_attribute("name") or "")
            identifiers.append(field.get_attribute("id") or "")
            identifiers.append(field.get_attribute("placeholder") or "")
            identifiers.append(field.get_attribute("aria-label") or "")
            identifiers.append(field.get_attribute("aria-describedby") or "")
            identifiers.append(field.get_attribute("data-testid") or "")
            identifiers.append(field.get_attribute("autocomplete") or "")

            # Get associated label
            field_id = field.get_attribute("id")
            if field_id:
                try:
                    labels = self.driver.find_elements(By.CSS_SELECTOR, f"label[for='{field_id}']")
                    if labels:
                        identifiers.append(labels[0].text)
                except Exception:
                    pass

            # Check parent containers for text
            try:
                parent = field.find_element(By.XPATH, "./..")
                if parent:
                    parent_text = parent.text[:100] if parent.text else ""
                    identifiers.append(parent_text)

                    # Check grandparent too
                    grandparent = parent.find_element(By.XPATH, "./..")
                    if grandparent:
                        gp_text = grandparent.text[:100] if grandparent.text else ""
                        identifiers.append(gp_text)
            except Exception:
                pass

            # Combine and lowercase all identifiers
            combined = " ".join(identifiers).lower()
            return combined

        except Exception:
            return ""

    def match_field_to_value(self, field_info):
        """
        Match field identification to appropriate USER_INFO value.
        Returns the value to fill, or None if no match.
        """
        if not field_info:
            return None

        # Skip cover letter fields entirely
        if any(kw in field_info for kw in ["cover letter", "cover_letter", "coverletter", "motivation"]):
            return None  # Skip - no cover letter

        # Email
        if any(kw in field_info for kw in ["email", "e-mail", "e_mail"]):
            return USER_INFO["email"]

        # Phone
        if any(kw in field_info for kw in ["phone", "mobile", "telephone", "tel", "cell"]):
            return USER_INFO["phone"]

        # First name (check before generic "name")
        if ("first" in field_info or "fname" in field_info or "given" in field_info) and "name" in field_info:
            return USER_INFO["first_name"]

        # Last name
        if ("last" in field_info or "lname" in field_info or "surname" in field_info or "family" in field_info) and "name" in field_info:
            return USER_INFO["last_name"]

        # Full name (generic "name" field)
        if "name" in field_info and "first" not in field_info and "last" not in field_info and "company" not in field_info:
            return USER_INFO["full_name"]

        # Address
        if any(kw in field_info for kw in ["address", "street", "address1", "address_1"]):
            if "address2" in field_info or "address_2" in field_info or "apt" in field_info:
                return ""  # Leave secondary address empty
            return USER_INFO["address"]

        # City
        if any(kw in field_info for kw in ["city", "town", "municipality"]):
            return USER_INFO["city"]

        # State
        if any(kw in field_info for kw in ["state", "province", "region"]) and "country" not in field_info:
            return USER_INFO["state"]

        # Zip/Postal code
        if any(kw in field_info for kw in ["zip", "postal", "postcode"]):
            return USER_INFO["zip_code"]

        # Country
        if "country" in field_info:
            return USER_INFO["country"]

        # LinkedIn
        if any(kw in field_info for kw in ["linkedin", "linked in", "linked_in"]):
            return USER_INFO["linkedin"]

        # Portfolio/Website
        if any(kw in field_info for kw in ["portfolio", "website", "personal site", "personal_site", "url", "homepage"]):
            if "linkedin" not in field_info and "github" not in field_info:
                return USER_INFO["portfolio"]

        # GitHub
        if any(kw in field_info for kw in ["github", "git hub", "git_hub"]):
            return USER_INFO["github"]

        # University/School
        if any(kw in field_info for kw in ["university", "college", "school", "institution"]):
            return USER_INFO["university"]

        # Degree
        if any(kw in field_info for kw in ["degree", "qualification"]):
            return f"{USER_INFO['degree']} in {USER_INFO['major']}"

        # Major/Field of study
        if any(kw in field_info for kw in ["major", "field of study", "specialization", "concentration"]):
            return USER_INFO["major"]

        # GPA
        if any(kw in field_info for kw in ["gpa", "grade point", "grades"]):
            return USER_INFO["gpa"]

        # Graduation date/year
        if any(kw in field_info for kw in ["graduation", "grad date", "grad year", "expected graduation"]):
            return f"{USER_INFO['graduation_month']} {USER_INFO['graduation_year']}"

        # Salary
        if any(kw in field_info for kw in ["salary", "compensation", "expected pay", "desired pay", "pay expectation"]):
            return USER_INFO["salary_expectation"]

        # Years of experience
        if any(kw in field_info for kw in ["years of experience", "years experience", "yoe", "experience years"]):
            return USER_INFO["years_experience"]

        # Current title
        if any(kw in field_info for kw in ["current title", "job title", "position", "current position"]):
            return USER_INFO["current_title"]

        # Current company
        if any(kw in field_info for kw in ["current company", "current employer", "employer"]):
            return USER_INFO["current_company"]

        # Start date
        if any(kw in field_info for kw in ["start date", "available date", "when can you start", "earliest start"]):
            return USER_INFO["start_date"]

        # Notice period
        if any(kw in field_info for kw in ["notice period", "notice required"]):
            return USER_INFO["notice_period"]

        return None

    def smart_select_option(self, select_element, value):
        """Smart selection from dropdown menus."""
        try:
            select = Select(select_element)

            # Try exact match first
            try:
                select.select_by_visible_text(value)
                return True
            except Exception:
                pass

            # Try partial match
            options = select.options
            value_lower = value.lower()

            for option in options:
                option_text = option.text.lower()
                if value_lower in option_text or option_text in value_lower:
                    try:
                        select.select_by_visible_text(option.text)
                        return True
                    except Exception:
                        continue

            # Try by value attribute
            try:
                select.select_by_value(value)
                return True
            except Exception:
                pass

            return False

        except Exception:
            return False

    def smart_answer_questions(self):
        """
        Intelligently answer screening questions (radio buttons, checkboxes).
        Uses the QUESTION_ANSWERS database for matching.
        """
        if not self.is_browser_alive():
            return

        try:
            # Find all question containers (fieldsets, divs with radio/checkbox groups)
            question_containers = self.driver.find_elements(By.XPATH,
                "//fieldset | //div[.//input[@type='radio' or @type='checkbox']]")

            for container in question_containers:
                try:
                    container_text = container.text.lower()

                    # Find answer from QUESTION_ANSWERS database
                    answer = self.answer_question_intelligently(container_text)

                    if answer:
                        # Find the appropriate radio/checkbox to click
                        inputs = container.find_elements(By.CSS_SELECTOR,
                            "input[type='radio'], input[type='checkbox']")

                        for inp in inputs:
                            try:
                                # Get input value and label
                                inp_value = (inp.get_attribute("value") or "").lower()
                                inp_label = self.get_field_label(inp).lower()

                                answer_lower = str(answer).lower()

                                # Check if this input matches our answer
                                if (answer_lower in inp_value or
                                    answer_lower in inp_label or
                                    inp_value in answer_lower or
                                    (answer_lower == "yes" and inp_value in ["yes", "true", "1", "y"]) or
                                    (answer_lower == "no" and inp_value in ["no", "false", "0", "n"])):

                                    if not inp.is_selected():
                                        inp.click()
                                        self.random_delay(0.2, 0.4)
                                    break
                            except Exception:
                                continue

                except Exception:
                    continue

        except Exception as e:
            self.log(f"Error answering questions: {str(e)[:30]}", "WARN")

    def answer_question_intelligently(self, question_text):
        """
        Parse a question and find the appropriate answer from QUESTION_ANSWERS.
        Returns the answer string or None.
        """
        if not question_text:
            return None

        question_lower = question_text.lower()

        # Check each keyword in QUESTION_ANSWERS
        for keyword, answer in QUESTION_ANSWERS.items():
            if keyword in question_lower:
                return answer

        # Special handling for work authorization questions (F-1 OPT specific)
        if "authorized to work" in question_lower or "legally authorized" in question_lower:
            return "yes"
        if "sponsorship" in question_lower and "now" in question_lower:
            return "no"  # No sponsorship needed NOW (on OPT)
        if "sponsorship" in question_lower and ("future" in question_lower or "will you" in question_lower):
            return "yes"  # Will need H-1B in future

        # Default positive for generic questions about skills/abilities
        if any(kw in question_lower for kw in ["able to", "willing to", "comfortable", "familiar", "experience with"]):
            return "yes"

        return None

    # ==================== ATS-SPECIFIC HANDLERS ====================

    def fill_workday_form(self):
        """Handle Workday-specific form structures."""
        if not self.is_browser_alive():
            return False

        try:
            self.log("Filling Workday application...")
            self.random_delay(2.0, 3.0)

            # Workday often has multi-step wizards
            # Look for "Apply" or "Apply Manually" button first
            apply_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'Apply') or contains(@data-automation-id, 'apply')]")

            if apply_buttons:
                try:
                    apply_buttons[0].click()
                    self.random_delay(2.0, 3.0)
                except Exception:
                    pass

            # Use LinkedIn if available (Workday supports this)
            linkedin_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'LinkedIn') or contains(@data-automation-id, 'linkedin')]")

            if linkedin_buttons:
                try:
                    linkedin_buttons[0].click()
                    self.log("Using LinkedIn for Workday")
                    self.random_delay(3.0, 5.0)
                    return True
                except Exception:
                    pass

            # Fill form using smart_fill_form
            self.smart_fill_form()

            # Complete multi-step if needed
            return self.complete_multi_step_application()

        except Exception as e:
            self.log(f"Workday fill error: {str(e)[:30]}", "WARN")
            return False

    def fill_greenhouse_form(self):
        """Handle Greenhouse-specific form structures."""
        if not self.is_browser_alive():
            return False

        try:
            self.log("Filling Greenhouse application...")
            self.random_delay(1.5, 2.5)

            # Greenhouse forms are typically single-page
            self.smart_fill_form()

            # Upload resume (Greenhouse usually has a clear upload button)
            self.upload_resume()

            # Fill any custom questions
            self.smart_answer_questions()

            return True

        except Exception as e:
            self.log(f"Greenhouse fill error: {str(e)[:30]}", "WARN")
            return False

    def fill_lever_form(self):
        """Handle Lever-specific form structures."""
        if not self.is_browser_alive():
            return False

        try:
            self.log("Filling Lever application...")
            self.random_delay(1.5, 2.5)

            # Lever typically has a simple apply button
            apply_buttons = self.driver.find_elements(By.XPATH,
                "//a[contains(text(), 'Apply') or contains(@class, 'apply')]")

            if apply_buttons:
                try:
                    apply_buttons[0].click()
                    self.random_delay(2.0, 3.0)
                except Exception:
                    pass

            # Fill the form
            self.smart_fill_form()

            return True

        except Exception as e:
            self.log(f"Lever fill error: {str(e)[:30]}", "WARN")
            return False

    def fill_icims_form(self):
        """Handle iCIMS-specific form structures."""
        if not self.is_browser_alive():
            return False

        try:
            self.log("Filling iCIMS application...")
            self.random_delay(1.5, 2.5)

            # iCIMS often requires account creation
            self.handle_account_requirement()

            # Fill form
            self.smart_fill_form()

            # Multi-step navigation
            return self.complete_multi_step_application()

        except Exception as e:
            self.log(f"iCIMS fill error: {str(e)[:30]}", "WARN")
            return False

    def fill_generic_ats_form(self):
        """Handle any unknown ATS with generic form filling."""
        if not self.is_browser_alive():
            return False

        try:
            self.log("Filling generic application form...")
            self.random_delay(1.5, 2.5)

            # Try account handling first (many sites require login)
            self.handle_account_requirement()

            # Use smart form filler
            self.smart_fill_form()

            # Complete multi-step if applicable
            return self.complete_multi_step_application()

        except Exception as e:
            self.log(f"Generic form fill error: {str(e)[:30]}", "WARN")
            return False

    # ==================== MULTI-STEP APPLICATION HANDLER ====================

    def complete_multi_step_application(self, max_steps=10):
        """
        Navigate through multi-page application forms.
        Fills each page and clicks Next/Continue until Submit.
        """
        if not self.is_browser_alive():
            return False

        try:
            for step in range(max_steps):
                self.log(f"Processing application step {step + 1}...")
                self.random_delay(1.5, 2.5)

                # Check for captcha
                if self.detect_captcha():
                    self.log("CAPTCHA detected - cannot complete automatically")
                    return False

                # Fill current page
                self.smart_fill_form()

                # Look for navigation button
                nav_button = self.find_navigation_button()

                if nav_button is None:
                    self.log("No navigation button found - may be final step")
                    return True

                button_text = nav_button.text.lower()

                # Check if it's the final submit
                if any(kw in button_text for kw in ["submit", "apply", "send", "finish", "complete"]):
                    try:
                        nav_button.click()
                        self.log("Clicked SUBMIT button")
                        self.random_delay(3.0, 5.0)

                        # Check for success
                        if self.check_application_success():
                            return True
                        return True  # Assume success if no error
                    except Exception as e:
                        self.log(f"Submit click error: {str(e)[:30]}", "WARN")
                        return False

                # Click Next/Continue
                try:
                    nav_button.click()
                    self.log(f"Clicked: {button_text}")
                    self.random_delay(2.0, 3.5)
                except Exception as e:
                    self.log(f"Navigation click error: {str(e)[:30]}", "WARN")
                    break

            return True

        except Exception as e:
            self.log(f"Multi-step error: {str(e)[:30]}", "WARN")
            return False

    def find_navigation_button(self):
        """
        Find the Next, Continue, or Submit button on the current page.
        Returns the button element or None.
        """
        if not self.is_browser_alive():
            return None

        try:
            # Words to exclude (not navigation buttons)
            exclude_words = ['search', 'filter', 'clear', 'reset', 'cancel', 'back', 'close', 'skip']

            # Strategy 1: Find buttons by exact/partial text match
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            all_buttons.extend(self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit']"))

            # Priority keywords for navigation
            priority_keywords = ['submit', 'apply', 'complete', 'finish', 'continue', 'next', 'save', 'send']

            for keyword in priority_keywords:
                for btn in all_buttons:
                    try:
                        btn_text = btn.text.lower().strip()
                        btn_value = (btn.get_attribute('value') or '').lower()
                        btn_combined = f"{btn_text} {btn_value}"

                        # Skip excluded buttons
                        if any(excl in btn_combined for excl in exclude_words):
                            continue

                        # Match priority keyword
                        if keyword in btn_combined:
                            if btn.is_displayed() and btn.is_enabled():
                                return btn
                    except Exception:
                        continue

            # Strategy 2: Look for submit buttons by type attribute (but filter out search)
            submit_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                "button[type='submit'], input[type='submit']")

            for btn in submit_buttons:
                try:
                    btn_text = btn.text.lower().strip()
                    btn_value = (btn.get_attribute('value') or '').lower()
                    btn_combined = f"{btn_text} {btn_value}"

                    # Skip excluded buttons
                    if any(excl in btn_combined for excl in exclude_words):
                        continue

                    if btn.is_displayed() and btn.is_enabled():
                        return btn
                except Exception:
                    continue

            return None

        except Exception:
            return None

    def check_application_success(self):
        """Check if application was successfully submitted."""
        if not self.is_browser_alive():
            return False

        try:
            success_indicators = [
                "application submitted",
                "successfully applied",
                "thank you for applying",
                "application received",
                "application complete",
                "thanks for your interest",
                "we have received your application",
                "your application has been submitted",
            ]

            page_text = self.driver.page_source.lower()

            for indicator in success_indicators:
                if indicator in page_text:
                    self.log("SUCCESS: Application submitted!")
                    return True

            return False

        except Exception:
            return False

    # ==================== EXTERNAL APPLICATION HANDLER ====================

    def handle_external_application(self, job):
        """
        Handle applications that redirect to external company sites.
        Opens new tab, navigates ATS, fills forms, and returns.
        """
        if not self.is_browser_alive():
            return False

        try:
            self.log(f"Handling external application for: {job['company']}")

            # Find the external apply button using multiple strategies
            apply_button = None

            # Strategy 1: Find button by text content (most reliable)
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in all_buttons:
                btn_text = btn.text.lower().strip()
                if "apply" in btn_text and ("company" in btn_text or "site" in btn_text or btn_text == "apply"):
                    apply_button = btn
                    self.log(f"Found external apply button: '{btn.text.strip()}'")
                    break

            # Strategy 2: Find any button/link containing "Apply"
            if not apply_button:
                for btn in all_buttons:
                    btn_text = btn.text.lower().strip()
                    if btn_text in ["apply", "apply now", "apply on company site"]:
                        apply_button = btn
                        break

            # Strategy 3: Find apply links
            if not apply_button:
                apply_links = self.driver.find_elements(By.CSS_SELECTOR,
                    "a[href*='apply'], a[href*='career'], a[href*='jobs']")
                for link in apply_links:
                    if "apply" in link.text.lower():
                        apply_button = link
                        break

            if not apply_button:
                self.log("No external apply button found", "WARN")
                self.save_failed_job(job['url'], job['title'], job['company'], "No apply button")
                return False

            # Track windows before click
            windows_before = set(self.driver.window_handles)

            # Click the button using JavaScript (regular click often doesn't work)
            try:
                self.driver.execute_script('arguments[0].click();', apply_button)
                self.random_delay(2.0, 3.5)
                self.log("Clicked external apply button (JS)")
            except Exception as e:
                # Fallback to regular click
                try:
                    apply_button.click()
                    self.random_delay(2.0, 3.5)
                    self.log("Clicked external apply button")
                except Exception as e2:
                    self.log(f"Click failed: {str(e2)[:30]}", "WARN")
                    return False

            # Check for new window
            windows_after = set(self.driver.window_handles)
            new_windows = windows_after - windows_before

            # Switch to new window (directly if we know which one)
            if new_windows:
                new_win = new_windows.pop()
                self.driver.switch_to.window(new_win)
                self.random_delay(2.0, 3.0)
                self.log(f"Switched to external window: {self.driver.current_url[:50]}...")
            elif not self.switch_to_new_window():
                self.log("Failed to switch to new window", "WARN")
                self.save_failed_job(job['url'], job['title'], job['company'], "No new window opened")
                return False

            # Check if Indeed sign-in page appeared (common for external apps)
            if "secure.indeed.com" in self.driver.current_url or "Sign In" in self.driver.title:
                self.log("Indeed sign-in required for external application")
                self.save_failed_job(job['url'], job['title'], job['company'],
                    "Requires Indeed sign-in - log in manually then retry")
                self.return_to_indeed()
                return False

            # Check for captcha
            if self.detect_captcha():
                self.save_failed_job(job['url'], job['title'], job['company'], "Captcha detected")
                self.return_to_indeed()
                return False

            # Detect ATS type
            ats_type = self.detect_ats_system()
            self.log(f"Detected ATS: {ats_type}")

            # Fill based on ATS type
            success = False
            if ats_type == "workday":
                success = self.fill_workday_form()
            elif ats_type == "greenhouse":
                success = self.fill_greenhouse_form()
            elif ats_type == "lever":
                success = self.fill_lever_form()
            elif ats_type == "icims":
                success = self.fill_icims_form()
            else:
                success = self.fill_generic_ats_form()

            # Check for success
            if success and self.check_application_success():
                self.log(f"External application completed for {job['company']}")
                self.external_apps += 1
            else:
                # Log as needing manual follow-up
                self.save_failed_job(job['url'], job['title'], job['company'],
                    f"External app ({ats_type}) - may need manual completion")

            # Return to Indeed
            self.return_to_indeed()

            return success

        except Exception as e:
            self.log(f"External application error: {str(e)[:30]}", "WARN")
            self.return_to_indeed()
            return False

    def fill_application_form(self):
        """Fill out the application form intelligently"""
        if not self.is_browser_alive():
            return False
        try:
            self.random_delay(1.5, 2.5)
            
            # Find all input fields
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], input[type='tel'], textarea")
            
            for inp in inputs:
                try:
                    field_name = (inp.get_attribute("name") or "").lower()
                    field_id = (inp.get_attribute("id") or "").lower()
                    field_label = self.get_field_label(inp).lower()
                    
                    # Combine all identifiers
                    field_info = f"{field_name} {field_id} {field_label}"
                    
                    # Fill based on field type
                    if any(keyword in field_info for keyword in ["email", "e-mail"]):
                        self.fill_text_field(inp, USER_INFO["email"])
                    
                    elif any(keyword in field_info for keyword in ["phone", "mobile", "telephone"]):
                        self.fill_text_field(inp, USER_INFO["phone"])
                    
                    elif any(keyword in field_info for keyword in ["first", "fname", "given"]) and "name" in field_info:
                        self.fill_text_field(inp, USER_INFO["first_name"])
                    
                    elif any(keyword in field_info for keyword in ["last", "lname", "surname", "family"]) and "name" in field_info:
                        self.fill_text_field(inp, USER_INFO["last_name"])
                    
                    elif "name" in field_info and "first" not in field_info and "last" not in field_info:
                        self.fill_text_field(inp, USER_INFO["full_name"])
                    
                    elif any(keyword in field_info for keyword in ["city", "town"]):
                        self.fill_text_field(inp, USER_INFO["city"])
                    
                    elif any(keyword in field_info for keyword in ["state", "province"]):
                        self.fill_text_field(inp, USER_INFO["state"])
                    
                    elif any(keyword in field_info for keyword in ["zip", "postal"]):
                        self.fill_text_field(inp, USER_INFO["zip_code"])
                    
                    elif any(keyword in field_info for keyword in ["address", "street"]):
                        self.fill_text_field(inp, USER_INFO["address"])
                    
                    elif any(keyword in field_info for keyword in ["linkedin", "linked in"]):
                        self.fill_text_field(inp, USER_INFO["linkedin"])
                    
                    elif any(keyword in field_info for keyword in ["portfolio", "website", "personal site"]):
                        self.fill_text_field(inp, USER_INFO["portfolio"])
                    
                    elif any(keyword in field_info for keyword in ["github", "git hub"]):
                        self.fill_text_field(inp, USER_INFO["github"])
                    
                    elif any(keyword in field_info for keyword in ["gpa", "grade"]):
                        self.fill_text_field(inp, USER_INFO["gpa"])
                    
                    elif any(keyword in field_info for keyword in ["university", "college", "school"]):
                        self.fill_text_field(inp, USER_INFO["university"])
                    
                    elif any(keyword in field_info for keyword in ["degree", "education"]):
                        self.fill_text_field(inp, f"{USER_INFO['degree']} in {USER_INFO['major']}")
                    
                    elif any(keyword in field_info for keyword in ["salary", "compensation", "expected pay"]):
                        self.fill_text_field(inp, USER_INFO["salary_expectation"])
                    
                    elif any(keyword in field_info for keyword in ["experience", "years"]):
                        self.fill_text_field(inp, USER_INFO["years_experience"])
                
                except:
                    continue
            
            # Handle file upload (resume)
            self.upload_resume()
            
            # Handle dropdowns (select fields)
            self.fill_dropdowns()
            
            # Handle radio buttons and checkboxes
            self.answer_screening_questions()
            
            return True
            
        except Exception as e:
            print(f"⚠️ Form filling error: {e}")
            return False
    
    def get_field_label(self, field):
        """Get label text for a field"""
        try:
            # Try to find associated label
            field_id = field.get_attribute("id")
            if field_id:
                label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{field_id}']")
                return label.text
            
            # Try parent label
            parent = field.find_element(By.XPATH, "./..")
            if parent.tag_name == "label":
                return parent.text
            
            return ""
        except:
            return ""
    
    def upload_resume(self):
        """Upload resume if file input exists"""
        if not self.is_browser_alive():
            return
        try:
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if file_inputs and os.path.exists(USER_INFO["resume_path"]):
                self.log("Uploading resume...")
                file_inputs[0].send_keys(USER_INFO["resume_path"])
                self.random_delay(1.5, 2.5)
                self.log("Resume uploaded")
        except NoSuchWindowException:
            pass
        except Exception as e:
            self.log(f"Resume upload skipped: {str(e)[:30]}", "WARN")
    
    def fill_dropdowns(self):
        """Fill dropdown/select fields"""
        if not self.is_browser_alive():
            return
        try:
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            
            for select_elem in selects:
                try:
                    select = Select(select_elem)
                    field_name = (select_elem.get_attribute("name") or "").lower()
                    field_id = (select_elem.get_attribute("id") or "").lower()
                    
                    field_info = f"{field_name} {field_id}"
                    
                    # Match dropdown to appropriate value
                    if "state" in field_info or "province" in field_info:
                        self.select_option(select, ["MD", "Maryland"])
                    
                    elif "country" in field_info:
                        self.select_option(select, ["United States", "US", "USA"])
                    
                    elif "degree" in field_info or "education" in field_info:
                        self.select_option(select, ["Bachelor", "BS", "Undergraduate"])
                    
                    elif "experience" in field_info:
                        self.select_option(select, ["2", "1-2", "0-2"])
                    
                except:
                    continue
        except:
            pass
    
    def select_option(self, select_element, possible_values):
        """Select an option from dropdown"""
        try:
            for value in possible_values:
                try:
                    select_element.select_by_visible_text(value)
                    return
                except:
                    try:
                        select_element.select_by_value(value)
                        return
                    except:
                        continue
        except:
            pass
    
    def answer_screening_questions(self):
        """Answer yes/no questions and checkboxes"""
        if not self.is_browser_alive():
            return
        try:
            # Find all radio buttons and checkboxes
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio'], input[type='checkbox']")
            
            for inp in inputs:
                try:
                    label_text = self.get_field_label(inp).lower()
                    question = label_text
                    
                    # Work authorization questions (F-1 OPT specific)
                    if any(keyword in question for keyword in ["authorized to work", "legally authorized", "work authorization", "eligible to work"]):
                        if "yes" in inp.get_attribute("value").lower() or inp.get_attribute("value") == "1":
                            inp.click()
                            print(f"✓ Answered: Work authorized (Yes - F-1 OPT)")
                    
                    # Sponsorship NOW (No - on OPT)
                    elif any(keyword in question for keyword in ["require sponsorship now", "need sponsorship", "currently require", "require visa sponsorship"]):
                        if "no" in inp.get_attribute("value").lower() or inp.get_attribute("value") == "0":
                            inp.click()
                            print(f"✓ Answered: Need sponsorship now (No - on OPT)")
                    
                    # Sponsorship FUTURE (Yes - will need H-1B)
                    elif any(keyword in question for keyword in ["future sponsorship", "will you require", "in the future"]):
                        if "yes" in inp.get_attribute("value").lower() or inp.get_attribute("value") == "1":
                            inp.click()
                            print(f"✓ Answered: Future sponsorship (Yes - H-1B)")
                    
                    # Willing to relocate
                    elif any(keyword in question for keyword in ["relocate", "relocation", "willing to move"]):
                        if "yes" in inp.get_attribute("value").lower():
                            inp.click()
                            print(f"✓ Answered: Willing to relocate (Yes)")
                    
                    # Remote work
                    elif any(keyword in question for keyword in ["remote", "work from home"]):
                        if "yes" in inp.get_attribute("value").lower():
                            inp.click()
                            print(f"✓ Answered: Remote work (Yes)")
                    
                    # Veteran status
                    elif "veteran" in question:
                        if "no" in inp.get_attribute("value").lower():
                            inp.click()
                    
                    # Disability
                    elif "disability" in question and "disable" not in question:
                        if "no" in inp.get_attribute("value").lower() or "decline" in inp.get_attribute("value").lower():
                            inp.click()
                    
                    # Gender
                    elif "gender" in question:
                        if "female" in inp.get_attribute("value").lower():
                            inp.click()
                    
                    # Race
                    elif "race" in question or "ethnicity" in question:
                        if "asian" in inp.get_attribute("value").lower():
                            inp.click()
                
                except:
                    continue
        except:
            pass
    
    def submit_application(self):
        """Find and click submit button"""
        if not self.is_browser_alive():
            return False
        try:
            self.random_delay(0.8, 1.5)

            # Look for various submit button patterns
            submit_buttons = self.driver.find_elements(By.XPATH,
                "//button[contains(text(), 'Submit') or contains(text(), 'Apply') or contains(text(), 'Continue') or contains(text(), 'Next')]")

            if not submit_buttons:
                submit_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                    "button[type='submit'], input[type='submit']")

            if submit_buttons:
                # Click the most likely submit button (usually the last one)
                submit_buttons[-1].click()
                self.random_delay(2.5, 4.0)
                self.log("Clicked submit button")
                return True
            else:
                self.log("No submit button found", "WARN")
                return False

        except NoSuchWindowException:
            self.log("Browser closed during submit", "ERROR")
            return False
        except Exception as e:
            self.log(f"Submit error: {str(e)[:30]}", "WARN")
            return False
    
    def apply_to_job(self, job):
        """
        Complete full application process with robust error handling.
        Handles BOTH Easy Apply AND external applications.
        """
        # Check browser health first
        if not self.is_browser_alive():
            self.log("Browser closed - cannot apply", "ERROR")
            return False

        try:
            self.log(f"Applying to: {job['title'][:40]}...")

            # Click on job to view details
            if not self.click_job(job):
                self.errors_count += 1
                return False

            # Detect application type (Easy Apply, External, or None)
            app_type = self.detect_application_type()

            if app_type == "none":
                self.log("No application method available")
                self.save_failed_job(job['url'], job['title'], job['company'], "No apply button found")
                self.skipped_jobs += 1
                return False

            # Handle based on application type
            if app_type == "external":
                # Handle external application (company site)
                self.log("Processing EXTERNAL application...")
                success = self.handle_external_application(job)
                if success:
                    self.log("EXTERNAL APPLICATION PROCESSED!")
                    self.save_applied_job(job['url'], job['title'], job['company'])
                    self.applications_today += 1
                    self.save_session_state()
                    return True
                else:
                    self.errors_count += 1
                    return False

            # Handle Easy Apply
            self.log("Processing EASY APPLY...")

            # Click Apply button using multiple strategies
            apply_clicked = False
            try:
                # Strategy 1: Indeed Apply wrapper button
                apply_wrapper = self.driver.find_elements(By.CSS_SELECTOR,
                    ".ia-IndeedApplyButton button, [class*='IndeedApply'] button")
                if apply_wrapper:
                    apply_wrapper[0].click()
                    apply_clicked = True
                    self.log("Clicked Apply button (IndeedApply wrapper)")

                # Strategy 2: Find button by text
                if not apply_clicked:
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for btn in all_buttons:
                        btn_text = btn.text.lower().strip()
                        if btn_text in ["apply now", "easily apply", "apply"]:
                            btn.click()
                            apply_clicked = True
                            self.log(f"Clicked Apply button (text: {btn_text})")
                            break

                # Strategy 3: Use wait with CSS selector
                if not apply_clicked:
                    apply_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR,
                            "button[class*='apply'], button[data-testid*='apply']"))
                    )
                    apply_button.click()
                    apply_clicked = True
                    self.log("Clicked Apply button (CSS selector)")

                if apply_clicked:
                    self.random_delay(2.0, 3.5)

            except NoSuchWindowException:
                self.log("Browser closed during apply", "ERROR")
                return False
            except TimeoutException:
                self.log("Apply button not clickable", "WARN")
                self.errors_count += 1
                return False
            except Exception as e:
                self.log(f"Could not click Apply button: {str(e)[:30]}", "WARN")
                self.errors_count += 1
                return False

            if not apply_clicked:
                self.log("No Apply button found to click", "WARN")
                self.errors_count += 1
                return False

            # Check for captcha
            if self.detect_captcha():
                self.log("CAPTCHA detected - saving for manual application")
                self.save_failed_job(job['url'], job['title'], job['company'], "Captcha detected")
                self.errors_count += 1
                return False

            # Fill the application form
            self.log("Filling application form...")
            self.fill_application_form()

            # Handle multi-step application if needed
            self.complete_multi_step_application()

            # Submit application
            if self.submit_application():
                # Check if successfully submitted
                self.random_delay(2.0, 3.0)

                # Look for success message - be thorough
                if self.is_browser_alive():
                    try:
                        # Check page text for success indicators
                        page_text = self.driver.page_source.lower()

                        success_phrases = [
                            "application sent",
                            "successfully applied",
                            "application submitted",
                            "application received",
                            "thank you for applying",
                            "your application has been submitted",
                            "you have applied",
                            "application complete",
                        ]

                        confirmed = False
                        for phrase in success_phrases:
                            if phrase in page_text:
                                self.log(f"APPLICATION CONFIRMED: '{phrase}' found!")
                                confirmed = True
                                break

                        if confirmed:
                            self.save_applied_job(job['url'], job['title'], job['company'])
                            self.applications_today += 1
                            self.save_session_state()
                            return True
                        else:
                            # No clear success message - log as uncertain
                            self.log("No confirmation message found - marking as UNCERTAIN")
                            self.save_failed_job(job['url'], job['title'], job['company'],
                                "Submitted but no confirmation - check manually")
                            return False

                    except Exception as e:
                        self.log(f"Error checking success: {str(e)[:30]}", "WARN")
                        self.save_failed_job(job['url'], job['title'], job['company'],
                            "Could not verify submission")
                        return False
            else:
                self.log("Could not complete submission", "WARN")
                self.save_failed_job(job['url'], job['title'], job['company'], "Submit button not found")
                self.errors_count += 1
                return False

        except NoSuchWindowException:
            self.log("Browser was closed - stopping application", "ERROR")
            return False
        except WebDriverException as e:
            self.log(f"Browser error: {str(e)[:40]}", "ERROR")
            self.errors_count += 1
            return False
        except Exception as e:
            self.log(f"Application error: {str(e)[:40]}", "WARN")
            self.save_failed_job(job['url'], job['title'], job['company'], str(e)[:50])
            self.errors_count += 1
            return False
    
    def run(self):
        """
        Main execution loop - FULLY AUTOMATIC MODE.
        Applies to ALL matching jobs without manual approval.
        Press Ctrl+C at any time to stop.
        """
        print(f"\n{'='*70}")
        print("  INDEED AUTO-APPLIER BOT - FULLY AUTOMATIC MODE")
        print(f"{'='*70}")
        print(f"  Applicant: {USER_INFO['full_name']}")
        print(f"  Email:     {USER_INFO['email']}")
        print(f"  Status:    F-1 OPT (Will need H-1B sponsorship)")
        print(f"  Goal:      {MAX_APPLICATIONS_PER_SESSION} applications")
        print(f"  Mode:      AUTOMATIC - Applying to ALL jobs (Easy Apply + External)")
        print(f"{'='*70}")
        print(f"  Press Ctrl+C at any time to stop the bot")
        print(f"{'='*70}\n")

        # Confirm resume path
        if not os.path.exists(USER_INFO["resume_path"]):
            self.log("ERROR: Resume not found!", "ERROR")
            print(f"Looking for: {USER_INFO['resume_path']}")
            return

        # Try to resume previous session
        self.load_session_state()

        # Launch browser
        if not self.setup_driver():
            self.log("Failed to launch browser - exiting", "ERROR")
            return

        # Store the original window handle
        self.original_window = self.driver.current_window_handle

        # Manual sign-in flow for Indeed
        self.log("Opening Indeed for sign-in...")
        self.driver.get("https://www.indeed.com")
        self.random_delay(2.0, 3.0)

        print(f"\n{'='*70}")
        print("  SIGN IN TO INDEED")
        print(f"{'='*70}")
        print("  1. Click 'Sign in' in the top right corner of the browser")
        print("  2. Enter your Indeed email and password")
        print("  3. Complete any verification if needed")
        print("  4. Once signed in, come back here and press Enter")
        print(f"{'='*70}")
        input("\n  Press Enter after you've signed in to Indeed... ")

        # Verify sign-in
        self.random_delay(1.0, 2.0)
        if self.check_if_logged_in():
            self.log("Indeed sign-in confirmed!")
        else:
            self.log("Could not verify sign-in - continuing anyway (Easy Apply will still work)")

        browser_closed = False

        try:
            for keyword_idx, keyword in enumerate(JOB_KEYWORDS[self.current_keyword_index:], self.current_keyword_index):
                if self.applications_today >= MAX_APPLICATIONS_PER_SESSION:
                    self.log(f"Reached goal of {MAX_APPLICATIONS_PER_SESSION} applications!")
                    break

                # Check browser health before each keyword
                if not self.is_browser_alive():
                    self.log("Browser closed - ending session", "ERROR")
                    browser_closed = True
                    break

                self.current_keyword_index = keyword_idx

                for loc_idx, location in enumerate(LOCATIONS[self.current_location_index:], self.current_location_index):
                    if self.applications_today >= MAX_APPLICATIONS_PER_SESSION:
                        break

                    # Check browser health
                    if not self.is_browser_alive():
                        browser_closed = True
                        break

                    self.current_location_index = loc_idx

                    if not self.search_jobs(keyword, location):
                        continue

                    job_cards = self.get_job_listings()
                    total_jobs = len(job_cards)

                    for job_idx, job_card in enumerate(job_cards, 1):
                        if self.applications_today >= MAX_APPLICATIONS_PER_SESSION:
                            break

                        # Check browser health before each job
                        if not self.is_browser_alive():
                            browser_closed = True
                            break

                        try:
                            job = self.extract_job_details(job_card)
                            if not job:
                                continue

                            # Skip if already applied
                            if job['url'] in self.applied_jobs:
                                self.log(f"Already applied to: {job['company'][:20]}")
                                continue

                            # Skip if already in failed jobs (will need manual follow-up)
                            if job['url'] in self.failed_jobs:
                                self.log(f"Previously failed: {job['company'][:20]} - skipping")
                                continue

                            # Display job with progress
                            self.display_job(job, job_idx, total_jobs)

                            # AUTOMATIC MODE: Apply to all jobs without asking
                            self.log("AUTO-APPLYING...")
                            success = self.apply_to_job(job)

                            if success:
                                self.log(f"Progress: {self.applications_today}/{MAX_APPLICATIONS_PER_SESSION} applications")
                            else:
                                self.log("Application could not be completed - continuing to next job")

                            # Random delay between applications (anti-detection)
                            self.random_delay(2.0, 4.0)

                        except StaleElementReferenceException:
                            self.log("Job element expired, continuing to next", "WARN")
                            continue
                        except NoSuchWindowException:
                            browser_closed = True
                            break
                        except Exception as e:
                            self.log(f"Error processing job: {str(e)[:40]}", "WARN")
                            self.errors_count += 1
                            continue

                    if browser_closed:
                        break

                    # Reset location index for next keyword
                    self.current_location_index = 0
                    self.random_delay(3.0, 5.0)  # Delay between searches

                if browser_closed:
                    break

        except KeyboardInterrupt:
            self.log("Bot stopped by user (Ctrl+C)")

        except Exception as e:
            self.log(f"Unexpected error: {str(e)[:50]}", "ERROR")

        finally:
            # Save final state
            self.save_session_state()

            # Print comprehensive summary
            duration = datetime.now() - self.session_start_time
            print(f"\n{'='*70}")
            print("  SESSION SUMMARY - AUTOMATIC MODE")
            print(f"{'='*70}")
            print(f"  Applications submitted: {self.applications_today}")
            print(f"  External apps attempted: {self.external_apps}")
            print(f"  Jobs skipped:           {self.skipped_jobs}")
            print(f"  Errors encountered:     {self.errors_count}")
            print(f"  Failed (need manual):   {len(self.failed_jobs)}")
            print(f"  Total in database:      {len(self.applied_jobs)}")
            print(f"  Session duration:       {str(duration).split('.')[0]}")
            print(f"{'='*70}")

            # Show info about failed jobs for manual follow-up
            if self.failed_jobs:
                print(f"\n  Jobs needing manual attention: {len(self.failed_jobs)}")
                print(f"  Check file: {FAILED_JOBS_FILE}")

            if browser_closed:
                print("\n  Browser was closed. Session state saved.")
                print("  Run again to resume from where you left off.")
            else:
                input("\n  Press Enter to close browser...")
                try:
                    if self.driver:
                        self.driver.quit()
                except Exception:
                    pass

            print("\n  Thank you for using Indeed Auto-Applier - Smart Edition!")
            print("  Tip: Run daily to apply to fresh job postings!")
            print("  Tip: Check failed_jobs.json for jobs that need manual application.\n")

if __name__ == "__main__":
    print(f"\n{'='*70}")
    print("  INDEED AUTO-APPLIER BOT - SMART EDITION")
    print(f"{'='*70}")
    print("\n  NEW FEATURES:")
    print("  - FULLY AUTOMATIC: No manual Y/N approval needed")
    print("  - ALL JOBS: Applies to Easy Apply + External applications")
    print("  - SMART FORMS: Handles Workday, Greenhouse, Lever, iCIMS, etc.")
    print("  - AUTO ACCOUNTS: Uses LinkedIn/Google sign-in or creates accounts")
    print("  - MULTI-STEP: Navigates multi-page application forms")
    print("  - CAPTCHA SKIP: Detects captchas, logs for manual follow-up")
    print(f"\n  Requirements:")
    print("  1. Python 3 installed")
    print("  2. Required packages: pip3 install selenium undetected-chromedriver")
    print("  3. Resume path configured correctly")
    print(f"\n  Resume path: {USER_INFO['resume_path']}")

    if os.path.exists(USER_INFO["resume_path"]):
        print("  Status: Resume file FOUND")
    else:
        print("  Status: Resume NOT FOUND - please update path in USER_INFO")

    # Check for previous session
    if os.path.exists(SESSION_STATE_FILE):
        try:
            with open(SESSION_STATE_FILE, 'r') as f:
                state = json.load(f)
                if state.get("date") == datetime.now().strftime("%Y-%m-%d"):
                    print(f"\n  Previous session found: {state.get('applications_today', 0)} apps done today")
                    print("  Session will resume from where you left off")
        except Exception:
            pass

    # Check for failed jobs that need manual attention
    if os.path.exists(FAILED_JOBS_FILE):
        try:
            with open(FAILED_JOBS_FILE, 'r') as f:
                failed = json.load(f)
                if failed:
                    print(f"\n  NOTICE: {len(failed)} jobs need manual follow-up")
                    print(f"  See: {FAILED_JOBS_FILE}")
        except Exception:
            pass

    print(f"\n{'='*70}")
    print("  WARNING: This bot will automatically apply to ALL matching jobs!")
    print("  Press Ctrl+C at any time to stop the bot.")
    print(f"{'='*70}")

    proceed = input("\n  Start AUTOMATIC job application? (y/n): ").strip().lower()

    if proceed == 'y':
        bot = IndeedAutoApplier()
        bot.run()
    else:
        print("\n  To install required packages:")
        print("  pip3 install selenium undetected-chromedriver")
        print("\n  Then run: python3 indeed_auto_applier.py")
        print("\n  Check failed_jobs.json for jobs that need manual application.\n")