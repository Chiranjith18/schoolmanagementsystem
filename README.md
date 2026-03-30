# College Management System – User Manual

## Getting Started

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

Create a `.env` file in the root directory with the following:

```env
SECRET_KEY=your-secret-key
DEBUG=1
DATABASE_URL=postgres://user:password@host:5432/dbname
```

> **Note:** `DATABASE_URL` is required — the app will not start without it. Use a PostgreSQL connection string (e.g. from Supabase, Railway, or a local Postgres instance).

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://localhost:8000` in your browser and `http://localhost:8000/admin` for the admin panel.

---

This guide explains the workflow for **Admin, Teacher, and Student** users.

---

## 1. Admin Setup

**Login:**
- Open your browser and navigate to the admin panel at `/admin`
- **Username:** `admin`
- **Password:** `admin123`

**Add Base Data:**

- **Subjects:**
  - Go to **Academics → Subjects → Add**
  - Example: `Name = Mathematics`, `Code = MATH101` → Save

- **Semesters:**
  - Go to **Academics → Semesters → Add**
  - Example: `Year = 1`, `Semester = 1` → Save

- **Assessments:**
  - Go to **Academics → Assessment Types → Add**
  - Example: `Name = Internal 1`, `Max Marks = 25` → Save
  - Example: `Name = Semester`, `Max Marks = 100` → Save

**Create Users:**
- Admin **creates usernames and passwords** for Teachers and Students.
- **Teachers:** Go to **Users → Add** → select `Role = Teacher` → Save
- **Students:** Go to **Users → Add** → select `Role = Student` → Save

**Assign Teachers to Subjects:**
- Go to **Academics → Teacher Assignments → Add**
- Select **Teacher**, **Subject**, **Semester** → Save

✅ **Admin setup is done!**

---

## 2. Teacher Workflow

**Login:**
- Navigate to the homepage `/`
- **Username:** assigned by Admin
- **Password:** assigned by Admin

**Mark Attendance:**
- Go to **Teacher Dashboard → Attendance**
- Select **Student**, **Subject**, **Date** → Mark Present/Absent → Submit

**Assign Marks:**
- Go to **Teacher Dashboard → Assign Marks**
- Select **Student**, **Subject**, **Assessment** → Enter marks → Submit

✅ Teachers can now manage attendance and assign marks for their students.

---

## 3. Student Workflow

**Login:**
- Navigate to the homepage `/`
- **Username:** assigned by Admin
- **Password:** assigned by Admin

**View Results:**
- Go to **Student Dashboard**
- Check **marks per subject** and **attendance percentage**

✅ Students can view their marks and attendance summary at any time.

---

## 4. Sample Flow

1. Admin logs in → adds **Mathematics, Semester 1, Internal 1**
2. Admin creates **Teacher1** and **Student1** with usernames/passwords
3. Admin assigns Teacher1 to teach Mathematics in Semester 1
4. Teacher1 logs in → marks **attendance** and assigns **marks 22/25** for Student1
5. Student1 logs in → views **marks and attendance summary**

---

## Tips

- All setup can be done via `/admin` – **no Swagger or API calls required**.
- Teachers use the main homepage `/` to mark attendance and assign marks.
- Students use the homepage `/` to view marks and attendance.
- Marks and attendance are automatically updated in the Student Dashboard.
