# LifeStruct

Transform chaos into structure. LifeStruct is the all-in-one desktop companion that turns your academic goals and career aspirations into actionable, organized plans.

![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Privacy & Security](#privacy--security)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [FAQ](#faq)
- [License](#license)

## About

**The Problem:** Students and professionals juggle countless learning goals, job applications, and deadlines—often losing track of what matters most.

**The Solution:** LifeStruct brings AI-powered organization to your academic and professional life, turning overwhelming to-do lists into structured, achievable plans.

## Features

### Smart Timetable Management
- **Goal-Driven Planning**: Set learning objectives with custom durations and daily time commitments
- **Conflict-Free Scheduling**: Add classes, meetings, and commitments to avoid double-booking
- **AI Schedule Generation**: Get intelligent timetables that optimize your time and energy
- **Progress Tracking**: Visual completion tracking to keep you motivated and on track

### Intelligent Job Assistant
- **CV Analysis**: Upload PDF resumes for automatic skill extraction and analysis
- **Application Tracking**: Centralized dashboard for all job applications with status monitoring
- **Skill Matching**: Compare your CV against job descriptions to identify strengths and gaps
- **Cover Letter Generation**: AI-powered cover letter drafts tailored to specific opportunities

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/LifeStruct.git
   cd LifeStruct
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch LifeStruct**
   ```bash
   python lifestruct.py
   ```

### Building Standalone Executable

Create a portable version that runs without Python installation:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed \
  --add-data "assets;assets" \
  --hidden-import=PyPDF2 \
  --hidden-import=openai \
  --icon=assets/app.ico \
  lifestruct.py
```

Find your executable in the `dist/` folder.

## Usage

### Smart Timetable
1. **Set Learning Goals**: Define what you want to learn, how long it should take, and daily time commitment
2. **Add Fixed Events**: Input classes, meetings, or other non-negotiable commitments
3. **Generate Schedule**: Click "Generate AI Schedule" for an optimized timetable
4. **Track Progress**: Mark completed tasks to visualize your journey

### Job Assistant
1. **Upload Your CV**: Click "Upload CV (PDF)" to extract and analyze your skills
2. **Track Applications**: Add job applications with company details and status updates
3. **Analyze Job Fit**: Paste job descriptions and click "Analyze Match & Generate Cover Letter"
4. **Get Insights**: Review skill matches and generated cover letter drafts

## Project Structure

```
LifeStruct/
├── lifestruct.py          # Main application
├── requirements.txt       # Dependencies
├── dist/                  # Built executables
├── user_data/            # Your saved data (local only)
│   ├── schedule.json
│   ├── applications.json
│   └── cv_analysis.json
├── assets/               # App resources
│   └── app.ico
└── README.md
```

## Privacy & Security

**Your data stays yours.** LifeStruct stores all information locally in the `user_data/` folder. No data is transmitted to external servers, ensuring complete privacy and control over your personal information.

## Roadmap

### Coming Soon
- **Advanced AI Scheduling**: Machine learning-powered optimization based on your productivity patterns
- **Enhanced NLP**: Better skill extraction and job description analysis
- **Calendar Integration**: Sync with Google Calendar, Outlook, and other popular platforms
- **Smart Notifications**: Intelligent reminders and deadline alerts
- **Analytics Dashboard**: Insights into your productivity and job search progress
- **Mobile Companion**: Sync with mobile app for on-the-go access

## Contributing

We love contributions! Here's how you can help make LifeStruct better:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Found a Bug?
Open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your system information

## FAQ

**Q: Is LifeStruct really free?**  
A: Yes! It's completely open-source under the MIT License.

**Q: What operating systems are supported?**  
A: Windows, macOS, and Linux are all supported.

**Q: How "smart" is the AI scheduling?**  
A: Currently uses intelligent logic for time distribution. Advanced ML features coming in future releases.

**Q: Can I use this for team projects?**  
A: Currently designed for individual use, but team features are on our roadmap.

**Q: What file formats does it support for CVs?**  
A: PDF format is currently supported, with more formats planned.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for students and professionals who refuse to let chaos win.**

[Report Bug](https://github.com/your-username/LifeStruct/issues) • [Request Feature](https://github.com/your-username/LifeStruct/issues) • [Documentation](https://github.com/your-username/LifeStruct/wiki)
