import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from datetime import datetime, timedelta
import PyPDF2
import openai
from pathlib import Path

class StudentLifeOS:
    def __init__(self, root):
        self.root = root
        self.root.title("StudentLifeOS - Smart Schedule & Job Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Data directories
        self.data_dir = Path("user_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.goals = []
        self.schedule = []
        self.applications = []
        self.cv_data = None
        self.fixed_events = []
        
        # Load existing data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="StudentLifeOS", 
                              font=("Arial", 24, "bold"), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Module tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Module 1: Smart Timetable
        self.timetable_frame = self.create_timetable_module()
        self.notebook.add(self.timetable_frame, text="📅 Smart Timetable")
        
        # Module 2: Job Assistant
        self.job_frame = self.create_job_module()
        self.notebook.add(self.job_frame, text="💼 Job Assistant")
        
    def create_timetable_module(self):
        frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        
        # Goals Section
        goals_section = tk.LabelFrame(frame, text="📋 Learning Goals", 
                                     font=("Arial", 14, "bold"), padx=10, pady=10)
        goals_section.pack(fill=tk.X, pady=(0, 20))
        
        # Add goal form
        goal_form = tk.Frame(goals_section)
        goal_form.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(goal_form, text="Goal:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.goal_entry = tk.Entry(goal_form, width=30)
        self.goal_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(goal_form, text="Duration (weeks):").grid(row=0, column=2, sticky='w', padx=(10, 5))
        self.duration_entry = tk.Entry(goal_form, width=10)
        self.duration_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(goal_form, text="Hours/day:").grid(row=0, column=4, sticky='w', padx=(10, 5))
        self.hours_entry = tk.Entry(goal_form, width=10)
        self.hours_entry.grid(row=0, column=5, padx=5)
        
        add_goal_btn = tk.Button(goal_form, text="Add Goal", command=self.add_goal,
                                bg='#3498db', fg='white', padx=15)
        add_goal_btn.grid(row=0, column=6, padx=10)
        
        # Goals list
        self.goals_listbox = tk.Listbox(goals_section, height=5)
        self.goals_listbox.pack(fill=tk.X, pady=5)
        
        # Fixed Events Section
        events_section = tk.LabelFrame(frame, text="📅 Fixed Events", 
                                      font=("Arial", 14, "bold"), padx=10, pady=10)
        events_section.pack(fill=tk.X, pady=(0, 20))
        
        # Add event form
        event_form = tk.Frame(events_section)
        event_form.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(event_form, text="Event:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.event_entry = tk.Entry(event_form, width=20)
        self.event_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(event_form, text="Day:").grid(row=0, column=2, sticky='w', padx=(10, 5))
        self.day_combo = ttk.Combobox(event_form, values=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], width=12)
        self.day_combo.grid(row=0, column=3, padx=5)
        
        tk.Label(event_form, text="Time:").grid(row=0, column=4, sticky='w', padx=(10, 5))
        self.time_entry = tk.Entry(event_form, width=15)
        self.time_entry.grid(row=0, column=5, padx=5)
        
        add_event_btn = tk.Button(event_form, text="Add Event", command=self.add_fixed_event,
                                 bg='#2ecc71', fg='white', padx=15)
        add_event_btn.grid(row=0, column=6, padx=10)
        
        # Events list
        self.events_listbox = tk.Listbox(events_section, height=4)
        self.events_listbox.pack(fill=tk.X, pady=5)
        
        # Generated Schedule Section
        schedule_section = tk.LabelFrame(frame, text="🗓️ Generated Schedule", 
                                        font=("Arial", 14, "bold"), padx=10, pady=10)
        schedule_section.pack(fill=tk.BOTH, expand=True)
        
        # Generate button
        generate_btn = tk.Button(schedule_section, text="🤖 Generate AI Schedule", 
                                command=self.generate_schedule,
                                bg='#e74c3c', fg='white', font=("Arial", 12, "bold"), pady=10)
        generate_btn.pack(pady=10)
        
        # Schedule display
        schedule_frame = tk.Frame(schedule_section)
        schedule_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for schedule
        columns = ('Day', 'Time', 'Task', 'Goal', 'Status')
        self.schedule_tree = ttk.Treeview(schedule_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=120)
        
        # Scrollbar for schedule
        schedule_scrollbar = ttk.Scrollbar(schedule_frame, orient=tk.VERTICAL, command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=schedule_scrollbar.set)
        
        self.schedule_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        schedule_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mark complete button
        mark_complete_btn = tk.Button(schedule_section, text="✅ Mark Selected as Complete", 
                                     command=self.mark_task_complete,
                                     bg='#27ae60', fg='white')
        mark_complete_btn.pack(pady=5)
        
        return frame
    
    def create_job_module(self):
        frame = tk.Frame(self.notebook, bg='white', padx=20, pady=20)
        
        # CV Upload Section
        cv_section = tk.LabelFrame(frame, text="📄 CV Management", 
                                  font=("Arial", 14, "bold"), padx=10, pady=10)
        cv_section.pack(fill=tk.X, pady=(0, 20))
        
        cv_frame = tk.Frame(cv_section)
        cv_frame.pack(fill=tk.X)
        
        upload_cv_btn = tk.Button(cv_frame, text="📎 Upload CV (PDF)", 
                                 command=self.upload_cv,
                                 bg='#3498db', fg='white', padx=20)
        upload_cv_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cv_status_label = tk.Label(cv_frame, text="No CV uploaded", fg='red')
        self.cv_status_label.pack(side=tk.LEFT)
        
        # CV Skills Display
        self.cv_skills_text = tk.Text(cv_section, height=4, wrap=tk.WORD)
        self.cv_skills_text.pack(fill=tk.X, pady=10)
        
        # Job Application Section
        job_section = tk.LabelFrame(frame, text="💼 Job Applications", 
                                   font=("Arial", 14, "bold"), padx=10, pady=10)
        job_section.pack(fill=tk.BOTH, expand=True)
        
        # Add application form
        app_form = tk.Frame(job_section)
        app_form.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(app_form, text="Company:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.company_entry = tk.Entry(app_form, width=20)
        self.company_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(app_form, text="Position:").grid(row=0, column=2, sticky='w', padx=(10, 5))
        self.position_entry = tk.Entry(app_form, width=25)
        self.position_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(app_form, text="Status:").grid(row=0, column=4, sticky='w', padx=(10, 5))
        self.status_combo = ttk.Combobox(app_form, values=['Applied', 'Interview', 'Rejected', 'Accepted'], width=12)
        self.status_combo.grid(row=0, column=5, padx=5)
        
        add_app_btn = tk.Button(app_form, text="Add Application", command=self.add_application,
                               bg='#9b59b6', fg='white', padx=15)
        add_app_btn.grid(row=0, column=6, padx=10)
        
        # Job description analysis
        jd_frame = tk.Frame(job_section)
        jd_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(jd_frame, text="Job Description:").pack(anchor='w')
        self.job_desc_text = tk.Text(jd_frame, height=6, wrap=tk.WORD)
        self.job_desc_text.pack(fill=tk.X, pady=(5, 10))
        
        analyze_btn = tk.Button(jd_frame, text="🔍 Analyze Match & Generate Cover Letter", 
                               command=self.analyze_job_match,
                               bg='#e67e22', fg='white', font=("Arial", 11, "bold"))
        analyze_btn.pack(pady=5)
        
        # Results display
        self.results_text = tk.Text(jd_frame, height=8, wrap=tk.WORD)
        self.results_text.pack(fill=tk.X, pady=10)
        
        # Applications list
        app_columns = ('Company', 'Position', 'Status', 'Date', 'Match %')
        self.app_tree = ttk.Treeview(job_section, columns=app_columns, show='headings', height=8)
        
        for col in app_columns:
            self.app_tree.heading(col, text=col)
            self.app_tree.column(col, width=100)
        
        self.app_tree.pack(fill=tk.X, pady=10)
        
        return frame
    
    def add_goal(self):
        goal = self.goal_entry.get().strip()
        duration = self.duration_entry.get().strip()
        hours = self.hours_entry.get().strip()
        
        if goal and duration and hours:
            try:
                duration_weeks = int(duration)
                daily_hours = float(hours)
                
                goal_data = {
                    'id': len(self.goals) + 1,
                    'title': goal,
                    'duration_weeks': duration_weeks,
                    'daily_hours': daily_hours,
                    'created_date': datetime.now().isoformat(),
                    'status': 'active'
                }
                
                self.goals.append(goal_data)
                self.goals_listbox.insert(tk.END, f"{goal} ({duration}w, {hours}h/day)")
                
                # Clear entries
                self.goal_entry.delete(0, tk.END)
                self.duration_entry.delete(0, tk.END)
                self.hours_entry.delete(0, tk.END)
                
                self.save_data()
                messagebox.showinfo("Success", "Goal added successfully!")
                
            except ValueError:
                messagebox.showerror("Error", "Duration and hours must be numbers!")
        else:
            messagebox.showerror("Error", "Please fill all fields!")
    
    def add_fixed_event(self):
        event = self.event_entry.get().strip()
        day = self.day_combo.get()
        time = self.time_entry.get().strip()
        
        if event and day and time:
            event_data = {
                'id': len(self.fixed_events) + 1,
                'title': event,
                'day': day,
                'time': time
            }
            
            self.fixed_events.append(event_data)
            self.events_listbox.insert(tk.END, f"{day} {time}: {event}")
            
            # Clear entries
            self.event_entry.delete(0, tk.END)
            self.day_combo.set('')
            self.time_entry.delete(0, tk.END)
            
            self.save_data()
            messagebox.showinfo("Success", "Fixed event added!")
        else:
            messagebox.showerror("Error", "Please fill all fields!")
    
    def generate_schedule(self):
        if not self.goals:
            messagebox.showwarning("Warning", "Please add some learning goals first!")
            return
        
        # Clear existing schedule
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        # Simple schedule generation logic (replace with AI later)
        self.schedule = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for goal in self.goals:
            if goal['status'] != 'active':
                continue
                
            # Distribute goal across the week
            sessions_per_week = 5  # 5 days per week
            for i in range(sessions_per_week):
                day = days[i % 7]
                
                # Check for conflicts with fixed events
                time_slot = self.find_available_time_slot(day)
                
                task_data = {
                    'id': len(self.schedule) + 1,
                    'day': day,
                    'time': time_slot,
                    'task': f"Study: {goal['title']}",
                    'goal': goal['title'],
                    'duration': goal['daily_hours'],
                    'status': 'pending'
                }
                
                self.schedule.append(task_data)
                
                # Add to treeview
                self.schedule_tree.insert('', tk.END, values=(
                    day, time_slot, task_data['task'], goal['title'], '⏳ Pending'
                ))
        
        self.save_data()
        messagebox.showinfo("Success", f"Generated schedule with {len(self.schedule)} tasks!")
    
    def find_available_time_slot(self, day):
        # Simple time slot allocation (9 AM to 6 PM)
        available_slots = ['09:00', '11:00', '14:00', '16:00', '18:00']
        
        # Check which slots are occupied by fixed events
        occupied_slots = []
        for event in self.fixed_events:
            if event['day'] == day:
                occupied_slots.append(event['time'])
        
        # Find first available slot
        for slot in available_slots:
            if slot not in occupied_slots:
                return slot
        
        return '20:00'  # Default late slot
    
    def mark_task_complete(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return
        
        item = selected[0]
        values = list(self.schedule_tree.item(item, 'values'))
        values[4] = '✅ Complete'
        self.schedule_tree.item(item, values=values)
        
        # Update in data
        day, time = values[0], values[1]
        for task in self.schedule:
            if task['day'] == day and task['time'] == time:
                task['status'] = 'complete'
                break
        
        self.save_data()
    
    def upload_cv(self):
        file_path = filedialog.askopenfilename(
            title="Select CV (PDF)",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            try:
                # Copy CV to user data directory
                cv_dest = self.data_dir / "cv.pdf"
                import shutil
                shutil.copy2(file_path, cv_dest)
                
                # Extract text from PDF
                cv_text = self.extract_pdf_text(file_path)
                
                # Simple skill extraction (replace with spaCy/NLP later)
                skills = self.extract_skills_simple(cv_text)
                
                self.cv_data = {
                    'file_path': str(cv_dest),
                    'text': cv_text,
                    'skills': skills,
                    'upload_date': datetime.now().isoformat()
                }
                
                self.cv_status_label.config(text="✅ CV uploaded successfully", fg='green')
                self.cv_skills_text.delete(1.0, tk.END)
                self.cv_skills_text.insert(1.0, f"Extracted Skills:\n{', '.join(skills)}")
                
                self.save_data()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload CV: {str(e)}")
    
    def extract_pdf_text(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract PDF text: {str(e)}")
            return ""
    
    def extract_skills_simple(self, text):
        # Simple keyword-based skill extraction
        common_skills = [
            'Python', 'Java', 'JavaScript', 'Go', 'Golang', 'C++', 'C#',
            'React', 'Angular', 'Vue', 'Node.js', 'Express',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
            'Git', 'Jenkins', 'CI/CD', 'DevOps',
            'Machine Learning', 'AI', 'Data Science', 'Pandas', 'NumPy'
        ]
        
        found_skills = []
        text_upper = text.upper()
        
        for skill in common_skills:
            if skill.upper() in text_upper:
                found_skills.append(skill)
        
        return found_skills
    
    def add_application(self):
        company = self.company_entry.get().strip()
        position = self.position_entry.get().strip()
        status = self.status_combo.get()
        
        if company and position and status:
            app_data = {
                'id': len(self.applications) + 1,
                'company': company,
                'position': position,
                'status': status,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'match_percentage': 0
            }
            
            self.applications.append(app_data)
            self.app_tree.insert('', tk.END, values=(
                company, position, status, app_data['date'], '0%'
            ))
            
            # Clear entries
            self.company_entry.delete(0, tk.END)
            self.position_entry.delete(0, tk.END)
            self.status_combo.set('')
            
            self.save_data()
            messagebox.showinfo("Success", "Application added!")
        else:
            messagebox.showerror("Error", "Please fill all fields!")
    
    def analyze_job_match(self):
        if not self.cv_data:
            messagebox.showwarning("Warning", "Please upload your CV first!")
            return
        
        job_desc = self.job_desc_text.get(1.0, tk.END).strip()
        if not job_desc:
            messagebox.showwarning("Warning", "Please enter job description!")
            return
        
        # Simple matching logic
        cv_skills = set(skill.lower() for skill in self.cv_data['skills'])
        
        # Extract required skills from job description
        job_skills = []
        for skill in ['python', 'java', 'aws', 'docker', 'kubernetes', 'terraform', 'react', 'node.js']:
            if skill in job_desc.lower():
                job_skills.append(skill)
        
        # Calculate match percentage
        if job_skills:
            matches = len(cv_skills.intersection(set(job_skills)))
            match_percentage = (matches / len(job_skills)) * 100
        else:
            match_percentage = 50  # Default if no specific skills found
        
        # Generate simple cover letter template
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my interest in the {self.position_entry.get() or '[Position]'} position at {self.company_entry.get() or '[Company]'}.

Based on my CV analysis, I have {matches if 'matches' in locals() else 'several'} relevant skills that match your requirements, including: {', '.join(cv_skills.intersection(set(job_skills)) if job_skills else list(cv_skills)[:5])}.

My background in software development and experience with cloud technologies make me a strong candidate for this role.

I would welcome the opportunity to discuss how my skills can contribute to your team.

Best regards,
[Your Name]"""
        
        # Display results
        results = f"MATCH ANALYSIS:\n"
        results += f"Match Percentage: {match_percentage:.1f}%\n"
        results += f"Your Skills: {', '.join(self.cv_data['skills'])}\n"
        results += f"Required Skills Found: {', '.join(job_skills)}\n\n"
        results += f"GENERATED COVER LETTER:\n{cover_letter}"
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
    
    def save_data(self):
        data = {
            'goals': self.goals,
            'schedule': self.schedule,
            'applications': self.applications,
            'cv_data': self.cv_data,
            'fixed_events': self.fixed_events
        }
        
        with open(self.data_dir / "studentlifeos_data.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        data_file = self.data_dir / "studentlifeos_data.json"
        if data_file.exists():
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                
                self.goals = data.get('goals', [])
                self.schedule = data.get('schedule', [])
                self.applications = data.get('applications', [])
                self.cv_data = data.get('cv_data', None)
                self.fixed_events = data.get('fixed_events', [])
                
            except Exception as e:
                print(f"Error loading data: {e}")

def main():
    # EXE compatibility fix
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        os.chdir(sys._MEIPASS)
    
    root = tk.Tk()
    app = StudentLifeOS(root)
    root.mainloop()

if __name__ == "__main__":
    main()