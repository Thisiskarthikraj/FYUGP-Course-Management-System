
# FYUGP Management System 🎓  

## 📌 Project Overview  
The **FYUGP (Four-Year Undergraduate Programme) Management System** is a web-based application designed to streamline the process of course registration, department transfers, and academic management for students and faculty members.  

The system aims to **ensure flexibility in course selection** while preventing schedule conflicts and maintaining a structured approach to inter-departmental course enrollments.  

## 🎯 Objectives  
- Provide students with an easy-to-use **course registration** system.  
- Allow department heads to **approve inter-department enrollments**.  
- Enable **automatic schedule conflict detection** for students.  
- Maintain **academic records** of students, courses, and faculty.  
- Facilitate **inter-department transfers** after one semester.  

---

## 🚀 Features  

### 🔹 **Admin Features**  
- Register new **departments** and manage them.  
- Add and manage **students**
- Register courses and mdc course management   



### 🔹 **Student Features**  
- **View available courses** across different departments.  
- Register for up to **3 courses per semester** (with approval for inter-department courses).  
- Check **class schedules** to avoid timing conflicts.  
- Apply for **inter-department transfers** after completing a semester.  
 

---

## 🛠️ Tech Stack  
- **Backend:** Django  
- **Database:** SQLite  
- **Frontend:** HTML, CSS (Custom Styling, No Bootstrap)  
- **Authentication:** Custom Django-based login system  

---



---

## 🎯 How to Run the Project  

### 🔹 Step 1: Clone the Repository  
```bash
git clone https://github.com/your-username/fyugp.git
cd fyugp
```

### 🔹 Step 2: Create and Activate Virtual Environment  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 🔹 Step 3: Install Dependencies  
```bash
pip install -r requirements.txt
```

### 🔹 Step 4: Apply Migrations & Run Server  
```bash
python manage.py migrate
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---



## 📝 Future Enhancements  
- **Automated schedule conflict detection** to prevent overlapping classes.  
- **Notification system** for approvals and updates.  
- **Enhanced student dashboard** for better course tracking.  
- **Reports & analytics** for student academic performance.  

---

## 🤝 Contributing  
Contributions are welcome! If you'd like to improve the project, fork the repository, make changes, and submit a pull request.  

---

## 📜 License  
This project is open-source and available under the MIT License.  

---

**💡 FYUGP: Simplifying Course Registration for the Future!**
```

