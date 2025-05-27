
LifeStruct: Your Smart Schedule & Job Assistant
LifeStruct is a desktop app designed to help students and professionals manage their learning goals, schedules, and job applications efficiently. It offers a smart timetable for academic pursuits and a dedicated assistant for your job search.

Features
📅 Smart Timetable
Manage Learning Goals: Set and track your study objectives with custom durations and daily hours.
Add Fixed Events: Easily input classes, meetings, or other commitments to avoid scheduling conflicts.
Generate Schedule: Get an instant schedule based on your goals and fixed events.
Track Progress: Mark tasks as complete to monitor your academic journey.
💼 Job Assistant
CV Upload & Analysis: Upload your PDF CV to automatically extract key skills.
Application Tracker: Keep tabs on your job applications, noting company, position, and status.
Job Description Matcher: Paste job descriptions to see how well your CV's skills align.
Cover Letter Drafts: Generate a basic cover letter tailored to the job description and your CV.
Installation
To get LifeStruct running:

Clone the repository:

Bash

git clone https://github.com/your-username/LifeStruct.git
cd LifeStruct
(Adjust the URL if your repository is different.)

Set up a virtual environment:

Bash

python -m venv venv
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
(Ensure requirements.txt lists PyPDF2 and openai.)

Building the Executable
You can create a standalone executable using PyInstaller. First, pip install pyinstaller, then run:

Bash

pyinstaller --onefile --windowed --add-data "assets;assets" --hidden-import=PyPDF2 --hidden-import=openai --icon=assets/app.ico lifestruct.py
Find your executable in the dist/ folder. (Remember to rename your main file to lifestruct.py if it's currently studentlifeos.py.)

Usage
Launch the app by running python lifestruct.py or the executable from the dist/ folder.

Smart Timetable: Enter goals and fixed events, then click "🤖 Generate AI Schedule". Select tasks and click "✅ Mark Selected as Complete".
Job Assistant: "📎 Upload CV (PDF)", add new applications with company, position, and status. Paste job descriptions and hit "🔍 Analyze Match & Generate Cover Letter" for instant insights.
Project Structure
LifeStruct/
├── lifestruct.py       # Main application code
├── requirements.txt    # Python dependencies
├── dist/               # Contains the executable
├── user_data/          # Stores your saved data (schedule, applications, CV)
└── assets/             # Application icons and resources
Future Enhancements
We're planning to add more advanced AI scheduling, better NLP for skill extraction, calendar integration, notifications, and analytics.

Contributing
Contributions are welcome! Fork the repo, create a feature branch, make your changes, commit, push, and open a Pull Request.

License
This project is licensed under the MIT License.

FAQ
Q: What is LifeStruct?
A: A desktop app for managing student schedules, learning goals, and job applications.

Q: Is it free?
A: Yes, it's open-source and free.

Q: What OS does it support?
A: Runs on Windows, macOS, and Linux.

Q: How smart is the "AI Schedule"?
A: Currently, it uses simple logic to distribute goals. Future versions will have more advanced AI.

Q: Is my CV data safe?
A: All data is stored locally in the user_data folder; nothing is sent externally.