import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
from time import strftime
from tkcalendar import DateEntry
import re
import datetime


# File path
file_path = "C:\\Users\\ahmed\\Desktop\\Schedule_Project\\SQL.txt"

# Read lines from the file and assign to variables
with open(file_path, "r") as file:
    variables = [line.strip() for line in file]

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host=variables[0], user=variables[1], password=variables[2], database=variables[3]
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Create a Tkinter window
window = tk.Tk()
window.title("Teaching Schedule")
window.geometry("1400x930")

# Add the rowheight
ttk.Style().theme_use("clam")
ttk.Style().configure("Treeview", font=("Times New Roman ", 10), rowheight=80)

# Create a Treeview widget
tree = ttk.Treeview(window, columns=("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"),height=7)

# Format the columns
tree.column("#0", width=0, stretch=tk.NO)  # Hide the first (default) column
for day, heading in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
    tree.column(day, anchor=tk.W)
    tree.heading(day, text=heading)

# Pack the Treeview widget
tree.grid(row=0, column=0, columnspan=7, padx=10, pady=10)

# Create payment frames
money_frame = tk.Frame(window)
money_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

money_month_frame = tk.Frame(window)
money_month_frame.grid(row=1, column=4, columnspan=2, padx=10, pady=10)

# Create labels for total hours and total money (weekly)
weekly_label = ttk.Label(money_frame, text="Weekly Hours", font=("Times New Roman", 15), foreground="Black")
weekly_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

total_hours_label = ttk.Label(money_frame, text="Total Hours Worked: ", font=("Times New Roman", 12), foreground="brown")
total_hours_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

total_money_label = ttk.Label(money_frame, text="Total Expected Money: $", font=("Times New Roman", 12), foreground="brown")
total_money_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")

paid_label = ttk.Label(money_frame, text="Total Received Money: $", font=("Times New Roman", 12), foreground="brown")
paid_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="w")

expected_label = ttk.Label(money_frame, text="Expected Payment: $", font=("Times New Roman", 12), foreground="brown")
expected_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="w")

# Create labels for total hours and total money (monthly)
monthly_label = ttk.Label(money_month_frame, text="Monthly Hours", font=("Times New Roman", 15), foreground="Black")
monthly_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

total_hours_label_month = ttk.Label(money_month_frame, text="Total Hours Worked: ", font=("Times New Roman", 12), foreground="brown")
total_hours_label_month.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

total_money_label_month = ttk.Label(money_month_frame, text="Total Expected Money: $", font=("Times New Roman", 12), foreground="brown")
total_money_label_month.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")

paid_label_month = ttk.Label(money_month_frame, text="Total Received Money: $", font=("Times New Roman", 12), foreground="brown")
paid_label_month.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="w")

expected_label_month = ttk.Label(money_month_frame, text="Expected Payment: $", font=("Times New Roman", 12), foreground="brown")
expected_label_month.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="w")

# Create a calendar frame
calendar_frame = tk.Frame(window)
calendar_frame.grid(row=1, column=2, columnspan=3, padx=10, pady=10)

# Create a calendar widget
cal = Calendar(calendar_frame, selectmode="day", date_pattern="yyyy-mm-dd", font="Arial 10")
cal.pack(pady=5)


def filter_classes():
    selected_date = cal.get_date()
    selected_datetime = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
    start_date = selected_datetime - datetime.timedelta(days=selected_datetime.weekday())
    end_date = start_date + datetime.timedelta(days=6)

    query = "SELECT * FROM teaching_schedule WHERE date BETWEEN %s AND %s"   
    cursor.execute(query, (start_date.date(), end_date.date()))

    teaching_schedule_data = cursor.fetchall()

    tree.delete(*tree.get_children())

    schedule_data = {day: [] for day in range(7)}

    for row in teaching_schedule_data:
        class_id, class_name, date, starttime, endtime, school, rate, paid = row[:8]
        paid = paid.upper() + " !! " if paid.lower() == "no" else paid.upper()

        day = (date.weekday()) % 7
        schedule_data[day].append((class_id, class_name, date, starttime, endtime, school, rate, paid))

    for day in range(7):
        schedule_data[day].sort(key=lambda x: x[3])

    for row in range(max(len(schedule_data[day]) for day in range(7))):
        values = []

        for day in range(7):
            if row < len(schedule_data[day]):
                class_id, class_name, date, starttime, endtime, school, rate, paid = schedule_data[day][row]
                formatted_date = date.strftime("%d-%m-%y")
                values.append(f"{class_id}~{class_name}~{school}\n{formatted_date} | {starttime} | {endtime}\n{paid}\n{rate}")
            else:
                values.append("")
        tree.insert("", index=tk.END, text="", values=values)

    calculate_totals()
    
    # Get the column names
    columns = tree['columns']
    
    # Get the column names
    columns = tree['columns']

