**INVESTIE**

**Introduction**

Investie is a full-stack Django web application designed to increase financial literacy among new 
investors and streamline personal investment tracking and analysis. This project integrates a user-friendly frontend, robust middleware and a secure backend to provide a seamless experience for users.

**Project Aim & Objectives**

Aim: Develop a comprehensive platform to allow user to monitor and track stocks to their liking with several views which provide real time and historical data.

Objectives: 
1. Implement secure user authentication
2. Enable users to create, read, update and delete watchlists
3. Provide real time data visualisation
4. Deploy the application for public access

**Enterprise considerations**

Performance 

- Utilized Django's efficent ORM for optimized database queires
- Implemented caching to reduce server load and improve response time

Scalability
- Adopted a modular achitechture separating conceresn across different Django applications
- Designed a system that accomodates to increasing user loads and data volume

Security
- Employed Django's built-in authentication system with password hashing
- Implemented CSRF protection and input validation to prevent common web vulnerabilities
- Ensured user-friendly error messages

Deployment
- Deployed the application on Render
- Configured continuous integration and deployment pipelines for streamlined updates

**Installation and usage instructions**

Prerequisites
- Python 3.x
- pip
- Your chosen database
- Git

Setup Steps

1. Clone the repository:
   ```
   git clone https://github.com/MayaHA2512/Investie.git
   cd Investie
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure enviroment variables:
   - Create a .env file in the root directory.
   - Add the following variables:
     ```
     SECRET_KEY=your_secret_key
     DEBUG=True
     DATABASE_URL=your_database_url
     ```
5. Apply migrations:
   ```
   python manage.py migrate
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```
7. Access the application at http://localhost:8000/ in your web browser







