import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json

class HealthcareDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthcare Dashboard")
        self.root.geometry("600x500")
        
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#f3f4f6')
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Custom.TButton', padding=10)

        self.main_frame = ttk.Frame(root, style='Custom.TFrame', padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(
            self.main_frame,
            text="Patient Information Form",
            style='Header.TLabel'
        )
        header.pack(pady=(0, 20))

        self.form_frame = ttk.Frame(self.main_frame)
        self.form_frame.pack(fill=tk.X, padx=20)

        self.form_data = {
            'name': tk.StringVar(),
            'age': tk.StringVar(),
            'file_path': None
        }

        self.age_options = ['Select Age'] + [f"{i} years" for i in range(151)]

        self.create_form_fields()

    def create_form_fields(self):
        ttk.Label(self.form_frame, text="Patient Name:").pack(anchor=tk.W, pady=(0, 5))
        name_entry = ttk.Entry(
            self.form_frame,
            textvariable=self.form_data['name'],
            width=40
        )
        name_entry.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(self.form_frame, text="Age:").pack(anchor=tk.W, pady=(0, 5))
        age_dropdown = ttk.Combobox(
            self.form_frame,
            textvariable=self.form_data['age'],
            values=self.age_options,
            state='readonly',  
            width=37
        )
        age_dropdown.set('Select Age')  
        age_dropdown.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(self.form_frame, text="Medical Records:").pack(anchor=tk.W, pady=(0, 5))
        self.file_label = ttk.Label(self.form_frame, text="No file selected")
        self.file_label.pack(fill=tk.X, pady=(0, 5))
        
        upload_btn = ttk.Button(
            self.form_frame,
            text="Choose File",
            command=self.upload_file,
            style='Custom.TButton'
        )
        upload_btn.pack(fill=tk.X, pady=(0, 15))

        submit_btn = ttk.Button(
            self.form_frame,
            text="Submit Information",
            command=self.submit_form,
            style='Custom.TButton'
        )
        submit_btn.pack(fill=tk.X, pady=(20, 0))

    def upload_file(self):
        file_types = (
            ('PDF files', '*.pdf'),
            ('Document files', '*.doc;*.docx'),
            ('Image files', '*.jpg;*.png'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Upload Medical Records',
            filetypes=file_types
        )
        
        if filename:
            self.form_data['file_path'] = filename
            self.file_label.config(text=Path(filename).name)

    def submit_form(self):
        if not self.validate_form():
            return

        age_value = self.form_data['age'].get()
        age = age_value.split()[0] if age_value != 'Select Age' else None
        
        submission_data = {
            'name': self.form_data['name'].get(),
            'age': age,
            'file': str(self.form_data['file_path']) if self.form_data['file_path'] else None
        }

        print("Submitted data:", json.dumps(submission_data, indent=2))
        
        self.show_success_message()
        
        self.clear_form()

    def validate_form(self):
        if not self.form_data['name'].get():
            self.show_error("Please enter patient name")
            return False
            
        if self.form_data['age'].get() == 'Select Age':
            self.show_error("Please select an age")
            return False
            
        return True

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success_message(self):
        messagebox.showinfo(
            "Success",
            "Patient information submitted successfully!"
        )

    def clear_form(self):
        self.form_data['name'].set('')
        self.form_data['age'].set('Select Age')
        self.form_data['file_path'] = None
        self.file_label.config(text="No file selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareDashboard(root)
    root.mainloop()