class_name_entry = None
date_entry = None
start_hour_spinbox = None
start_minute_spinbox = None
end_hour_spinbox = None
end_minute_spinbox = None
school_entry = None
rate_entry = None
new_class_window = None
calculate_window = None

def open_new_class_window():
    def submit_new_class():
        class_name = entry_variables[0].get()
        date = entry_variables[1].get_date().strftime("%Y-%m-%d")
        start_time = f"{entry_variables[2].get().zfill(2)}:{entry_variables[3].get().zfill(2)}:00"
        end_time = f"{entry_variables[4].get().zfill(2)}:{entry_variables[5].get().zfill(2)}:00"
        school = entry_variables[6].get()
        rate = entry_variables[7].get()

        insert_query = "INSERT INTO teaching_schedule (class, date, starttime, endtime, school, rate) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (class_name, date, start_time, end_time, school, rate))
        connection.commit()

        messagebox.showinfo("New Class", "Class has been added successfully.")

        new_class_window.destroy()

        filter_classes()

    new_class_window = tk.Toplevel(window)
    new_class_window.title("New Class")
    new_class_window.geometry("300x300")

    entry_labels = [
        "Class Name",
        "Date",
        "Start Hour",
        "Start Minute",
        "End Hour",
        "End Minute",
        "School",
        "Rate",
    ]
    entry_variables = [
        None,  # Placeholder for class_name_entry
        None,  # Placeholder for date_entry
        None,  # Placeholder for start_hour_spinbox
        None,  # Placeholder for start_minute_spinbox
        None,  # Placeholder for end_hour_spinbox
        None,  # Placeholder for end_minute_spinbox
        None,  # Placeholder for school_entry
        None,  # Placeholder for rate_entry
    ]

    row = 0
    row2 = 0
    for label_text, entry_variable in zip(entry_labels, entry_variables):
        if "Minute" in label_text:
            pass
        elif "Hour" in label_text:
            label = tk.Label(new_class_window, text=label_text.split(" ", 1)[0] + " Time :")
            label.grid(row=row, column=0, padx=10, pady=10)
        else:
            label = tk.Label(new_class_window, text=label_text + ":")
            label.grid(row=row, column=0, padx=10, pady=10)

        if "Date" in label_text:
            entry_variable = DateEntry(
                new_class_window,
                width=12,
                date_pattern="yyyy-mm-dd",
                font="Arial 12"
            )
            entry_variable.set_date(datetime.datetime.now().date())
            entry_variable.grid(row=row, column=1, columnspan=3, padx=10, pady=10)
            
        elif "Hour" in label_text or "Minute" in label_text:
            if "Minute" in label_text:
                row -=1
            entry_variable = tk.Spinbox(
                new_class_window,
                from_=0,
                to=23,
                width=4,
                wrap=True
            )
            entry_variable.grid(
                row=row,
                column=1 if "Hour" in label_text else 2,
                padx=10,
                pady=10
            )

        else:
            entry_variable = tk.StringVar()  # Create a StringVar for class_name_entry
            entry = tk.Entry(
                new_class_window,
                textvariable=entry_variable
            )
            entry.grid(row=row, column=1, columnspan=3, padx=10, pady=10)

        entry_variables[row2] = entry_variable
        row += 1
        row2 +=1

    submit_button = tk.Button(
        new_class_window,
        text="Submit",
        command=submit_new_class
    )
    submit_button.grid(row=row, column=0, columnspan=4, padx=10, pady=10)


