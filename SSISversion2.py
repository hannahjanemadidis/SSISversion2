from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import messagebox

top = Tk()
top.title("STUDENT INFORMATION SYSTEM")
top.geometry("1000x400")
top.config(bg = 'black')
top.resizable(False, False)
top.overrideredirect(True)
top.attributes('-alpha', 0.0)

def main():
    root = Tk()
    root.title("STUDENT INFORMATION SYSTEM")
    w = 1000
    h = 400
    root.geometry(f'{w}x{h}+{170}+{150}')
    root.config(bg='black')
    root.resizable(False, False)

    conn = sqlite3.connect('StudentsList.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS studentlist(
            ID_NUMBER,
            NAME,
            GENDER,
            YEAR_LEVEL,
            COURSE
            COURSE_CODE
            )""")
    c.execute("""CREATE TABLE IF NOT EXISTS courselist(
            COURSE_CODE,
            COURSE
            )""")

    def register():
        if E1.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif E2.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif gender.get() == 'Select Gender':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif yearlvl.get() == 'Select Year Level':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif course.get() == 'Select Course':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif course_code.get() == 'Select Course_CODE':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()
        c.execute("INSERT INTO studentlist VALUES(:ID_NUMBER, :NAME, :GENDER,:YEAR_LEVEL,:COURSE,:COURSE_CODE)",
                  {
                      'ID_NUMBER': E1.get(),
                      'NAME': E2.get(),
                      'GENDER': gender.get(),
                      'YEAR_LEVEL': yearlvl.get(),
                      'COURSE': course.get(),
                      'COURSE_CODE': course_code.get()

                  })

        conn.commit()
        messagebox.showinfo("REGISTRATION INFORMATION", "YEHEY! YOU JUST GOT REGISTERED!")
        conn.close()

        E1.delete(0, END)
        E2.delete(0, END)
        gender.set("Select Gender")
        yearlvl.set("Select Year Level")
        course_code.set("Select Course")
        course.set("Select Course Code")

    def select():
        conn = sqlite3.connect('StudentsList.db')

        E3.delete(0, END)
        E4.delete(0, END)
        root_gender.delete(0, END)
        root_yearlvl.delete(0, END)
        root_course.delete(0, END)
        root_coursecode.delete(0, END)

        selected = tree.focus()
        values = tree.item(selected, 'values')

        E3.insert(0, values[0])
        E4.insert(0, values[1])
        root_gender.insert(0, values[2])
        root_yearlvl.insert(0, values[3])
        root_course.insert(0, values[4])
        root_coursecode.insert(0, values[5])

        conn.commit()
        conn.close()

    def update():
        if E3.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif E4.get() == '':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_gender.get() == 'Select Gender':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_yearlvl.get() == 'Select Year Level':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_course.get() == 'Select Course':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")
        elif root_coursecode.get() == 'Select Course Code':
            return messagebox.showwarning("WARNING!", "PLEASE TRY TO COMPLETE THE INPUT")

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()
        messagebox.showinfo("UPDATE INFORMATION", "YEHEY! DATA UPDATED")
        data1 = E3.get()
        data2 = E4.get()
        data3 = root_gender.get()
        data4 = root_yearlvl.get()
        data5 = root_course.get()
        data6 = root_coursecode.get()

        selected = tree.selection()
        tree.item(selected, values=(data1, data2, data3, data4, data5, data6))
        c.execute(
            "UPDATE studentlist set  ID_NUMBER=?, NAME=?, GENDER=?, YEAR_LEVEL=?, COURSE=?, COURSE_CODE=?  WHERE ID_NUMBER=? ",
            (data1, data2, data3, data4, data5, data6, data1))

        conn.commit()
        conn.close()

    def refresh():
        root.destroy()
        root2 = Tk()
        root2.title("STUDENT INFORMATION SYSTEM")
        root2.geometry("1000x400")
        root2.config(bg='black')
        root2.resizable(False, False)
        root2.overrideredirect(True)
        root2.attributes('-alpha', 0.0)

        def des():
            root2.destroy()

        root2.after(10, lambda: (des(), main()))

        root2.mainloop()

    def delete():
        if messagebox.askyesno("DELETE CONFIRMATION", "ARE YOU SURE?") == False:
            return
        else:
            messagebox.showinfo("DELETE CONFIRMATION", "DATA SUCCESSFULLY DELETED")
            conn = sqlite3.connect("StudentsList.db")
            c = conn.cursor()
            for selected_item in tree.selection():
                c.execute("DELETE FROM studentlist WHERE ID_number=?", (tree.set(selected_item, '#1'),))
                conn.commit()
                tree.delete(selected_item)
            conn.close()

    def search():
        root1 = Tk()
        root1.title("STUDENT FOUND!")
        root1.geometry("1000x100")
        root1.config(bg='white')
        root1.resizable(False, False)

        conn = sqlite3.connect('StudentsList.db')
        c = conn.cursor()

        c.execute("SELECT * FROM studentlist WHERE ID_NUMBER=? ", (E3.get(),))
        records = c.fetchall()

        frm = Frame(root1)
        frm.pack(side=LEFT, padx=5, pady=(0, 0))

        tree = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height=13)
        tree.pack()

        tree.heading(1, text="ID NUMBER", anchor=CENTER)
        tree.column("1", minwidth=0, width=150)
        tree.heading(2, text="NAME", anchor=CENTER)
        tree.heading(3, text="GENDER", anchor=CENTER)
        tree.column("3", minwidth=0, width=150)
        tree.heading(4, text="YEAR LEVEL", anchor=CENTER)
        tree.column("4", minwidth=0, width=150)
        tree.heading(5, text="COURSE", anchor=CENTER)
        tree.heading(6, text="COURSE CODE", anchor=CENTER)
        tree.column("6", minwidth=0, width=150)

        for i in records:
            tree.insert('', 'end', value=i)

        if not records:
            root1.destroy()
            messagebox.showinfo("SEARCH INFORMATION", "STUDENT DOESN'T EXIST or ENTER ID NUMBER")

        root1.mainloop()

    Reg = LabelFrame(root, text="Registration Form", width=500, height=200, bg="black", fg="white",
                     font=("Lucida Console", 15, "bold"))
    Reg.place(x=500, y=0)
    Upd_Del = LabelFrame(root, text="Update and Delete Form", width=500, height=200, bg="black", fg="white",
                         font=("Lucida Console", 15, "bold"))
    Upd_Del.place(x=0, y=0)
    L1 = Label(root, text="ID NUMBER:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L1.place(x=510, y=35)
    L2 = Label(root, text="NAME:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L2.place(x=510, y=60)
    L3 = Label(root, text="GENDER:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L3.place(x=510, y=85)
    L4 = Label(root, text="YEAR LEVEL:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L4.place(x=510, y=110)
    L5 = Label(root, text="COURSE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L5.place(x=510, y=135)
    L6 = Label(root, text="COURSE CODE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L6.place(x=510, y=160)

    E1 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E1.place(x=650, y=35)
    E2 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E2.place(x=650, y=60)

    gender = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    gender.set("Select Gender")
    gender['values'] = ("Male", "Female", "Other")
    gender.place(x=650, y=85)

    yearlvl = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    yearlvl.set("Select Year Level")
    yearlvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
    yearlvl.place(x=650, y=110)

    course = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    course.set("Select Course")
    course['values'] = (
    "BS in Computer Science", "BS in Computer Application", "BS in Information Technology", "BS in Information System", "BS in Statistics", "BS in Mathematics")
    course.place(x=650, y=135)

    course_code = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    course_code.set("Select Course Code")
    course_code['values'] = ("BSCS", "BSCA", "BSIT", "BSIS", "BSSTAT", "BSMATH")
    course_code.place(x=650, y=160)

    Sel = Button(root, text="SELECT", font=("Lucida Console", 9, "bold"), command=select)
    Sel.place(x=300, y=15)
    Upd = Button(root, text="UPDATE", font=("Lucida Console", 9, "bold"), command=update)
    Upd.place(x=365, y=15)
    Del = Button(root, text="DELETE", font=("Lucida Console", 9, "bold"), command=delete)
    Del.place(x=430, y=15)
    Sea = Button(root, text="SEARCH", font=("Lucida Console", 9, "bold"), command=search)
    Sea.place(x=430, y=40)
    Reg = Button(root, text="REGISTER", font=("Lucida Console", 9, "bold"), command=register)
    Reg.place(x=900, y=170)
    Ref = Button(root, text="REFRESH", font=("Lucida Console", 9, "bold"), command=refresh)
    Ref.place(x=420, y=170)

    conn = sqlite3.connect('StudentsList.db')
    c = conn.cursor()

    c.execute("SELECT * FROM studentlist")
    records = c.fetchall()
    total = c.rowcount

    frm = Frame(root)
    frm.pack(side=LEFT, padx=5, pady=(200, 0))

    tree = ttk.Treeview(frm, columns=(1, 2, 3, 4, 5, 6), show="headings", height=13)
    tree.pack()

    tree.heading(1, text="ID NUMBER", anchor=CENTER)
    tree.column("1", minwidth=0, width=150)
    tree.heading(2, text="NAME", anchor=CENTER)
    tree.heading(3, text="GENDER", anchor=CENTER)
    tree.column("3", minwidth=0, width=150)
    tree.heading(4, text="YEAR LEVEL", anchor=CENTER)
    tree.column("4", minwidth=0, width=150)
    tree.heading(5, text="COURSE", anchor=CENTER)
    tree.heading(6, text="COURSE CODE", anchor=CENTER)
    tree.column("6", minwidth=0, width=150)

    for i in records:
        tree.insert('', 'end', value=i)

    E3 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E3.place(x=200, y=40)
    E4 = Entry(root, bd=2, width=27, font=("Lucida Console", 10))
    E4.place(x=130, y=75)

    root_gender = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_gender.set("Select Gender")
    root_gender['values'] = ("Male", "Female", "Other")
    root_gender.place(x=130, y=100)

    root_yearlvl = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_yearlvl.set("Select Year Level")
    root_yearlvl['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year")
    root_yearlvl.place(x=130, y=125)

    root_course = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_course.set("Select Course")
    root_course['values'] = (
    "BS in Computer Science", "BS in Computer Application", "BS in Information Technology", "BS in Information System", "BS in Statistics", "BS in Mathematics")
    root_course.place(x=130, y=150)

    root_coursecode = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_coursecode.set("Select Course Code")
    root_coursecode['values'] = ("BSCS", "BSCA", "BSIT", "BSIS", "BSSTAT", "BSMATH")
    root_coursecode.place(x=130, y=175)

    L7 = Label(root, text="ID NUMBER TO FIND:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L7.place(x=5, y=38)
    L8 = Label(root, text="NAME:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L8.place(x=5, y=75)
    L9 = Label(root, text="GENDER:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L9.place(x=5, y=100)
    L10 = Label(root, text="YEAR LEVEL:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L10.place(x=5, y=125)
    L11 = Label(root, text="COURSE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L11.place(x=5, y=150)
    L12 = Label(root, text="COURSE CODE:", bg="black", fg="white", font=("Lucida Console", 11, "bold"))
    L12.place(x=5, y=175)

    conn.commit()
    conn.close()

    root.mainloop()

def des():
    top.destroy()

top.after(100, lambda :(des(), main()))

top.mainloop()
