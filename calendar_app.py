import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
from tkcalendar import Calendar

# Configuración de la base de datos
def setup_db():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, start_date TEXT, end_date TEXT, type TEXT)''')
    conn.commit()
    conn.close()

def add_event(title, start_date, end_date, event_type):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('INSERT INTO events (title, start_date, end_date, type) VALUES (?, ?, ?, ?)',
              (title, start_date, end_date, event_type))
    conn.commit()
    conn.close()

def view_events():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    events = c.fetchall()
    conn.close()
    return events

def cancel_event(event_id):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

def replace_event(event_id, title, start_date, end_date):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('UPDATE events SET title = ?, start_date = ?, end_date = ? WHERE id = ?',
              (title, start_date, end_date, event_id))
    conn.commit()
    conn.close()

# Validaciones
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def is_valid_event_type(event_type):
    return event_type in ['fixed', 'flexible']

def format_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%d/%m/%Y')
    except ValueError:
        return ''

def format_date_display(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%d/%m/%Y')
    except ValueError:
        return ''

# Interfaz gráfica
class CalendarApp:
    def __init__(self, root):
        self.root = root
        root.title("Simple Calendar App")

        self.setup_ui()
        self.update_calendar()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.title_label = ttk.Label(self.main_frame, text="Event Title:")
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.title_entry = ttk.Entry(self.main_frame)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.start_date_label = ttk.Label(self.main_frame, text="Start Date (dd/mm/yyyy):")
        self.start_date_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.start_date_entry = ttk.Entry(self.main_frame)
        self.start_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.end_date_label = ttk.Label(self.main_frame, text="End Date (dd/mm/yyyy):")
        self.end_date_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.end_date_entry = ttk.Entry(self.main_frame)
        self.end_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.type_label = ttk.Label(self.main_frame, text="Event Type (fixed/flexible):")
        self.type_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.type_entry = ttk.Entry(self.main_frame)
        self.type_entry.grid(row=3, column=1, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.add_button = ttk.Button(self.main_frame, text="Add Event", command=self.add_event)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.view_button = ttk.Button(self.main_frame, text="View Events", command=self.view_events)
        self.view_button.grid(row=5, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.cancel_button = ttk.Button(self.main_frame, text="Cancel Event", command=self.cancel_event)
        self.cancel_button.grid(row=6, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.replace_button = ttk.Button(self.main_frame, text="Replace Event", command=self.replace_event)
        self.replace_button.grid(row=7, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Calendar widget
        self.calendar = Calendar(self.root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.calendar.bind("<<CalendarSelected>>", self.update_calendar_view)

    def add_event(self):
        title = self.title_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        event_type = self.type_entry.get()

        if not title or not start_date or not end_date or not event_type:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        if not is_valid_date(start_date) or not is_valid_date(end_date):
            messagebox.showerror("Date Error", "Invalid date format. Use dd/mm/yyyy.")
            return

        if not is_valid_event_type(event_type):
            messagebox.showerror("Event Type Error", "Event type must be 'fixed' or 'flexible'.")
            return

        start_date = format_date(start_date)
        end_date = format_date(end_date)
        add_event(title, start_date, end_date, event_type)
        messagebox.showinfo("Info", "Event added successfully!")
        self.update_calendar()

    def view_events(self):
        events = view_events()
        view_window = tk.Toplevel(self.root)
        view_window.title("View Events")

        for event in events:
            event_label = ttk.Label(view_window, text=f"ID: {event[0]}, Title: {event[1]}, Start: {format_date_display(event[2])}, End: {format_date_display(event[3])}, Type: {event[4]}")
            event_label.pack(padx=10, pady=5)

    def cancel_event(self):
        event_id = simpledialog.askinteger("Cancel Event", "Enter the ID of the event to cancel:")
        if event_id:
            events = view_events()
            if any(event[0] == event_id for event in events):
                cancel_event(event_id)
                messagebox.showinfo("Info", "Event canceled successfully!")
                self.update_calendar()
            else:
                messagebox.showerror("Error", "Event ID not found.")

    def replace_event(self):
        event_id = simpledialog.askinteger("Replace Event", "Enter the ID of the event to replace:")
        if event_id:
            title = simpledialog.askstring("Replace Event", "Enter new title:")
            start_date = simpledialog.askstring("Replace Event", "Enter new start date (dd/mm/yyyy):")
            end_date = simpledialog.askstring("Replace Event", "Enter new end date (dd/mm/yyyy):")

            if not title or not start_date or not end_date:
                messagebox.showerror("Input Error", "All fields are required.")
                return

            if not is_valid_date(start_date) or not is_valid_date(end_date):
                messagebox.showerror("Date Error", "Invalid date format. Use dd/mm/yyyy.")
                return

            events = view_events()
            if any(event[0] == event_id for event in events):
                start_date = format_date(start_date)
                end_date = format_date(end_date)
                replace_event(event_id, title, start_date, end_date)
                messagebox.showinfo("Info", "Event replaced successfully!")
                self.update_calendar()
            else:
                messagebox.showerror("Error", "Event ID not found.")

    def update_calendar(self):
        self.calendar.calevent_remove("all")
        events = view_events()
        for event in events:
            try:
                start_date = datetime.strptime(event[2], '%d/%m/%Y').date()
                end_date = datetime.strptime(event[3], '%d/%m/%Y').date()
                if start_date == end_date:
                    self.calendar.calevent_create(start_date, event[1], 'event')
                else:
                    current_date = start_date
                    while current_date <= end_date:
                        self.calendar.calevent_create(current_date, event[1], 'event')
                        current_date += timedelta(days=1)
            except ValueError as e:
                print(f"Date parsing error: {e}")

    def update_calendar_view(self, event):
        selected_date = self.calendar.get_date()
        try:
            selected_date = datetime.strptime(selected_date, '%m/%d/%Y').date()
        except ValueError as e:
            messagebox.showerror("Date Error", f"Error parsing selected date: {e}")
            return

        events = view_events()
        event_details = [f"ID: {ev[0]}, Title: {ev[1]}, Start: {format_date_display(ev[2])}, End: {format_date_display(ev[3])}, Type: {ev[4]}"
                         for ev in events if datetime.strptime(ev[2], '%d/%m/%Y').date() == selected_date]

        view_window = tk.Toplevel(self.root)
        view_window.title("Events on Selected Date")
        if event_details:
            for detail in event_details:
                ttk.Label(view_window, text=detail).pack(padx=10, pady=5)
        else:
            ttk.Label(view_window, text="No events on this date.").pack(padx=10, pady=5)

if __name__ == "__main__":
    setup_db()
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
