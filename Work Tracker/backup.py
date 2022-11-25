from tkinter import *
from tkinter.ttk import *
from tkinter import Menu
from tkinter import messagebox

import time
from datetime import datetime
import math
import re
import uuid

#---------------------Startup-------------------------------------
log_file_location = "D:\\Raphael\\Python\\Code\\Work Tracker\\log.txt"
project_file_location = "D:\\Raphael\\Python\\Code\\Work Tracker\\projects.txt"

#log_file_location = "log.txt"
#project_file_location = "projects.txt"

#---------------------Variables-------------------------------------
comment_focus = 0
playing = False
reset_counter = 0

timings = []
current_time = []
total_time = 0
num_minutes = 0

current_date = None

time_error = False

list_log = []
tree = Treeview

#projects_combo = Combobox
hours_spin = Spinbox
min_spin = Spinbox
comment_entry = Entry
date_entry = Entry

record_selected = False
record_selected_delete = False
selected_item_list = []
list_log_2 = []
list_log_3 = []
edit_list_log = []
selected_records_delete = []
new_log = []
delete_id = []

all_projects = []
all_projects_ids = []
all_projects_og = []
temporary_data = []

filter_value_global = 'All'
action = 'add'

btn_press_count = 0


#---------------------Functions-------------------------------------


def load_projects():
    global all_projects
    global all_projects_og
    global all_projects_ids

    del all_projects[:]
    del all_projects_og[:]
    del all_projects_ids[:]

    with open(project_file_location) as project_file:
        file = project_file.readlines()[0]
        for i in file.split(',*|*,'):
            all_projects.append(i.split(",|, ")[0])
            all_projects_og.append(i.split(",|, ")[0])
            all_projects_ids.append(i.split(",|, "))
        del all_projects[-1]
        del all_projects_ids[-1]
        del all_projects_og[-1]



def take_focus():
    global comment_focus
    if comment_focus <= 0:
        comment.delete('0', 'end')
        comment.config(foreground = "black")
        comment_focus += 1


def generate_id():
    new_id = uuid.uuid4()
    known_ids = []
    id_records = []
    with open(log_file_location, "r") as log:
        txt_log = log.readlines()
        if len(txt_log) > 0:
            for record in txt_log[0].split(",*|*,"):
                id_records.append(record.split(",|, "))
            del id_records[-1]

    for i in id_records:
        known_ids.append(i[4])

    for i in all_projects_ids:
        known_ids.append(i[1])

    while new_id in known_ids:
        new_id = uuid.uuid4()

    return new_id


def check_files():
    try:
        f_read = open(project_file_location, "r")
        f_read.close()

    except:
        f_write = open(project_file_location, "w")
        f_write.close()

    f_read = open(project_file_location, "r")
    line = f_read.readlines()
    if len(line) < 1:
        f_write = open(project_file_location, "w")
        f_write.write("First Project,|, 11a11a1a-1aa1-1aa1-1111-a1aaa111a1a,*|*,")
        f_write.close()
    f_read.close()

    #-------------------------------------------------------------------------------

    try:
        f_read = open(log_file_location, "r")
        f_read.close()

    except:
        f_write = open(log_file_location, "w")
        f_write.close()

    f_read = open(log_file_location, "r")
    line = f_read.readlines()
    if len(line) < 1:
        f_write = open(log_file_location, "w")
        f_write.write("First Project,|, 30,|, Example record (delete this),|, 01/01/2000,|, 22b22b2b-2bb2-2bb2-2222-b2bbb222b2b,*|*,")
        f_write.close()
    f_read.close()

check_files()
load_projects()


def start_timer():
    global playing
    global current_time
    global timings
    global current_date

    if not playing:  #When timer starts
        global current_date

        playing = True
        start_btn.config(text = "II")
        current_time.append(time.time())

        if len(timings) == 0:
            current_date = datetime.today().strftime('%d/%m/%Y')

        projects.grid_remove()
        comment.grid_remove()
        submit_btn.grid_remove()
        error_message.grid_remove()
        reset_btn.grid_remove()
        if time_error:
            error_message.grid_remove()

    else:  #When timer stops
        playing = False
        start_btn.config(text = "▶")
        current_time.append(time.time())
        timings.append(current_time)
        current_time = []

        projects.grid()
        comment.grid()
        submit_btn.grid()
        reset_btn.grid()
        if time_error:
            error_message.grid()


