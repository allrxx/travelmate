# Travel Easy
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Overview
**Travel Easy** is a full-stack web application designed to simplify travel booking experiences. Built with **Python** and **Flask**, this platform allows users to browse travel packages, book trips, and view their booking history. The responsive and user-friendly interface ensures ease of use across various devices. With Docker integration, the application can be deployed seamlessly in containerized environments.

## 🎥 Demo
![App Demo](./demo.gif)

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** PostgreSQL (via SQLAlchemy)
- **Testing:** Selenium WebDriver
- **Browser Automation:** ChromeDriver
- **Containerization:** Docker

## ✨ Features
- Secure user authentication (Login/Signup via Flask).
- Browse and filter travel packages.
- Real-time booking and confirmation system.
- Viewable booking history with bill generation.
- Fully responsive user dashboard for travel package management.

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker (Latest version)
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/allrxx/TRAVEL_EASY.git
   ```
2. **Navigate into the project directory**:
   ```bash
   cd TRAVEL_EASY
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add your configuration details (e.g., database URL).

5. **Run the application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000`.

## 🐋 Docker Integration

### Building and Running Containers

#### PostgreSQL
1. **Pull the PostgreSQL image**:
   ```bash
   docker pull postgres:latest
   ```
2. **Run the PostgreSQL container**:
   ```bash
   docker run --name my-postgres --network my-network \
   -e POSTGRES_USER=<your_user> -e POSTGRES_PASSWORD=<your_password> -e POSTGRES_DB=<your_database> \
   -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -d postgres:latest
   ```

#### pgAdmin
1. **Pull the pgAdmin image**:
   ```bash
   docker pull dpage/pgadmin4:latest
   ```
2. **Run the pgAdmin container**:
   ```bash
   docker run --name my-pgadmin --network my-network \
   -e PGADMIN_DEFAULT_EMAIL=<your_email> -e PGADMIN_DEFAULT_PASSWORD=<your_password> \
   -p 5050:80 -d dpage/pgadmin4
   ```

#### Flask Application
1. **Build the Docker image**:
   ```bash
   docker build --no-cache -t flask-app .
   ```
2. **Run the Flask container**:
   ```bash
   docker run --name flask-app --network my-network -p 5000:5000 -v "%cd%:/app" flask-app
   ```

#### Jenkins
1. **Pull the Jenkins image**:
   ```bash
   docker pull jenkins/jenkins:lts
   ```
2. **Run the Jenkins container**:
   ```bash
   docker run --name my-jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -d jenkins/jenkins:lts
   ```

### Managing Containers
- **Stop a container**:
  ```bash
  docker stop <container_name>
  ```
- **Remove a container**:
  ```bash
  docker rm <container_name>
  ```
- **Access a running container**:
  ```bash
  docker exec -it <container_name> sh
  ```

## 🧪 Testing with Selenium WebDriver

### Setting Up Selenium
1. **Install Selenium**:
   Ensure Selenium is installed by running:
   ```bash
   pip install selenium
   ```
2. **Install ChromeDriver**:
   Download ChromeDriver compatible with your browser version from [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads).
   Add it to your system's PATH or specify its location in your tests.

### Running Tests
The test file `test_app.py` contains unit tests for the Travel Easy application.

1. Start the Flask application locally:
   ```bash
   python app.py
   ```
2. Run the tests:
   ```bash
   python -m unittest test_app.py
   ```

### Key Test Scenarios
- **User Authentication**:
  - Test login and signup flows.
- **Package Management**:
  - Verify adding packages to the cart.
- **Booking History**:
  - Check booking history retrieval and bill generation.
- **Logout**:
  - Ensure user logout functionality works.

## 🏃 Usage
- **Sign Up**: Create a new user account.
- **Book Travel Packages**: Browse and book packages directly from the dashboard.
- **View Booking History**: Access previous bookings and generate bills.

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📞 Contact
Alex E J - [LinkedIn](https://www.linkedin.com/in/alexjoy89) - alexjoy0480@gmail.com
