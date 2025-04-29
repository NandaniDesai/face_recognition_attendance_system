import tkinter as tk
from tkinter import *
import os
import cv2
import numpy as np
from PIL import ImageTk, Image
from datetime import datetime
import time
import pyttsx3
import webbrowser
import pandas as pd
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF
from utils import text_to_speech

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def show_contact_info():
    contact_window = tk.Toplevel()
    contact_window.title("Contact Us")
    contact_window.geometry("600x500")
    contact_window.configure(bg="white")
    
    # Header
    header = tk.Frame(contact_window, bg="#E31937", height=60)
    header.pack(fill="x")
    
    title = tk.Label(
        header,
        text="Contact Information",
        font=("Arial", 20, "bold"),
        bg="#E31937",
        fg="white"
    )
    title.pack(pady=10)
    
    # Content
    content = tk.Frame(contact_window, bg="white")
    content.pack(fill="both", expand=True, pady=20)
    
    # Contact 1 - Hely Modi
    name1 = tk.Label(
        content,
        text="Hely Modi",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black"
    )
    name1.pack(anchor="w", padx=20, pady=(20,5))
    
    phone1 = tk.Label(
        content,
        text="Phone: 9724440822",
        font=("Arial", 12),
        bg="white",
        fg="#333333"
    )
    phone1.pack(anchor="w", padx=20)
    
    email1 = tk.Label(
        content,
        text="Email: ku2407u073@karnavatiuniversity.edu.in",
        font=("Arial", 12),
        bg="white",
        fg="#333333"
    )
    email1.pack(anchor="w", padx=20)
    
    # Separator
    tk.Frame(content, height=2, bg="#E0E0E0").pack(fill="x", padx=20, pady=15)
    
    # Contact 2 - Nandani Desai
    name2 = tk.Label(
        content,
        text="Nandani Desai",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black"
    )
    name2.pack(anchor="w", padx=20, pady=(15,5))
    
    phone2 = tk.Label(
        content,
        text="Phone: 6355547950",
        font=("Arial", 12),
        bg="white",
        fg="#333333"
    )
    phone2.pack(anchor="w", padx=20)
    
    email2 = tk.Label(
        content,
        text="Email: ku2407u144@karnavatiuniversity.edu.in",
        font=("Arial", 12),
        bg="white",
        fg="#333333"
    )
    email2.pack(anchor="w", padx=20)
    
    # Separator
    tk.Frame(content, height=2, bg="#E0E0E0").pack(fill="x", padx=20, pady=15)
    
    # Contact 3 - Riya Singh
    name3 = tk.Label(
        content,
        text="Riya Singh",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black"
    )
    name3.pack(anchor="w", padx=20, pady=(15,5))
    
    phone3 = tk.Label(
        content,
        text="Phone: 8160072201",
        font=("Arial", 12),
        bg="white",
        fg="#333333"
    )
    phone3.pack(anchor="w", padx=20)
    
    email3 = tk.Label(
        content,
        text="Email: ku2407u183@karnavatiuniversity.edu.in",
        font=("Arial", 12),
        bg="white",
        fg="#333333"
    )
    email3.pack(anchor="w", padx=20)

def export_to_pdf(df, subject):
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Add header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Attendance Report - {subject}', ln=True, align='C')
        pdf.ln(10)
        
        # Add date
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Date: {datetime.now().strftime("%Y-%m-%d")}', ln=True)
        pdf.ln(10)
        
        # Add table headers
        pdf.set_font('Arial', 'B', 12)
        cols = df.columns
        col_width = 190 / len(cols)  # Distribute width evenly
        for col in cols:
            pdf.cell(col_width, 10, str(col), 1)
        pdf.ln()
        
        # Add rows
        pdf.set_font('Arial', '', 10)
        for _, row in df.iterrows():
            for item in row:
                pdf.cell(col_width, 10, str(item), 1)
            pdf.ln()
        
        # Save PDF
        filename = f"Attendance/{subject}/attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        return filename
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create PDF: {str(e)}")
        return None