def submit():
    global total_time
    global error_message
    global time_error
    global comment_focus

    inputted_project = projects.get()
    inputted_comment = comment.get()
    if comment_focus == 0:
        inputted_comment = ""

    if num_minutes >= 1:
        log_file = open(log_file_location, 'a')
        log_file.write(inputted_project
                       + ',|, ' + str(num_minutes)
                       + ',|, ' + inputted_comment
                       + ',|, ' + str(current_date)
                       + ',|, ' + str(generate_id())
                       + ',*|*,')
        log_file.close()

        reset()

    else:
        time_error = True
        error_message.grid()


def button_reset():
    global reset_counter

    if reset_counter < 1:
        reset_btn.config(text = "Sure?")
        reset_counter += 1

    else:
        reset_counter = 0
        reset_btn.config(text = "Reset")
        reset()


def reset():
    global total_time
    global comment_focus
    global timings

    timings = []
    comment.delete('0', 'end')
    comment.config(foreground = "grey")
    comment.insert(0, "Type comment here")
    time_lbl.config(text = "00:00")
    comment_focus = 0


def update():
    global total_time
    global num_minutes

    total_time = 0
    window.after(1000, update)
    for section in timings:
        total_time += section[1] - section[0]

    if playing:
        total_time += time.time() - current_time[0]

    minutes = math.floor(total_time / 60)
    if minutes < 1:
        submit_btn.configure(state = "disabled")

    else:
        submit_btn.configure(state = "enabled")

    num_minutes = minutes  #get total minutes

    hours = math.floor(minutes / 60)
    minutes = minutes % 60

    minutes = f"{minutes:02}"
    hours = f"{hours:02}"

    time_lbl.config(text = hours + ":" + minutes)


