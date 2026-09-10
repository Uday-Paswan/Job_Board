# JobBoard — Recruitment & Job Listing Platform

A full-stack job board web application built with Django, where recruiters can post job openings and job seekers can browse, search, and apply with resume uploads.

**Live demo:** https://job-board-8o5t.onrender.com/

> Note: hosted on Render's free tier, so the first load after a period of inactivity may take 20–30 seconds while the server spins back up.

---

## Features

- **Role-based accounts** — users sign up as either a Job Seeker or a Recruiter, with separate permissions and dashboards for each.
- **Recruiters** can post jobs, view all applicants per job, and track applicant status from a dedicated dashboard.
- **Job seekers** can browse and search jobs, apply with a resume upload, and track their application history and status.
- **Search & filtering** — jobs can be filtered by keyword (title, description, or skills), location, and job type, all combinable at once.
- **Duplicate-application prevention**, enforced both at the database level (a `unique_together` constraint) and in the view logic.
- **Secure authentication** — signup, login, logout, and role-based access control, with every protected view checked server-side (not just hidden in the UI).
- **Custom UI** — hand-written HTML/CSS/JavaScript throughout (no CSS framework), including a responsive navbar, toast notifications, and a custom logout confirmation modal.
- **Fully responsive**, tested down to mobile screen widths.

---

## Tech stack

- **Backend:** Python, Django
- **Database:** PostgreSQL (production), SQLite (local development)
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Deployment:** Render, with Gunicorn as the WSGI server and WhiteNoise for static file serving

---

## Data model

Three core models drive the app:

- `Profile` — extends Django's built-in `User` via a `OneToOneField`, storing each user's role (`seeker` or `recruiter`).
- `JobPost` — a job listing, linked to the recruiter who posted it via `ForeignKey`.
- `Application` — the join between a `JobPost` and an applicant `User`, holding the uploaded resume and application status. Enforces one application per user per job via `unique_together`.

---

## Running locally

```bash
git clone https://github.com/Uday-Paswan/Job_Board.git
cd Job_Board/job_board

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/jobs/` in your browser.

---

## Known limitations

- **Resume file storage is not persistent in production.** Render's free tier uses an ephemeral filesystem, so uploaded resumes can be lost on redeploy. Job posts, user accounts, and application records persist correctly (they're stored in PostgreSQL) — only the physical uploaded file is affected. In a production deployment, this would be solved by storing uploads on a service like AWS S3 or Cloudinary instead of local disk.
- No employer analytics (e.g. view counts per listing) are currently tracked.

---

## Possible future improvements

- Move resume storage to S3/Cloudinary for persistence across deploys
- Email notifications when an application's status changes
- Pagination on the job listing page
- Job view-count tracking for recruiters

---

Built as a learning project to practice Django's full request/response cycle, ORM relationships, authentication, role-based permissions, and deployment.
