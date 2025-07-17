Task Manager Web App

#### Video Demo: https://youtu.be/xjkQoc2F8nk?si=ETDYmom8uD0zrFWB
#### Author: Ferdaous
#### GitHub: [github.com/ferdaous3](https://github.com/ferdaous3)
#### Location: Mostaganem, Algeria
#### Date: 15 July 2025

---

## Description:

This is my final project for Harvard's CS50x course: a simple yet functional task manager web app that allows users to register, log in, and manage their personal tasks.

The application is designed to help users stay organized by adding tasks to a personal to-do list. Each user has a private session where they can view and add tasks. The interface is fully in Arabic, making it more accessible and friendly for Arabic speakers.

---

## Features:

- ✅ User registration with secure password hashing.
- ✅ Login/logout system using Flask sessions.
- ✅ Add tasks that are saved to a SQLite database.
- ✅ Tasks are user-specific; each user sees only their tasks.
- ✅ Clean, Arabic-friendly web UI built with HTML and CSS.
- ✅ Simple database structure using SQLite3.

---

## Technologies Used:

- Python 3
- Flask
- Flask-Session
- SQLite
- HTML5 / CSS3
- Jinja2 templating engine
- Werkzeug (for password hashing)

---

## Folder Structure:

project/ ├── app.py               # Main Flask application ├── requirements.txt     # List of Python dependencies ├── README.md            # Project description ├── templates/           # HTML templates (Jinja2) │   ├── layout.html │   ├── index.html │   ├── login.html │   └── register.html └── static/ └── style.css        # Custom styling

---

## How It Works:

When the app starts, it initializes a SQLite database containing two tables: users and tasks.

- A new user can register via the registration page.
- Passwords are hashed before storage.
- Upon login, a Flask session is started.
- The user can then add tasks to their personal list.
- The homepage displays all tasks associated with the logged-in user.
- Users can log out anytime, which clears their session.

---

## Design Decisions:

I chose to focus on simplicity and clarity. The application doesn’t support deleting or editing tasks — instead, it provides a minimal core feature set that works reliably and showcases my understanding of web development, routing, session management, and database integration.

Making the interface in Arabic was also an intentional choice, as I wanted the app to feel native for Arabic-speaking users like myself. I wrote the HTML manually and avoided heavy frameworks to better understand how everything works together.

---

## Challenges Faced:

- Managing user sessions and linking tasks to user IDs was tricky at first.
- Designing a basic user interface in Arabic while ensuring right-to-left readability was a unique experience.
- Handling errors like duplicate usernames or empty inputs required extra attention.
- Keeping the structure clean while maintaining separation of logic and UI taught me a lot.

---

## Future Improvements:

- Add ability to delete or mark tasks as done.
- Make tasks editable.
- Add deadlines or priority levels to tasks.
- Improve styling with a CSS framework like Bootstrap.
- Host the app online (e.g., on Replit, Render, or Heroku).

---

## Conclusion:

This project represents how far I’ve come with CS50x. From knowing little about backend development to creating this full working web app in Flask, I’m proud of what I achieved. I plan to keep improving it and continue building more complex apps in the future.

Thanks CS50!
