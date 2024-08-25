# StatusCODE_1 Team Alias 2024
# Track : Education

# Problem Statement
The education track encourages participants to build software solutions that enhance the quality of education. Participants might develop applications that provide personalized learning experiences, improve access to education for disadvantaged communities, or help teachers and students collaborate more effectively.

# Impact Hub

## Description
Impact Hub is a web-based platform built using Flask, designed to empower children in rural areas by connecting them with volunteers from NGOs who offer educational support in various fields. The platform serves as a bridge between volunteers and students, ensuring that children in underprivileged regions receive the education and guidance they need.


Key features of Impact Hub include:

Volunteer Coordination: Facilitates the matching of NGO volunteers with children based on educational needs.
Student Progress Tracking: Provides a comprehensive record of each student's progress, detailing the tasks assigned by volunteers and their completion status.
Standard Level Assessment: Offers an evaluation of the child's educational level, helping volunteers tailor their support to the student's needs.
Impact Hub aims to make a meaningful difference in the lives of children by providing them with the educational tools and mentorship necessary to succeed.

## Requirements
- Python (Flask) on your system or on your deployment environment.
- Frontend : HTML , CSS

## Installation
Step 1: Clone the Repository
Start by cloning the repository from GitHub to your local machine.

**git clone https://github.com/priyanshu3082/ImpactHub.git**

Step 2: Navigate to the Project Directory

**cd impact-hub**

Step 3: Create a Virtual Environment 

**python -m venv env**

Activate the virtual environment:

On Windows
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

Step 4: Install the Required Dependencies

pip install -r requirements.txt

Step 5: Set Up Environment Variables
Create a .env file in the root directory of the project and set up the necessary environment variables. For example:

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url

Step 6: Initialize the database

flsk db upgrade

Step 7: Access the Application
Open your web browser and go to http://127.0.0.1:5000/ to start using Impact Hub.
## Contributing
Contributions to friend.ly are welcome! If you find any bugs, have feature requests, or want to contribute code, please open an issue or submit a pull request to the project repository.