def calculate_hours():
    global calculate_window
    calculate_window = tk.Toplevel(window)
    calculate_window.title("Calculate Hours")
    calculate_window.geometry("400x300")

    # Create a label and combobox for selecting the month
    month_label = tk.Label(calculate_window, text="Select Month:")
    month_label.pack()

    month_var = tk.StringVar()
    month_combobox = ttk.Combobox(
        calculate_window, textvariable=month_var, state="readonly"
    )
    month_combobox["values"] = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )
    month_combobox.pack(pady=5)

    query = "SELECT DISTINCT school FROM teaching_schedule"
    cursor.execute(query)
    schools = cursor.fetchall()

    school_var = tk.StringVar()
    school_combobox = ttk.Combobox(
        calculate_window, textvariable=school_var, state="readonly"
    )
    school_combobox["values"] = schools
    school_combobox.pack(pady=5)

    # Create a button to calculate the hours
    calculate_button = tk.Button(
        calculate_window,
        text="Calculate",
        command=lambda: calculate_hours_worked(month_var.get(), school_var.get()),
    )
    calculate_button.pack(pady=10)

total_monthly_hours = None
avg_rate_label = None
salary_label = None

def calculate_hours_worked(selected_month, selected_school):
    global total_monthly_hours, avg_rate_label, salary_label, calculate_window

    # Extract the month from the selected month string
    month_number = datetime.datetime.strptime(selected_month, "%B").month

    # Perform SQL query to fetch classes from the selected month and school
    query = "SELECT * FROM teaching_schedule WHERE MONTH(date) = %s AND school = %s"
    cursor.execute(query, (month_number, selected_school))
    classes = cursor.fetchall()

    total_hours = 0

    # Calculate total hours worked
    for class_data in classes:
        start_time = class_data[3]
        end_time = class_data[4]

        # Calculate the difference in hours between start and end times
        hours_worked = (end_time - start_time).total_seconds() / 3600
        total_hours += hours_worked
        total_hours = round(total_hours, 2)

    # Update the total monthly hours label
    if total_monthly_hours:
        total_monthly_hours[
            "text"
        ] = f"Total Hours Worked in {selected_month}: {total_hours} hours"
    else:
        total_monthly_hours = tk.Label(
            calculate_window,
            text=f"Total Hours Worked in {selected_month}: {total_hours} hours",
        )
        total_monthly_hours.pack(pady=10)

    # Calculate the average rate (if applicable)
    avg_rate = int(classes[0][-2]) if classes else 0

    # Update the average rate label
    if avg_rate_label:
        avg_rate_label["text"] = f"The Average Rate is {avg_rate}.000 /1hr"
    else:
        avg_rate_label = tk.Label(
            calculate_window, text=f"The Average Rate is {avg_rate}.000 /1hr"
        )
        avg_rate_label.pack(pady=10)

    # Calculate the salary
    salary = avg_rate * total_hours * 1000

    # Update the salary label
    if salary_label:
        salary_label[
            "text"
        ] = f"The salary of {selected_month} from {selected_school} is {salary:,} VND"
    else:
        salary_label = tk.Label(
            calculate_window,
            text=f"The salary of {selected_month} from {selected_school} is {salary:,} VND",
        )
        salary_label.pack(pady=10)