def send_to_whatsapp(file_path):
    try:
        # Create WhatsApp message with file path
        message = f"Attendance Report has been generated. File: {file_path}"
        # Format the WhatsApp URL with the encoded message
        whatsapp_url = f"https://wa.me/?text={message}"
        webbrowser.open(whatsapp_url)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open WhatsApp: {str(e)}")

def send_to_email(file_path):
    try:
        # Create email with file path
        subject = "Attendance Report"
        body = f"Please find the attendance report attached.\n\nFile location: {file_path}"
        # Format the mailto URL
        mailto_url = f"mailto:?subject={subject}&body={body}"
        webbrowser.open(mailto_url)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open email client: {str(e)}")

def create_attendance_graphs(df, frame):
    # Clear any existing widgets
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create notebook for different graphs
    notebook = ttk.Notebook(frame)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Daily Attendance Tab
    daily_tab = ttk.Frame(notebook)
    notebook.add(daily_tab, text="Daily Attendance")
    
    # Weekly Attendance Tab
    weekly_tab = ttk.Frame(notebook)
    notebook.add(weekly_tab, text="Weekly Summary")
    
    # Monthly Attendance Tab
    monthly_tab = ttk.Frame(notebook)
    notebook.add(monthly_tab, text="Monthly Overview")
    
    try:
        # Ensure we have a Date column
        if 'Date' not in df.columns:
            df['Date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Convert date strings to datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Daily Attendance Graph
        fig_daily = Figure(figsize=(8, 4))
        ax_daily = fig_daily.add_subplot(111)
        daily_attendance = df.groupby('Date').size()
        daily_attendance.plot(kind='bar', ax=ax_daily)
        ax_daily.set_title('Daily Attendance Count')
        ax_daily.set_xlabel('Date')
        ax_daily.set_ylabel('Number of Students')
        ax_daily.tick_params(axis='x', rotation=45)
        canvas_daily = FigureCanvasTkAgg(fig_daily, daily_tab)
        canvas_daily.draw()
        canvas_daily.get_tk_widget().pack(fill="both", expand=True)
        
        # Weekly Attendance Graph
        fig_weekly = Figure(figsize=(8, 4))
        ax_weekly = fig_weekly.add_subplot(111)
        df['Week'] = df['Date'].dt.strftime('%Y-W%U')
        weekly_attendance = df.groupby('Week').size()
        weekly_attendance.plot(kind='line', marker='o', ax=ax_weekly)
        ax_weekly.set_title('Weekly Attendance Trend')
        ax_weekly.set_xlabel('Week')
        ax_weekly.set_ylabel('Total Attendance')
        ax_weekly.tick_params(axis='x', rotation=45)
        canvas_weekly = FigureCanvasTkAgg(fig_weekly, weekly_tab)
        canvas_weekly.draw()
        canvas_weekly.get_tk_widget().pack(fill="both", expand=True)
        
        # Monthly Attendance Graph
        fig_monthly = Figure(figsize=(8, 4))
        ax_monthly = fig_monthly.add_subplot(111)
        df['Month'] = df['Date'].dt.strftime('%Y-%m')
        monthly_attendance = df.groupby('Month').size()
        monthly_attendance.plot(kind='bar', ax=ax_monthly)
        ax_monthly.set_title('Monthly Attendance Overview')
        ax_monthly.set_xlabel('Month')
        ax_monthly.set_ylabel('Total Attendance')
        ax_monthly.tick_params(axis='x', rotation=45)
        canvas_monthly = FigureCanvasTkAgg(fig_monthly, monthly_tab)
        canvas_monthly.draw()
        canvas_monthly.get_tk_widget().pack(fill="both", expand=True)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create graphs: {str(e)}")

def create_header_with_logo(parent, title_text):
    header = tk.Frame(parent, bg="#E31937", height=120)
    header.pack(fill="x")
    
    # Logo and title container
    logo_title_frame = tk.Frame(header, bg="#E31937")
    logo_title_frame.pack(pady=10)
    
    # Title only - skip logo to avoid errors
    title = tk.Label(
        logo_title_frame,
        text=title_text,
        font=("Arial", 24, "bold"),
        bg="#E31937",
        fg="white"
    )
    title.pack(side="left", padx=10)

def train_model():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = []
        ids = []
        
        # Process all images in TrainingImage directory
        for root, dirs, files in os.walk("TrainingImage"):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        # Get enrollment from directory name or file name
                        path_parts = os.path.normpath(root).split(os.sep)
                        if len(path_parts) > 1:
                            # Try to get enrollment from directory name first
                            enrollment = path_parts[-1].split('_')[0]
                            if not enrollment.isdigit():
                                # If directory name doesn't have valid enrollment, try from filename
                                enrollment = file.split('_')[0]
                        else:
                            # Try to get enrollment from filename
                            enrollment = file.split('_')[0]
                            
                        if not enrollment.isdigit():
                            continue
                            
                        img_path = os.path.join(root, file)
                        pil_img = Image.open(img_path).convert('L')
                        img_np = np.array(pil_img, 'uint8')
                        
                        faces_detected = detector.detectMultiScale(img_np)
                        for (x, y, w, h) in faces_detected:
                            faces.append(img_np[y:y+h, x:x+w])
                            ids.append(int(enrollment))
                            
                    except Exception as e:
                        print(f"Error processing image {file}: {str(e)}")
                        continue
        
        if not faces:
            text_to_speech("No valid faces found in training images!")
            return False
            
        # Create model directory if it doesn't exist
        os.makedirs("TrainingImageLabel", exist_ok=True)
        
        # Train and save the model
        recognizer.train(faces, np.array(ids))
        recognizer.save("TrainingImageLabel/Trainner.yml")
        
        text_to_speech("Model Trained Successfully!")
        return True
        
    except Exception as e:
        text_to_speech(f"Error during training: {str(e)}")
        return False

def show_attendance_stats(subject):
    try:
        # Read attendance files
        attendance_dir = f"Attendance/{subject}"
        if not os.path.exists(attendance_dir):
            messagebox.showerror("Error", "No attendance records found for this subject!")
            return
            
        # Create stats window
        stats_window = tk.Toplevel()
        stats_window.title(f"Attendance Statistics - {subject}")
        stats_window.geometry("1200x900")
        stats_window.configure(bg="white")
        
        # Create header with logo
        create_header_with_logo(stats_window, f"Attendance Statistics - {subject}")
        
        # Left section for table (40% width)
        table_frame = tk.Frame(stats_window, bg="white")
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Table Label
        table_label = tk.Label(
            table_frame,
            text="Attendance Records",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        table_label.pack(pady=(0, 10))
        
        # Create table
        tree = ttk.Treeview(table_frame)
        tree.pack(fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Read all CSV files
        all_files = [f for f in os.listdir(attendance_dir) if f.endswith('.csv')]
        if not all_files:
            messagebox.showinfo("Info", "No attendance records found!")
            return
            
        # Read the most recent file
        latest_file = max(all_files)
        df = pd.read_csv(os.path.join(attendance_dir, latest_file))
        
        # Add timestamp column if not exists
        if 'Timestamp' not in df.columns:
            df['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Configure columns
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        
        for column in tree["columns"]:
            tree.heading(column, text=column)
            tree.column(column, width=100)
        
        # Add data
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        
        # Right section for graphs and export (60% width)
        right_section = tk.Frame(stats_window, bg="white")
        right_section.pack(side="left", fill="both", expand=True)
        
        # Graphs section
        graphs_frame = tk.Frame(right_section, bg="white")
        graphs_frame.pack(fill="both", expand=True)
        
        # Graphs Label
        graphs_label = tk.Label(
            graphs_frame,
            text="Attendance Analytics",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        graphs_label.pack(pady=(0, 10))
        
        # Create graphs
        create_attendance_graphs(df, graphs_frame)
        
        # Export section with a visible border and title
        export_section = tk.LabelFrame(
            right_section,
            text="Export Options",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333333",
            padx=20,
            pady=10
        )
        export_section.pack(fill="x", pady=20)
        
        def export_pdf():
            file_path = export_to_pdf(df, subject)
            if file_path:
                messagebox.showinfo("Success", f"PDF exported successfully to {file_path}")
                return file_path
            return None
        
        def export_whatsapp():
            file_path = export_pdf()
            if file_path:
                send_to_whatsapp(file_path)
        
        def export_email():
            file_path = export_pdf()
            if file_path:
                send_to_email(file_path)
        
        # Export buttons with modern styling
        button_style = {
            "font": ("Arial", 12, "bold"),  # Made font bold
            "width": 25,
            "height": 2,
            "cursor": "hand2",
            "border": 0,
            "borderwidth": 0,
            "padx": 20,
            "pady": 5
        }
        
        # Button container for horizontal layout
        button_container = tk.Frame(export_section, bg="white")
        button_container.pack(fill="x", pady=10)
        
        # Export buttons with hover effect
        pdf_btn = tk.Button(
            button_container,
            text="📄  Export as PDF",
            command=export_pdf,
            bg="#4CAF50",
            fg="black",  # Changed to black
            **button_style
        )
        pdf_btn.pack(side="left", padx=5, expand=True)
        
        whatsapp_btn = tk.Button(
            button_container,
            text="📱  Share via WhatsApp",
            command=export_whatsapp,
            bg="#25D366",
            fg="black",  # Changed to black
            **button_style
        )
        whatsapp_btn.pack(side="left", padx=5, expand=True)
        
        email_btn = tk.Button(
            button_container,
            text="📧  Send via Email",
            command=export_email,
            bg="#DB4437",
            fg="black",  # Changed to black
            **button_style
        )
        email_btn.pack(side="left", padx=5, expand=True)
        
        # Add hover effects
        def on_enter(e):
            e.widget['background'] = e.widget.default_bg_dark
            e.widget['foreground'] = "white"  # Change text to white on hover
        
        def on_leave(e):
            e.widget['background'] = e.widget.default_bg
            e.widget['foreground'] = "black"  # Change text back to black
        
        # Configure hover colors for buttons
        pdf_btn.default_bg = "#4CAF50"
        pdf_btn.default_bg_dark = "#388E3C"
        whatsapp_btn.default_bg = "#25D366"
        whatsapp_btn.default_bg_dark = "#1EA952"
        email_btn.default_bg = "#DB4437"
        email_btn.default_bg_dark = "#C53929"
        
        for btn in [pdf_btn, whatsapp_btn, email_btn]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to show attendance: {str(e)}")

def create_modern_button(parent, text, command, x, y, width=None):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#000000",  # Dark black text
        relief="groove",
        cursor="hand2",
        pady=10,
        activebackground="#f0f0f0",
        activeforeground="#000000",  # Keep text dark when button is pressed
        border=2
    )
    if width:
        btn.configure(width=width)
    btn.place(x=x, y=y)
    return btn

def create_card(parent, title, description, button_text, command, x, y):
    card = tk.Frame(
        parent,
        bg="white",
        relief="raised",
        width=350,
        height=160,
        borderwidth=1
    )
    card.place(x=x, y=y)
    card.pack_propagate(False)
    
    accent = tk.Frame(card, bg="#E31937", height=4)
    accent.pack(fill="x", side="top")
    
    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#000000"  # Dark black text
    )
    title_label.pack(anchor="w", padx=20, pady=(10,5))
    
    desc_label = tk.Label(
        card,
        text=description,
        font=("Arial", 11),
        bg="white",
        fg="#000000"  # Dark black text
    )
    desc_label.pack(anchor="w", padx=20)
    
    btn = tk.Button(
        card,
        text=button_text,
        command=command,
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#000000",  # Dark black text
        relief="groove",
        cursor="hand2",
        pady=8,
        padx=20,
        activebackground="#f0f0f0",
        activeforeground="#000000",  # Keep text dark when button is pressed
        border=2
    )
    btn.pack(pady=10)

    # Add hover effect
    def on_enter(e):
        e.widget['background'] = '#f0f0f0'
    
    def on_leave(e):
        e.widget['background'] = 'white'
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def main_window():
    root = tk.Tk()
    root.title("Karnavati University - Face Recognition Attendance System")
    root.geometry("1200x720")
    root.configure(bg="white")
    
    # Create header with logo
    create_header_with_logo(root, "KARNAVATI UNIVERSITY")
    
    content = tk.Frame(root, bg="white")
    content.pack(fill="both", expand=True, pady=20)
    
    def launch_registration():
        try:
            import subprocess
            import sys
            subprocess.run([sys.executable, 'takeImage.py'], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch registration: {str(e)}")
    
    create_card(
        content,
        "Register New Student",
        "Add new student data to train the face recognition model.",
        "Register New Student",
        launch_registration,  # Using the new launch function
        80, 20
    )
    
    create_card(
        content,
        "Train Model",
        "Train face recognition model with newly registered student data.",
        "Train Model",
        train_model,  # Using our fixed train_model function
        450, 20
    )
    
    create_card(
        content,
        "Take Attendance",
        "Start face recognition to mark student attendance for a subject.",
        "Take Attendance",
        lambda: os.system('python3 automaticAttedance.py'),
        820, 20
    )
    
    def view_attendance_dialog():
        dialog = tk.Toplevel()
        dialog.title("Enter Subject")
        dialog.geometry("400x200")
        dialog.configure(bg="white")
        
        tk.Label(
            dialog,
            text="Enter Subject Name:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black"
        ).pack(pady=20)
        
        subject_entry = tk.Entry(
            dialog,
            font=("Arial", 12),
            width=30
        )
        subject_entry.pack(pady=10)
        
        def submit():
            subject = subject_entry.get()
            if subject:
                dialog.destroy()
                show_attendance_stats(subject)
            else:
                messagebox.showwarning("Warning", "Please enter a subject name!")
        
        tk.Button(
            dialog,
            text="View Attendance",
            command=submit,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black",
            relief="groove"
        ).pack(pady=20)
    
    create_card(
        content,
        "View Attendance",
        "View and analyze recorded attendance data with detailed statistics.",
        "View Attendance",
        view_attendance_dialog,
        250, 220
    )
    
    create_card(
        content,
        "Contact Us",
        "Get in touch with us for any queries or support.",
        "Contact Us",
        show_contact_info,
        650, 220
    )
    
    # Footer frame
    footer_frame = tk.Frame(root, bg="white", height=100)
    footer_frame.pack(side="bottom", fill="x", pady=20)
    
    # Website link as a prominent button
    def open_ku_website():
        webbrowser.open("https://karnavatiuniversity.edu.in")
    
    visit_button = tk.Button(
        footer_frame,
        text="🌐  Visit Karnavati University",
        command=open_ku_website,
        font=("Arial", 14, "bold"),
        fg="black",
        bg="#f0f0f0",
        activebackground="#e0e0e0",
        activeforeground="black",
        cursor="hand2",
        relief="raised",
        border=2,
        padx=30,
        pady=10
    )
    visit_button.pack(pady=10)
    
    # Add hover effect
    def on_enter(e):
        visit_button['background'] = '#e0e0e0'
    
    def on_leave(e):
        visit_button['background'] = '#f0f0f0'
    
    visit_button.bind("<Enter>", on_enter)
    visit_button.bind("<Leave>", on_leave)
    
    # Website text link
    website_link = tk.Label(
        footer_frame,
        text="www.karnavatiuniversity.edu.in",
        font=("Arial", 11),
        bg="white",
        fg="#666666",
        cursor="hand2"
    )
    website_link.pack(pady=5)
    website_link.bind("<Button-1>", lambda e: open_ku_website())
    
    root.mainloop()

if __name__ == "__main__":
    main_window()