def display_log():
    global win_log

    def reload_projects():
        load_projects()

        filter_projects_combo['values'] = ("All",)
        for project1 in all_projects:
            filter_projects_combo['values'] += (project1,)

        projects_combo['values'] = all_projects
        projects_combo.current(0)

        projects_combo_edit['values'] = ("- Add New -",)
        for project in all_projects:
            projects_combo_edit['values'] += (project,)
        projects_combo_edit.current(0)

        try:
            projects['values'] = all_projects
            projects.current(0)
        except:
            pass

    def delete_project():
        global btn_press_count

        if btn_press_count == 0:
            delete_project_button.configure(text = 'Sure?')
            btn_press_count = 1

        else:
            if len(all_projects_ids) > 1:
                del temporary_data[:]
                for i in all_projects_ids:
                    if i[1] != current_id:
                        temporary_data.append(i)

                with open(project_file_location, "w") as f:
                    for data in temporary_data:
                        f.write(data[0]
                                + ',|, ' + data[1]
                                + ',*|*,')

            else:
                messagebox.showwarning("Deletion of Project", "You must have at least one project!\nPlease create a new project first before trying again.")

            edit_project_entry.delete('0', 'end')
            reload_projects()

            delete_project_button.configure(text = 'Delete Project')
            btn_press_count = 0

    def add_edit_projects(new_value):
        global temporary_data
        global current_id

        if action == "add":
            with open(project_file_location, "a") as f:
                f.write(new_value + ",|, " + str(generate_id()) + ",*|*,")

        elif action == "edit":
            temporary_data = []
            for i in all_projects_ids:
                if i[1] != current_id:
                    temporary_data.append(i)
                else:
                    temporary_data.append([new_value, current_id])

            with open(project_file_location, "w") as f:
                for data in temporary_data:
                    f.write(data[0]
                                   + ',|, ' + data[1]
                                   + ',*|*,')
        edit_project_entry.delete('0', 'end')
        current_id = None
        reload_projects()

    def set_pro_combo(position, length):
        global action
        global current_id

        win_log.focus()
        if position > 0:
            current_id = all_projects_ids[position-1][1]
            edit_project_entry.delete('0', 'end')
            edit_project_entry.insert(0, all_projects_ids[position-1][0])
            edit_add_project_button.configure(text = "Edit Project")
            action = "edit"

        else:
            current_id = generate_id()
            edit_project_entry.delete('0', 'end')
            edit_add_project_button.configure(text = "Add Project")
            action = "add"

    def filter_projects(element, filter_value):
        global filter_value_global

        element.focus()
        for item in tree.get_children():
            tree.delete(item)

        reload_log(filter_value)
        filter_value_global = filter_value

    win_log = Tk()
    win_log.title("Show Log")
    win_log.resizable(False, False)

    extra_lines = 3
    #all_projects.insert(0, "All")

    edit_window = LabelFrame(win_log, text = "Edit/Add Record")
    edit_window.grid(row = extra_lines + 2, column = 0, padx = 5, pady = 10, sticky = 'W')

    project_window = LabelFrame(win_log, text = "Edit/Add Projects")
    project_window.grid(row = extra_lines + 3, column = 0, padx = 5, pady = 10, sticky = 'WE')

    delete_button_style = Style()
    delete_button_style.configure('d.TButton', font = ('Arial', 12), foreground = "red")

    def delete_record():
        global record_selected_delete
        global selected_records_delete
        global delete_id
        global new_log
        global list_log_3
        global filter_projects_combo

        new_log = []
        selected_records_delete = []
        list_log_3 = []

        if not record_selected_delete:
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                selected_records_delete = [item["text"]]
                for i in item['values']:
                    selected_records_delete.append(i)

                delete_id.append(selected_records_delete[4])

                delete_btn.configure(text = "Sure?")
                record_selected_delete = True

        else:
            with open(log_file_location, "r") as log:
                txt_log = log.readlines()
                if len(txt_log) > 0:
                    for split_record in txt_log[0].split(",*|*,"):
                        list_log_3.append(split_record.split(",|, "))
                    del list_log_3[-1]

                for i in list_log_3:
                    if i[4] not in delete_id:
                        new_log.append(i)

            log_file = open(log_file_location, "w")
            text_to_write = ""
            for record in new_log:
                text_to_write += (record[0]
                                  + ',|, ' + str(record[1])
                                  + ',|, ' + str(record[2])
                                  + ',|, ' + str(record[3])
                                  + ',|, ' + str(record[4])
                                  + ',*|*,')
            log_file.write(text_to_write)
            log_file.close()
            reload_log(filter_value_global)
            delete_btn.configure(text = "Delete Record")
            record_selected_delete = False

    def add_record():
        inputted_project = projects_combo.get()
        inputted_hours = hours_spin.get()
        inputted_minutes = min_spin.get()
        inputted_comment = comment_entry.get()
        inputted_date = date_entry.get()
        if inputted_date == '':
            inputted_date = str(datetime.today().strftime('%d/%m/%Y'))

        log_file = open(log_file_location, "a")
        log_file.write(inputted_project + ",|, " + str(int(inputted_hours * 60) + int(
            inputted_minutes)) + ",|, " + inputted_comment + ",|, " + inputted_date + ",|, " + str(
            generate_id()) + ",*|*,")
        log_file.close()
        reload_log(filter_value_global)

    def edit_record():
        global record_selected
        global selected_item_list

        if not record_selected:
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                selected_item_list = [item["text"]]
                for i in item['values']:
                    selected_item_list.append(i)

                comment_entry.delete(0, END)
                date_entry.delete(0, END)

                split_time = re.split('hr |min', selected_item_list[1])
                del split_time[-1]
                selected_item_list[1] = split_time

                projects_combo.set(selected_item_list[0])
                hours_spin.set(selected_item_list[1][0])
                min_spin.set(selected_item_list[1][1])
                comment_entry.insert(0, selected_item_list[2])
                date_entry.insert(0, selected_item_list[3])
                edit_btn.configure(text = "Update Record")
                record_selected = True

        else:
            global list_log_2
            global edit_list_log
            edit_list_log = []
            list_log_2 = []

            with open(log_file_location, "r") as log:
                txt_log = log.readlines()
                if len(txt_log) > 0:
                    for split_record in txt_log[0].split(",*|*,"):
                        list_log_2.append(split_record.split(",|, "))
                    del list_log_2[-1]

            for record_value in list_log_2:
                if record_value[4] == selected_item_list[4]:
                    edit_list_log.append(
                        [projects_combo.get(), (int(hours_spin.get()) * 60) + int(min_spin.get()), comment_entry.get(),
                         date_entry.get(), selected_item_list[4]])

                else:
                    edit_list_log.append(record_value)

            log_file = open(log_file_location, "w")
            text_to_write = ""
            for record in edit_list_log:
                text_to_write += (record[0]
                                  + ',|, ' + str(record[1])
                                  + ',|, ' + str(record[2])
                                  + ',|, ' + str(record[3])
                                  + ',|, ' + str(record[4])
                                  + ',*|*,')
            log_file.write(text_to_write)
            log_file.close()

            record_selected = False
            edit_btn.configure(text = "Edit Record")

            comment_entry.delete(0, END)
            date_entry.delete(0, END)
            hours_spin.set("00")
            min_spin.set("00")
            projects_combo.set('')
            reload_log(filter_value_global)

    filter_window = Frame(win_log)
    filter_window.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = 'W')

    filter_lbl = Label(filter_window, text = "Filter:", font = ("Arial Bold", 12))
    filter_lbl.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = "W")

    filter_projects_combo = Combobox(filter_window, width = 19, font = text_font, state = "readonly")
    filter_projects_combo.option_add('*TCombobox*Listbox.font', text_font)

    filter_projects_combo['values'] = ("All",)
    for project in all_projects:
        filter_projects_combo['values'] += (project,)

    filter_projects_combo.current(0)
    filter_projects_combo.grid(column = 1, row = 0, padx = 5, pady = 3, sticky = "W")
    filter_projects_combo.bind("<<ComboboxSelected>>", lambda e: filter_projects(win_log, filter_projects_combo.get()))

    add_btn = Button(filter_window, text = "Add Record", takefocus = False, width = 17, style = 'my.TButton',
                     command = add_record)
    add_btn.grid(column = 2, row = 0, padx = 7, pady = 3)

    edit_btn = Button(filter_window, text = "Edit Record", takefocus = False, width = 17, style = 'my.TButton',
                      command = edit_record)
    edit_btn.grid(column = 3, row = 0, padx = 7, pady = 3)

    delete_btn = Button(filter_window, text = "Delete Record", takefocus = False, width = 17, style = 'd.TButton',
                        command = delete_record)
    delete_btn.grid(column = 4, row = 0, padx = 7, pady = 3)

    export_btn = Button(filter_window, text = "Export", takefocus = False, width = 17, style = 'my.TButton',
                      command = edit_record) #TODO Add export command
    export_btn.grid(column = 5, row = 0, padx = 7, pady = 3)

    sep = Separator(win_log, orient = 'horizontal')
    sep.grid(row = 1, column = 0, ipadx = 200, pady = 10, sticky = "EW", columnspan = 5)

    def reload_log(filter_value):
        global list_log

        list_log = []
        with open(log_file_location, "r") as log:
            txt_log = log.readlines()
            if len(txt_log) > 0:
                for record in txt_log[0].split(",*|*,"):
                    list_log.append(record.split(",|, "))
                del list_log[-1]
            headings = ("Time", "Comment", "Date", "ID")

            for record in list_log:
                value_num = 0
                for value in record:
                    if value_num == 1:
                        number = int(value)
                        hours = math.floor(number / 60)
                        minutes = number % 60
                        record[value_num] = (str(hours) + "hr " + str(minutes) + "min")

                    value_num += 1

            global tree
            tree = Treeview(win_log)
            tree.configure(columns = headings, displaycolumns = (0, 1, 2))

            tree.heading("#0", text = "Project")
            tree.heading("Time", text = "Time")
            tree.heading("Comment", text = "Comment")
            tree.heading("Date", text = "Date")
            tree.heading("ID", text = "ID")

            tree.column("#0", width = 150, minwidth = 150, stretch = False)
            tree.column("Time", width = 100, minwidth = 100)
            tree.column("Comment", width = 250, minwidth = 200)
            tree.column("Date", width = 100, minwidth = 100)
            tree.heading("ID", text = "ID")

            for record in list_log:
                if filter_value == "All" or filter_value == record[0]:
                    tree.insert('', END, text = record[0], values = record[1:])

            tree.grid(row = extra_lines, column = 0, sticky = 'nsew', padx = 5, pady = 5, columnspan = 5)

            scrollbar = Scrollbar(win_log, orient = VERTICAL, command = tree.yview)
            tree.configure(yscroll = scrollbar.set)
            scrollbar.grid(row = extra_lines, column = 5, sticky = 'ns', columnspan = 5)

        #-------------------
        time_log = []
        total_hours_sum = 0

        if len(txt_log) > 0:
            for record in txt_log[0].split(",*|*,"):
                try:
                    time_log.append(record.split(",|, ")[0:2])
                except:
                    pass
            del time_log[-1]

        for item in time_log:
            if filter_value == "All" or filter_value == item[0]:
                total_hours_sum += int(item[1])

        hours_total = math.floor(total_hours_sum / 60)
        minutes_total = total_hours_sum % 60

        minutes_total = f"{minutes_total:02}"
        hours_total = f"{hours_total:02}"

        str_time = (hours_total + ":" + minutes_total)

        total_hours = Frame(win_log)
        total_hours.grid(row = extra_lines + 1, column = 0, padx = 5, pady = 10, sticky = 'W')

        total_hours_lbl = Label(total_hours, text = "Total time:", font = ("Arial Bold", 12))
        total_hours_lbl.grid(column = 0, row = 0, padx = 5, sticky = "W")

        total_hours_time = Label(total_hours, text = str(str_time), font = ("Roboto Mono", 13))
        total_hours_time.grid(column = 1, row = 0, padx = 5, sticky = "W")

        #-------------------

        project_lbl = Label(edit_window, text = "Project", font = ("Arial Bold", 11))
        project_lbl.grid(column = 0, row = 0, padx = 5, pady = 3, sticky = "W")

        time_spent_lbl = Label(edit_window, text = "Time", font = ("Arial Bold", 11))
        time_spent_lbl.grid(column = 1, row = 0, padx = 5, pady = 3, sticky = "W", columnspan = 4)

        comment_lbl = Label(edit_window, text = "Comment", font = ("Arial Bold", 11))
        comment_lbl.grid(column = 5, row = 0, padx = 5, pady = 3, sticky = "W")

        date_lbl = Label(edit_window, text = "Date", font = ("Arial Bold", 11))
        date_lbl.grid(column = 6, row = 0, padx = 5, pady = 3, sticky = "W")

        #-------------------

        global projects_combo
        global hours_spin
        global min_spin
        global comment_entry
        global date_entry
        global projects_combo_edit

        projects_combo = Combobox(edit_window, width = 17, font = text_font, state = "readonly")
        projects_combo.option_add('*TCombobox*Listbox.font', text_font)
        projects_combo['values'] = all_projects
        projects_combo.current(0)
        projects_combo.grid(column = 0, row = 2, padx = 5, pady = 3, sticky = "W")

        hours_spin = Spinbox(edit_window, from_ = 00, to = 24, width = 3, state = "readonly",
                             font = ("Roboto Mono", 11), format = "%02.0f")
        hours_spin.set("00")
        hours_spin.grid(column = 1, row = 2)

        colon_lbl = Label(edit_window, text = ":", font = ("Arial Bold", 13))
        colon_lbl.grid(column = 2, row = 2, padx = 5, pady = 3, sticky = "W")

        min_spin = Spinbox(edit_window, from_ = 00, to = 59, width = 3, state = "readonly", font = ("Roboto Mono", 11),
                           format = "%02.0f", wrap = True)
        min_spin.set("00")
        min_spin.grid(column = 3, row = 2)

        comment_entry = Entry(edit_window, width = 40, font = text_font)
        comment_entry.grid(column = 5, row = 2, padx = 5, pady = 3)

        date_entry = Entry(edit_window, width = 18, font = text_font)
        date_entry.grid(column = 6, row = 2, padx = 5, pady = 3)

        #-------------------

    reload_log("All")

    help_lbl = Label(project_window, text = "Select a project to rename or select '- Add New -' to add a new project", font = ("Arial", 10))
    help_lbl.grid(column = 0, row = 0, padx = 5, pady = 3, sticky = "W", columnspan = 10)

    project_lbl_edit = Label(project_window, text = "Project", font = ("Arial Bold", 11))
    project_lbl_edit.grid(column = 0, row = 1, padx = 5, pady = 3, sticky = "W")

    projects_combo_edit = Combobox(project_window, width = 17, font = text_font, state = "readonly")
    projects_combo_edit.option_add('*TCombobox*Listbox.font', text_font)

    projects_combo_edit['values'] = ("- Add New -",)
    for project in all_projects:
        projects_combo_edit['values'] += (project,)
    projects_combo_edit.current(0)

    edit_project_edit = Label(project_window, text = "Name", font = ("Arial Bold", 11))
    edit_project_edit.grid(column = 1, row = 1, padx = 5, pady = 3, sticky = "W")

    edit_project_entry = Entry(project_window, width = 18, font = text_font)
    edit_project_entry.grid(column = 1, row = 2, padx = 5, pady = 3)

    edit_add_project_button = Button(project_window, text = "Add Project", takefocus = False, width = 20, style = 'my.TButton', command = lambda: add_edit_projects(edit_project_entry.get()))
    edit_add_project_button.grid(column = 2, row = 2, padx = 5)

    delete_project_button = Button(project_window, text = "Delete Project", takefocus = False, width = 20,
                                     style = 'my.TButton',
                                     command = lambda: delete_project())
    delete_project_button.grid(column = 3, row = 2, padx = 5)

    projects_combo_edit.grid(column = 0, row = 2, padx = 5, pady = 3, sticky = "W")
    projects_combo_edit.bind("<<ComboboxSelected>>",
                             lambda e: set_pro_combo(projects_combo_edit.current(), len(all_projects)))