def copy_classes():
    def get_classes():
        selected_date = calendar.get_date()
        selected_datetime = datetime.datetime.strptime(selected_date, "%m/%d/%y")
        start_date = selected_datetime - datetime.timedelta(
            days=selected_datetime.weekday()
        )
        end_date = start_date + datetime.timedelta(days=6)
        query = "SELECT * FROM teaching_schedule WHERE date >= %s AND date <= %s"
        cursor.execute(query, (start_date.date(), end_date.date()))
        classes = cursor.fetchall()
        display_classes(classes)

    def display_classes(classes):
        for i, class_info in enumerate(classes):
            class_name = class_info[0:5]
            class_checkbox = ttk.Checkbutton(class_frame, text=class_name)
            class_checkbox.grid(row=i + 2, column=0, sticky="nsew")
            class_checkboxes.append((class_info, class_checkbox))

    def copy_selected_classes():
        selected_date = calendar.get_date()
        selected_datetime = datetime.datetime.strptime(selected_date, "%m/%d/%y")
        start_date = selected_datetime - datetime.timedelta(
            days=selected_datetime.weekday()
        )
        end_date = start_date + datetime.timedelta(days=6)
        selected_classes = []
        for class_info, checkbox in class_checkboxes:
            if checkbox.instate(["selected"]):
                selected_classes.append(class_info)
        copy_to_second_week(selected_classes, start_date, end_date)
        new_window.destroy()

    def copy_to_second_week(classes, start_date, end_date):
        for class_info in classes:
            *_, class_name, date, start_time, end_time, school, rate, paid = class_info
            class_date_str = date.strftime(
                "%Y-%m-%d"
            )  # Convert the date to string format
            class_date = datetime.datetime.strptime(class_date_str, "%Y-%m-%d")
            day_difference = (class_date - start_date).days
            new_date = start_date + datetime.timedelta(
                days=day_difference + 7
            )  # Add 7 days to the original class date
            new_date_str = new_date.strftime(
                "%Y-%m-%d"
            )  # Convert the new date to string format
            query = "INSERT INTO teaching_schedule (class, date, starttime, endtime, school, rate) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(
                query, (class_name, new_date_str, start_time, end_time, school, rate)
            )
            # Commit the changes to the database
            connection.commit()

    new_window = tk.Toplevel()
    new_window.title("Copy Weeks")
    new_window.geometry("400x600")

    canvas = tk.Canvas(new_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(new_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    class_frame = ttk.Frame(canvas)

    calendar_frame = ttk.Frame(class_frame)
    calendar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    calendar = Calendar(calendar_frame, selectmode="day")
    calendar.pack()

    button_frame = ttk.Frame(class_frame)
    button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    get_classes_button = ttk.Button(
        button_frame, text="Get Classes", command=get_classes
    )
    get_classes_button.pack(side=tk.LEFT, padx=5)

    copy_classes_button = ttk.Button(
        button_frame, text="Copy", command=copy_selected_classes
    )
    copy_classes_button.pack(side=tk.LEFT, padx=5)

    class_frame.grid_columnconfigure(0, weight=1)

    class_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=class_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Bind mouse wheel events to the canvas for scrolling
    canvas.bind(
        "<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
    )

    class_checkboxes = []


def calculate_totals():
    selected_date = cal.get_date()
    selected_date_obj = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
    month = selected_date_obj.month

    total_hours = 0
    total_money = 0
    received_money = 0
    expected_money = 0
    
    start_date = selected_date_obj - datetime.timedelta(
        days=selected_date_obj.weekday()
    )
    end_date = start_date + datetime.timedelta(days=6)
    query = "SELECT * FROM teaching_schedule WHERE date >= %s AND date <= %s"

    cursor.execute(query, (start_date.date(), end_date.date()))
    classes = cursor.fetchall()

    # Calculate total hours worked and total expected money
    for class_data in classes:
        start_time = class_data[3]
        end_time = class_data[4]
        money = class_data[-2]

        # Calculate the difference in hours between start and end times
        hours_worked = (end_time - start_time).total_seconds() / 3600
        total_hours += hours_worked
        total_money += int(money) * hours_worked

        if class_data[-1] == "yes":
            received_money += int(money) * hours_worked
        else:
            expected_money += int(money) * hours_worked

    total_money = int(total_money * 1000)
    received_money = int(received_money * 1000)
    expected_money = int(expected_money * 1000)
    total_hours = round(total_hours, 2)

    # Update the labels with the calculated values
    total_hours_label.config(text=f"Total Hours: {total_hours}")
    total_money_label.config(text=f"Total Salary: {total_money:,} VND")
    paid_label.config(text=f"Received Salary: {received_money:,} VND")
    expected_label.config(text=f" Expected Salary: {expected_money:,} VND")
    
    total_hours_month = 0
    total_money_month = 0
    received_money_month = 0
    expected_money_month = 0

    query = "SELECT * FROM teaching_schedule WHERE month(date) = %s"
    cursor.execute(query, (month,))
    classes2 = cursor.fetchall()

    # Calculate total hours worked and total expected money
    for class_data in classes2:
        start_time = class_data[3]
        end_time = class_data[4]
        money_month = class_data[-2]

        # Calculate the difference in hours between start and end times
        hours_worked_month = (end_time - start_time).total_seconds() / 3600
        total_hours_month += hours_worked_month
        total_money_month += int(money_month) * hours_worked_month

        if class_data[-1] == "yes":
            received_money_month += int(money_month) * hours_worked_month
        else:
            expected_money_month += int(money_month) * hours_worked_month

    total_money_month = int(total_money_month * 1000)
    received_money_month = int(received_money_month * 1000)
    expected_money_month = int(expected_money_month * 1000)
    total_hours_month = round(total_hours_month, 2)

    # Update the labels with the calculated values
    total_hours_label_month.config(text=f"Total Hours: {total_hours_month}")
    total_money_label_month.config(text=f"Total Salary: {total_money_month:,} VND")
    paid_label_month.config(text=f"Received Salary: {received_money_month:,} VND")
    expected_label_month.config(text=f" Expected Salary: {expected_money_month:,} VND")


def db_info_update():
    db_info_window = tk.Toplevel(window)
    db_info_window.title("Connection Settings")
    db_info_window.geometry("300x300")

    # Create and pack the labels and entry widgets for each variable
    labels = ["Host Name:", "Username:", "Password:", "Database Name:"]
    entries = []

    for i, label_text in enumerate(labels):
        label = tk.Label(db_info_window, text=label_text, font=("Times New Roman ", 10))
        label.pack(pady=5)

        entry = tk.Entry(db_info_window, font=("Times New Roman ", 10))
        entry.insert(tk.END, variables[i])
        entry.pack(pady=5)

        entries.append(entry)

    def save_variables():
        # Save the modified variables to the file
        with open(file_path, "w") as file:
            for entry in entries:
                variable = entry.get()
                file.write(variable + "\n")

        db_info_window.destroy()
        messagebox.showinfo("Success", "Settings updated successfully.")

    # Create and pack the save button
    save_button = tk.Button(
        db_info_window,
        text="Save",
        command=save_variables,
        font=("Times New Roman ", 10),
    )
    save_button.pack(pady=5)


def open_info_window(event):
    def duplicate_classes(class_id):
        # Create a new window for editing
        duplicate_window = tk.Toplevel(window)
        duplicate_window.title("Duplicate Class")
        duplicate_window.geometry("300x400")
           
        if class_info:
            fields = [
                ("Class Name", class_info[1]),
                ("Date", class_info[2]),
                ("Start Hour", re.split(r":", str(class_info[3]))[0]),
                ("Start Minute", re.search(r":(.*?):", str(class_info[3])).group(1)),
                ("End Hour", re.split(r":", str(class_info[4]))[0]),
                ("End Minute", re.search(r":(.*?):", str(class_info[4])).group(1)),
                ("School", class_info[5]),
                ("Rate", class_info[6])
            ]

            entries = []
            row = 0

            for label_text, value in fields:
                if "Minute" in label_text:
                    pass
                elif "Hour" in label_text:
                    label = tk.Label(duplicate_window, text=label_text.split(" ", 1)[0] + " Time :")
                    label.grid(row=row, column=0, padx=10, pady=10)
                else:
                    label = tk.Label(duplicate_window, text=label_text + ":")
                    label.grid(row=row, column=0, padx=10, pady=10)

                if "Date" in label_text:
                    entry_variable = DateEntry(
                        duplicate_window,
                        width=12,
                        date_pattern="yyyy-mm-dd",
                        font="Arial 12"
                    )
                    entry_variable.set_date(datetime.datetime.now().date())
                    entry_variable.grid(row=row, column=1, columnspan=3, padx=10, pady=10)
                    entry_variable.set_date(value)
                    entries.append(entry_variable)
                elif "Hour" in label_text or "Minute" in label_text:
                    spinbox = tk.Spinbox(duplicate_window, from_=0, to=23 if "Hour" in label_text else 59, width=4, wrap=True)
                    spinbox.delete(0, tk.END)
                    spinbox.insert(0, value)
                    if "Minute" in label_text:
                        row -= 1
                    spinbox.grid(row=row, column=1 if "Hour" in label_text else 2, padx=10, pady=10)
                    entries.append(spinbox)
                else:
                    entry = tk.Entry(duplicate_window)
                    entry.insert(tk.END, value)
                    entry.grid(row=row, column=1, columnspan=3, padx=10, pady=10)
                    entries.append(entry)

                row += 1

            paid_label = tk.Label(duplicate_window, text="Rate:")
            paid_label.grid(row=row, column=0, padx=10, pady=10)

            paid_var = ["yes", "no"]
            paid_combobox = ttk.Combobox(duplicate_window, state="readonly")
            paid_combobox["values"] = paid_var
            paid_combobox.current(paid_var.index("no"))
            paid_combobox.grid(row=row, column=1, padx=10, pady=10, columnspan=2)
            entries.append(paid_combobox)

            def duplicate_new_class():
                values = []
                for entry in entries:
                    if isinstance(entry, tk.Entry) or isinstance(entry, DateEntry):
                        values.append(entry.get())
                    elif isinstance(entry, tk.Spinbox):
                        values.append(entry.get())
                    else:
                        values.append(entry.get())
                start_time = f"{values[2].zfill(2)}:{values[3].zfill(2)}:00"
                end_time = f"{values[4].zfill(2)}:{values[5].zfill(2)}:00"
                query = "INSERT INTO teaching_schedule (class, date, starttime, endtime, school, rate, paid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (values[0], values[1], start_time, end_time, values[6], values[7], values[8]))
                connection.commit()

                # Close the edit window
                duplicate_window.destroy()

                # Refresh the class schedule display
                filter_classes()

            # Create and pack the update button
            duplicate_button = tk.Button(
                duplicate_window, text="Duplicate", command=duplicate_new_class
            )
            duplicate_button.grid(row=8, column=0, columnspan=3, padx=10, pady=10)
        else:
            messagebox.showerror("Error", "Invalid Class ID")


    def edit_class(id):
        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Class")
        edit_window.geometry("300x400")

        if class_info:
            fields = [
                ("Class Name", class_info[1]),
                ("Date", class_info[2]),
                ("Start Hour", re.split(r":", str(class_info[3]))[0]),
                ("Start Minute", re.search(r":(.*?):", str(class_info[3])).group(1)),
                ("End Hour", re.split(r":", str(class_info[4]))[0]),
                ("End Minute", re.search(r":(.*?):", str(class_info[4])).group(1)),
                ("School", class_info[5]),
                ("Rate", class_info[6])
            ]

            entries = []
            row = 0

            for label_text, value in fields:
                if "Minute" in label_text:
                    pass
                elif "Hour" in label_text:
                    label = tk.Label(edit_window, text=label_text.split(" ", 1)[0] + " Time :")
                    label.grid(row=row, column=0, padx=10, pady=10)
                else:
                    label = tk.Label(edit_window, text=label_text + ":")
                    label.grid(row=row, column=0, padx=10, pady=10)

                if "Date" in label_text:
                    entry_variable = DateEntry(
                        edit_window,
                        width=12,
                        date_pattern="yyyy-mm-dd",
                        font="Arial 12"
                    )
                    entry_variable.set_date(datetime.datetime.now().date())
                    entry_variable.grid(row=row, column=1, columnspan=3, padx=10, pady=10)
                    entry_variable.set_date(value)
                    entries.append(entry_variable)
                elif "Hour" in label_text or "Minute" in label_text:
                    spinbox = tk.Spinbox(edit_window, from_=0, to=23 if "Hour" in label_text else 59, width=4, wrap=True)
                    spinbox.delete(0, tk.END)
                    spinbox.insert(0, value)
                    if "Minute" in label_text:
                        row -= 1
                    spinbox.grid(row=row, column=1 if "Hour" in label_text else 2, padx=10, pady=10)
                    entries.append(spinbox)
                else:
                    entry = tk.Entry(edit_window)
                    entry.insert(tk.END, value)
                    entry.grid(row=row, column=1, columnspan=3, padx=10, pady=10)
                    entries.append(entry)

                row += 1

            paid_label = tk.Label(edit_window, text="Rate:")
            paid_label.grid(row=row, column=0, padx=10, pady=10)

            paid_var = ["yes", "no"]
            paid_combobox = ttk.Combobox(edit_window, state="readonly")
            paid_combobox["values"] = paid_var
            paid_combobox.current(paid_var.index(class_info[7])) if class_info[7] in paid_var else None
            paid_combobox.grid(row=row, column=1, padx=10, pady=10, columnspan=2)
            entries.append(paid_combobox)

            def update_class():
                values = []
                for entry in entries:
                    if isinstance(entry, tk.Entry) or isinstance(entry, DateEntry):
                        values.append(entry.get())
                    elif isinstance(entry, tk.Spinbox):
                        values.append(entry.get())
                    else:
                        values.append(entry.get())
                start_time = f"{values[2].zfill(2)}:{values[3].zfill(2)}:00"
                end_time = f"{values[4].zfill(2)}:{values[5].zfill(2)}:00"
                query = "UPDATE teaching_schedule SET class = %s, date = %s, starttime = %s, endtime = %s, school = %s, rate = %s, paid = %s WHERE id = %s"
                cursor.execute(query, (values[0], values[1], start_time, end_time, values[6], values[7], values[8], id))
                connection.commit()
                edit_window.destroy()
                filter_classes()

            update_button = tk.Button(edit_window, text="Update", command=update_class)
            update_button.grid(row=row + 1, column=0, columnspan=3, padx=10, pady=10)

        else:
            messagebox.showerror("Error", "Invalid Class ID")
            
    def delete(class_id):
        try:
            response = messagebox.askyesno(
                "Class Information",
                message,
                detail="Do you want to edit the class information?",
            )
            if response:
                # Execute the DELETE query
                delete_query = "DELETE FROM teaching_schedule WHERE id = %s"
                cursor.execute(delete_query, (class_id,))
                connection.commit()
    
        except mysql.connector.Error as error:
            # Display an error message
            messagebox.showerror("Class Deletion", f"Error deleting class: {error}")
    
        filter_classes()
        
    def edit(class_id):
        response = messagebox.askyesno(
            "Class Information",
            message,
            detail="Do you want to edit the class information?",
        )

        if response:
            edit_class(class_id)
            
    def payment(class_id):
        try:
            if class_info[7] == "yes":
                response = messagebox.askyesno(
                    "Class Information",
                    message,
                    detail="Do you want to edit the class payment as 'NO' ?",
                )
                if response:
                    # Execute the DELETE query
                    update_query = "UPDATE teaching_schedule SET paid = %s WHERE id = %s"
                    cursor.execute(update_query, ("no",class_id))
                    connection.commit()
            else:
                response = messagebox.askyesno(
                    "Class Information",
                    message,
                    detail="Do you want to edit the class payment as 'YES' ?",
                )
                if response:
                    # Execute the DELETE query
                    update_query = "UPDATE teaching_schedule SET paid = %s WHERE id = %s"
                    cursor.execute(update_query, ("yes",class_id))
                    connection.commit()
               
            filter_classes()
        except mysql.connector.Error as error:
            # Display an error message
            messagebox.showerror("Class Update", f"Error updating class: {error}")
        
    item = tree.identify("item", event.x, event.y)
    column = tree.identify("column", event.x, event.y)
    if item and column:
        item_text = tree.item(item, "text")
        cell_value = tree.set(item, column)
        class_id = re.split(r"~", cell_value)[0]
        
        # Fetch the class information from the database based on the class ID
        query = "SELECT * FROM teaching_schedule WHERE id = %s"
        cursor.execute(query, (class_id,))
        class_info = cursor.fetchone()
        
        # Format the date as DD/MM/YYYY
        formatted_date = class_info[2].strftime("%d/%m/%Y")

        # Create a single message with the values
        message = (
            f"\u2022 Class ID: {class_info[0]}\n"
            f"\u2022 Class Name: {class_info[1]}\n"
            f"\u2022 Date: {formatted_date}\n"
            f"\u2022 Start Time: {str(class_info[3])}\n"
            f"\u2022 End Time: {str(class_info[4])}\n"
            f"\u2022 School: {class_info[5]}\n"
            f"\u2022 Rate: {str(class_info[6])}\n"
            f"\u2022 Paid: {str(class_info[7].capitalize())}"
        )
        
        menu = tk.Menu(window, tearoff=0)
        menu.add_command(label="Details", command=lambda: edit(class_id))
        menu.add_command(label="Delete", command=lambda: delete(class_id))
        menu.add_command(label="Edit", command=lambda: edit_class(class_id))
        menu.add_command(label="Duplicate", command=lambda: duplicate_classes(class_id))
        menu.add_command(label="Un/Paid", command=lambda: payment(class_id))
        menu.post(event.x_root, event.y_root)

filter_classes()

# Create a button to filter classes for the selected week
filter_button = tk.Button(window, text="Filter", command=filter_classes, width=10, height=2)
filter_button.grid(row=2, column=2, columnspan=3, padx=10, pady=10)

# Create a menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Connection Settings", command=db_info_update)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)

# Create "Edit" menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Add options to "Edit" menu
edit_menu.add_command(label="New Class (F1)", command=open_new_class_window)
edit_menu.add_separator()
edit_menu.add_command(label="Copy Classes(F4)", command=copy_classes)
edit_menu.add_separator()
edit_menu.add_command(label="Calculate Hours(F10)", command=calculate_hours)

# Bind key events
key_events = [
    ("<F5>", filter_classes),
    ("<F1>", open_new_class_window),
    ("<F4>", copy_classes),
    ("<F10>", calculate_hours)
]

for event, command in key_events:
    window.bind(event, lambda e, cmd=command: cmd())

tree.bind("<Button-3>", open_info_window)


# Start the Tkinter event loop
window.mainloop()
