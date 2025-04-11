# **INVESTIE**

## **Introduction**

**Investie** is a full-stack Django web application designed to empower new investors by enhancing their financial literacy and providing a streamlined, interactive platform for personal investment tracking and analysis. This project integrates a user-friendly frontend, robust middleware, and a secure backend to offer a seamless user experience.

## **Project Aim & Objectives**

### **Aim:**
Develop a comprehensive platform that allows users to track and monitor stocks of their choice through various views providing real-time and historical data.

### **Objectives:**
1. **Implement secure user authentication.**
2. **Enable users to create, read, update, and delete watchlists.**
3. **Provide real-time data visualization.**
4. **Deploy the application for public access.**

## **Enterprise Considerations**

### **Performance:**
- Utilized Django's efficient ORM to optimize database queries.
- Implemented caching to reduce server load and improve response times.

### **Scalability:**
- Adopted a modular architecture, separating concerns across different Django applications.
- Designed a system that accommodates increasing user loads and growing data volumes.

### **Security:**
- Employed Django's built-in authentication system with password hashing.
- Implemented CSRF protection and input validation to mitigate common web vulnerabilities.
- Ensured user-friendly error messages for a smooth experience.

### **Deployment:**
- Deployed the application on **Render** for robust hosting.
- Configured continuous integration and deployment pipelines to streamline updates.

## **Installation and Usage Instructions**

### **Prerequisites:**
- **Python 3.x**
- **pip**
- Your preferred database
- **Git**


Setup Steps

1. Clone the repository:
   ```python
   git clone https://github.com/MayaHA2512/Investie.git
   cd Investie
   ```
2. Create and activate a virtual environment:
   ```python
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```python
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
   ```python
   python manage.py migrate
   ```
6. Run the development server:
   ```python
   python manage.py runserver
   ```
7. Access the application at http://localhost:8000/ in your web browser

**Feature overview**

**Realtime and historical data visualisation** 

Purpose: Provides users with graphical representations of stock performance, helping them make informed investment decisions

Location in Code: 
- Frontend: templates/analysis.html
- Logic/Data: views.py
- Charts: Chart.js integration in the front end

Endpoints / Modules involved:

- Yahoo Finance API: yfinance was used to provide both realtime and historical data that was then surfaced for our analysis page as seen below
  ```python
  def index(request):
    ticker = request.GET.get('ticker', 'AAPL')
    stock_data = yf.Ticker(ticker).history(period="6mo", auto_adjust=True)
    labels = stock_data.index.strftime('%Y-%m-%d').tolist()
    data = stock_data['Close'].tolist()
    chart_data = {
        'labels': labels,
        'data': data
    }
  ```
- JS chart logic:
  ```python
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  const myChart = new Chart(ctx, {
             type: 'line',
             data: {
                 labels: data.labels,
                 datasets: [{
                     label: 'My First Dataset',
                     data: data.data,
                     borderColor: 'rgba(75, 192, 192, 1)',
                     borderWidth: 1
                 }]
             }
         })
  ```
  
This is an example of the live pricing and the historical data that has been plotted:

<img width="1437" alt="Screenshot 2025-04-11 at 20 09 50" src="https://github.com/user-attachments/assets/98f2a143-3e91-4f06-ab09-629f4c6f8267" />

**User Authentication (Register/Login)**

Purpose: Provides users confidence that they're information is being stored safely 
Location in Code: 
- Frontend: templates/registration/register.html + templates/registration/login.html
- Logic/Data: views.py
- Authentication: Django user authentication system

Endpoints / Modules involved:

- Login Endpoint:
  - URL: /login/
  - Method: POST (and GET for rendering the login page)
  - Description: This endpoint handles user login by accepting credentials (username/email and password). Upon successful authentication, the user is granted access to the            system, and a session is created
  - View: Handled by Django's built-in LoginView

- django.contrib.auth library which helps with:
  1. Password strength checking
  2. Throttling of login attempts
  3. Authentication against third-parties (OAuth, for example)
 