#---------------------Window Config---------------------------------

window = Tk()
window.title("")
window.resizable(False, False)
window.attributes('-topmost', True)
#window.wm_attributes('-toolwindow', True)

text_font = ("Arial", 10)

submit_button = Style()
submit_button.configure('my.TButton', font = text_font)

reset_button = Style()
reset_button.configure('r.TButton', font = text_font, foreground = "red")

start_btn = Button(window, text = "▶", takefocus = False, command = start_timer, style = 'my.TButton')
start_btn.grid(column = 0, row = 1, padx = 5, pady = 5, sticky = "W")

time_lbl = Label(window, text = "00:00", font = ("Roboto Mono", 15))
time_lbl.grid(column = 1, row = 1, padx = 5, pady = 5, sticky = "E")

projects = Combobox(window, width = 19, font = text_font, state = "readonly")
projects.option_add('*TCombobox*Listbox.font', text_font)
projects['values'] = all_projects
projects.current(0)
projects.grid(column = 0, row = 2, padx = 5, pady = 3, columnspan = 2, sticky = "WE")
projects.bind("<<ComboboxSelected>>", lambda e: window.focus())

comment = Entry(window, width = 21, font = text_font, foreground = "grey")
comment.grid(column = 0, row = 3, padx = 5, pady = 3, columnspan = 2, sticky = "WE")
comment.insert(0, "Type comment here")
comment.bind("<FocusIn>", lambda args: take_focus())

submit_btn = Button(window, text = "Submit", takefocus = False, width = 21, style = 'my.TButton', command = submit)
submit_btn.grid(column = 0, row = 4, padx = 5, pady = 3, sticky = "WE", columnspan = 2)

reset_btn = Button(window, text = "Reset", takefocus = False, width = 21, style = 'r.TButton', command = button_reset)
reset_btn.grid(column = 0, row = 5, padx = 5, pady = 3, sticky = "WE", columnspan = 2)

error_message = Label(window, text = "Work for at least 5 minutes", font = text_font, foreground = 'red')
error_message.grid(column = 0, row = 6, padx = 5, pady = 3, sticky = "WE", columnspan = 2)
error_message.grid_remove()

update()

menu = Menu(window)
open_window = Menu(menu, tearoff=0)
open_window.add_command(label='Log', command=display_log)
menu.add_cascade(label='Open', menu=open_window)
window.config(menu=menu)

window.mainloop()
