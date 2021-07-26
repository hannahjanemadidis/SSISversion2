from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import os
import sqlite3

root = Tk()
root.geometry("1360x700")
root.title('SSIS')
root.state('zoomed')
root.configure(background="blue")
root.resizable(False, False)
positionRight = int((root.winfo_screenwidth()/2 - 688))
positionDown = int((root.winfo_screenheight()/2 - 386))
root.geometry("+{}+{}".format(positionRight, positionDown))

StdID = StringVar()
Name = StringVar()
Gender = StringVar()
Course = StringVar()
YearLevel = IntVar()

mainFrame = LabelFrame(root, bg="cadetblue1", highlightbackground="gray26",highlightthickness=4)
mainFrame.place(x=468,y=100,height=575,width=885)

mainFrame2 = LabelFrame(root, bg="cadetblue1",highlightbackground="gray26",highlightthickness=4)
mainFrame2.place(x=8,y=100,height=575,width=450)

Label(root, text="STUDENT INFORMATION SYSTEM", font = ('Britannic Bold', 50, 'bold'),fg="black",bg= "blue", width=32).pack(side=TOP,fill=X)   
Label(mainFrame, text="STUDENT LIST", font = ('Apple SD Gothic Neo', 30, 'bold'),fg="black",bg="cadetblue1", width=34).grid(row=0,column=0, columnspan=6)
Label(mainFrame2, text="COURSES LIST", font = ('Apple SD Gothic Neo', 30, 'bold'),fg="black",bg="cadetblue1", width=15).grid(row=0,column=0, columnspan=6)

mydb = sqlite3.connect('SSIS2.db')
mycursor = mydb.cursor()     

mydb.execute("PRAGMA foreign_keys = ON;"); 

mycursor.execute("""CREATE TABLE IF NOT EXISTS COURSE_INFO(
        course_code text varchar(10) PRIMARY KEY,
        course_name text
        )""")


mycursor.execute("""CREATE TABLE IF NOT EXISTS STUD_INFO_SYS(
        ID_number text PRIMARY KEY,
        name text,
        course_code string,
        year_level text,
        gender text,
        FOREIGN KEY (course_code)
            REFERENCES COURSE_INFO(course_code)
                ON DELETE CASCADE
        )""")

mydb.commit()

def makeList():
    global listStudents
    mycursor.execute("SELECT * FROM STUD_INFO_SYS")
    listStudents = mycursor.fetchall()
    global listCourse
    mycursor.execute("SELECT * FROM COURSE_INFO")
    listCourse = mycursor.fetchall()



def addCourse():
    top=Toplevel()
    top.title('ADD COURSE')
    top.geometry("556x230")
    top.resizable(0,0)
    top.geometry("+{}+{}".format(positionRight+400, positionDown+230))
    
    SecondFrame = Frame(top, bg="#eaebeb")
    SecondFrame.grid()
    
    SecDataFrame = Frame(SecondFrame,bd=1, width=1300, height=400, padx=20, pady=20, bg ="cadetblue1")
    SecDataFrame.pack(side=BOTTOM)
    
    CourseInf=LabelFrame(SecDataFrame, width=1000, height=600, padx=20, bg="cadetblue1", font=('Apple SD Gothic Neo ',20,'bold'),text="Course Information", fg="black")
    CourseInf.pack(side=LEFT)
    
    Cno.set("")
    Cname.set("")
    
    Ccode = Label(CourseInf,text="Course Code ",font=('Apple SD Gothic Neo',13, 'bold'), padx=2, pady=2, bg="cadetblue1", fg="black",)
    Ccode.grid(row=1, column=0, sticky=W)
    code = Entry(CourseInf, font=('Apple SD Gothic Neo',13),textvariable=Ccode, width=39)
    code.grid(row=1, column=1, pady=8)
    
    CName = Label(CourseInf, font=('Apple SD Gothic Neo',13, 'bold'),text="Course Name ", padx=2, pady=2, bg="cadetblue1", fg="black")
    CName.grid(row=2, column=0, sticky=W)
    coursename = Entry(CourseInf, font=('Apple SD Gothic Neo',13),textvariable=Cname, width=39)
    coursename.grid(row=2, column=1, pady=8)

    def addCourseData():
        if  code.get() == "" or coursename.get() == "":
            messagebox.showinfo("Please Fill In the Box")
        else:
            mycursor.execute("INSERT INTO COURSE_INFO(course_code,course_name)VALUES(?,?)",
                                     (code.get(),coursename.get()))
            messagebox.showinfo("Course Recorded Successfully")
            top.destroy()
            mydb.commit()
            viewCourseList()
            viewList()
            
    AddCourse=Button(CourseInf, text="ADD COURSE", command=addCourseData,font=('Apple SD Gothic Neo', 15,'bold'), bg="cadetblue1", fg="black")
    AddCourse.grid(row=3, column=0, columnspan=3,pady=8)
    
def viewCourseList():
    makeList()
    for i in treeSec.get_children():
        treeSec.delete(i)
    counter = 0
    for course in listCourse:
        treeSec.insert(parent='',  index='end', iid=counter,
                        values=(course[0],course[1]))
        counter += 1
        
def searchCourse():
    for i in treeSec.get_children():
        treeSec.delete(i)
    
    search2 = searchbar2.get()
    counter = 0
    for course in listCourse:
        if course[0].startswith(search2):
            treeSec.insert(parent='',  index='end', iid=counter,
                        values=(course[0],course[1]))
        counter += 1
        
def deleteCourse():
    messageDeleteCour = messagebox.askyesno("Do you want to remove this course?")
    if messageDeleteCour > 0:
        selectedCourse = treeSec.selection()[0]
        courcode = treeSec.item(selectedCourse)['values'][0]
        for course in listCourse:
            if courcode == course[0]:
                courcode =course[0]
                break
        mycursor.execute("DELETE FROM COURSE_INFO WHERE course_code=?",(courcode,))
        mydb.commit()
        treeSec.delete(selectedCourse)
        viewList()
        viewCourseList()

def updateCourse(index):
    def thisUpdateCourse(CourseInfo):
        Cselect = treeSec.selection()
        for i in Cselect:
            mycursor.execute("UPDATE COURSE_INFO SET course_name=?\
                             WHERE course_code=?", (Cname.get(),Ccode.get(),))
            mydb.commit()
            messagebox.showinfo("Student Information System","Course updated successfully")
            viewCourseList()
            viewList()
        
    CinfoItem = treeSec.focus()
    values = treeSec.item(CinfoItem,"values")
    
    topUpC=Toplevel()
    topUpC.title('UPDATE COURSE')
    topUpC.geometry("556x230")
    topUpC.resizable(0,0)
    topUpC.geometry("+{}+{}".format(positionRight+400, positionDown+230))
    
    CourseInfo = treeSec.item(index)['values']
    
    CourseFrame = Frame(topUpC, bg="#eaebeb")
    CourseFrame.grid()
            
    DataCFrame = Frame(CourseFrame,bd=1, width=1300, height=400, padx=20, pady=20, bg ="#eaebeb")
    DataCFrame.pack(side=BOTTOM)
            
    DataCAdd=LabelFrame(DataCFrame, width=1000, height=600, padx=20, bg="#eaebeb", font=('Palatino Linotype',20,'bold'),text="Course Information", fg="#104c70")
    DataCAdd.pack(side=LEFT)
            
    CCode = Label(DataCAdd, font=('Palatino Linotype',13, 'bold'),text="Course Code  ", padx=2, pady=2, bg="#eaebeb", fg="#104c70")
    CCode.grid(row=1, column=0, sticky=W)
    code = Entry(DataCAdd, font=('Palatino Linotype',13),textvariable=Ccode, width=39)
    code.grid(row=1, column=1, pady=8)
            
    CName = Label(DataCAdd, font=('Palatino Linotype',13, 'bold'),text="Course Name ", padx=2, pady=2, bg="#eaebeb", fg="#104c70")
    CName.grid(row=2, column=0, sticky=W)
    courseN = Entry(DataCAdd, font=('Palatino Linotype',13),textvariable=Cname, width=39)
    courseN.grid(row=2, column=1, pady=8)

    CourseSubmit=Button(DataCAdd, text="UPDATE", command=lambda:thisUpdateCourse(CourseInfo), font=('Apple SD Gothic Neo', 15,'bold'), bg="cadetblue1", fg="black")
    CourseSubmit.grid(row=5, column=0, columnspan=3,pady=8)
    
    Ccode.set(values[0])
    code.config(state=DISABLED)
    Cname.set(values[1])

Cno = IntVar()
Ccode = StringVar()
Cname = StringVar()

searchbar2 = Entry(mainFrame2,font=('Palatino Linotype',12), width=40)
searchbar2.grid(row=2, column=1,columnspan=4, padx=4, pady=5)
searchbutton2 = Button(mainFrame2, text="SEARCH",font=('Apple SD Gothic Neo', 9,'bold'), bg="gray68", fg="black", width=12,command=searchCourse)
searchbutton2.grid(row=2, column=0, padx=6, pady=5)
    
viewButton2 = Button(mainFrame2, text="VIEW ALL", command=viewCourseList,font=('Apple SD Gothic Neo', 9,'bold'), bg="gray68", fg="black",width=12)
viewButton2.grid(row=1, column=0, padx=6, pady=5)

addButton2 = Button(mainFrame2, text="ADD COURSE", font=('Apple SD Gothic Neo', 9,'bold'), bg="gray68", fg="black",width=16,command=addCourse)
addButton2.grid(row=1, column=3, padx=4, pady=5)
    
edit2 = Button(mainFrame2, text="EDIT",font=('Apple SD Gothic Neo', 9,'bold'), bg="gray68", fg="black", width=11, command=lambda:updateCourse(treeSec.focus()))
edit2.grid(row=1, column=2, padx=6, pady=5)
    
delete2 = Button(mainFrame2, text="DELETE",font=('Apple SD Gothic Neo', 9,'bold'), bg="gray68", fg="black", width=12,command=deleteCourse)
delete2.grid(row=1, column=4, padx=5, pady=5)

treeSec = ttk.Treeview(mainFrame2, height=20)
treeSec.grid(row=3, column=0, columnspan=6, padx=12, pady=10)
    
sSec = ttk.Style(mainFrame2)
sSec.configure("Treeview.Heading", font=('Apple SD Gothic Neo',11,'bold'))
sSec.configure(".", font=('Palatino Linotype',12))
        
treeSec['columns'] = ("Course Code","Course Name")

treeSec.column('#0',width=0, stretch=NO)
treeSec.column("Course Code", anchor=CENTER, width=30)
treeSec.column("Course Name", anchor=CENTER, width=210)

treeSec.heading("Course Code", text="Course Code", anchor=CENTER)
treeSec.heading("Course Name", text="Course Name", anchor=CENTER)

treeSec.place(x=4,y=150, height=410, width=425)


 
def clicked(*args):
    this = treeSec.selection()

    if len(this) != 0 or there == True:
        def add():
            top=Toplevel()
            top.title('ADD STUDENT')
            top.geometry("540x363")
            top.resizable(0,0)
            top.geometry("+{}+{}".format(positionRight+400, positionDown+190))
            
            MainFrame = Frame(top, bg="cadetblue1")
            MainFrame.grid()
            
            DataFrame = Frame(MainFrame,bd=1, width=1300, height=400, padx=20, pady=20, bg ="cadetblue1")
            DataFrame.pack(side=BOTTOM)
            
            StudInf=LabelFrame(DataFrame, width=1000, height=600, padx=20, bg="cadetblue1", font=('Apple SD Gothic Neo',20,'bold'),text="Student's Information", fg="black")
            StudInf.pack(side=TOP,fill=X)
            
            StdID.set("")
            Name.set("")
            Course.set("")
            YearLevel.set("")
            Gender.set("") 

            SILabel = Label(StudInf, font=('Apple SD Gothic Neo',13, 'bold'),text="Student ID  ", padx=2, pady=2, bg ="cadetblue1", fg="black")
            SILabel.grid(row=0, column=0, sticky=W)
            ID = Entry(StudInf, font=('Apple SD Gothic Neo',13),textvariable=StdID, width=39)
            ID.grid(row=0, column=1, pady=8)
            
            FLabel = Label(StudInf, font=('Apple SD Gothic Neo',13, 'bold'),text="Name", padx=2, pady=2,  bg ="cadetblue1", fg="black")
            FLabel.grid(row=1, column=0, sticky=W)
            name = Entry(StudInf, font=('Apple SD Gothic Neo',13),textvariable=Name, width=39)
            name.grid(row=1, column=1, pady=8)
            
            CLabel = Label(StudInf, font=('Apple SD Gothic Neo',13, 'bold'),text="Course ", padx=2, pady=2, bg ="cadetblue1", fg="black")
            CLabel.grid(row=2, column=0, sticky=W)
            course = Entry(StudInf, font=('Apple SD Gothic Neo',13),textvariable=Course, width=39)
            course.grid(row=2, column=1, pady=8)
            
            YLabel = Label(StudInf, font=('Apple SD Gothic Neo',13, 'bold'),text="Year Level ", padx=2, pady=2,  bg ="cadetblue1", fg="black")
            YLabel.grid(row=3, column=0, sticky=W)
            ylevel = Entry(StudInf, font=('Apple SD Gothic Neo',13),textvariable=YearLevel, width=39)
            ylevel.grid(row=3, column=1, pady=8)

            GLabel = Label(StudInf, font=('Apple SD Gothic Neo',13, 'bold'),text="Gender ", padx=2, pady=2,  bg ="cadetblue1", fg="black")
            GLabel.grid(row=4, column=0, sticky=W)
            gender = Entry(StudInf, font=('Apple SD Gothic Neo',13),textvariable=Gender, width=39)
            gender.grid(row=4, column=1, pady=8)
          

           

            
            def addData():
                if  ID.get() == "" or name.get() == "" or gender.get() == "" or course.get() == "" or ylevel.get()== "":
                    messagebox.showinfo("Student Information System")
                else:
                    for student in listStudents:                        
                            if student[0] == ID.get() or student[1] == name.get():
                                messagebox.showinfo("ID Number Already Exists")
                                return
                    x = StdID.get()
                    id_list = []
                    for i in x:
                        id_list.append(i)
                    if "-" in id_list:
                        y = x.split("-")
                        year = y[0]
                        number = y[1]
                        cournum=""
                        if year.isdigit() == False or number.isdigit() == False:
                            messagebox.showerror("Invalid ID")
                        else:
                            for cour in list_Course:
                                if cour[0] == course.get():
                                    if cour[0] == course.get():
                                        cournum = cour[0]
                                    else:
                                         messagebox.showinfo("Course Not Found")
                            try:
                                mycursor.execute("INSERT INTO STUD_INFO_SYS(ID_number,name,course_code,year_level,gender)VALUES(?,?,?,?,?)",
                                                 (ID.get(),name.get(),cournum,ylevel.get(),gender.get()))
                                messagebox.showinfo("Student Recorded Successfully")
                                top.destroy()
                                mydb.commit()
                                viewList()
                                viewCourseList()
                            except:
                                messagebox.showinfo("Course Nooooot Found")
                        
                    else:
                        messagebox.showerror("Invalid ID")

            addstudent=Button(StudInf, text="ADD STUDENT",command=addData, font=('Apple SD Gothic Neo', 15,'bold'),  bg ="gray26", fg="black")
            addstudent.grid(row=5, column=0, columnspan=3,pady=8) 




           
        def viewList():
            makeList()
            for i in tree.get_children():
                tree.delete(i)
            
            counter = 0
            mycursor.execute("SELECT * FROM STUD_INFO_SYS")
            listStudents = mycursor.fetchall()
            for student in listStudents:
                if listStudents != []:
                    for cour in listCourse:
                        if cour[0] == student[2]:
                            courname = cour[0]
                    
                    if there == True or len(this) == 0:
                        tree.insert(parent='',  index='end', iid=counter,
                                        values=(student[0],student[1],courname,student[3],student[4]))
                    
                    elif courname == treeSec.item(treeSec.focus(),"values")[0]:
                        tree.insert(parent='',  index='end', iid=counter,
                                        values=(student[0],student[1],courname,student[3],student[4]))
                counter += 1   
                    
        def search():
            for i in tree.get_children():
                tree.delete(i)
            search = searchbar.get()
            counter = 0
            for student in listStudents:
                if student[0].startswith(search):
                    for cour in listCourse:
                        if cour[0] == student[2]:
                            courname = cour[0]
                    if len(this) == 0:
                        tree.insert(parent='',  index='end', iid=counter,
                                    values=(student[0],student[1],courname,student[3],student[4]))
                    elif courname == treeSec.item(treeSec.focus(),"values")[0]:
                        tree.insert(parent='',  index='end', iid=counter,
                                        values=(student[0],student[1],courname,student[3],student[4]))
                counter += 1
                
        def delete():
            messageDeleteStud = messagebox.askyesno("Do you want to delete this record?")
            if messageDeleteStud > 0:
                selected = tree.selection()[0]
                uid = tree.item(selected)['values'][0]
                mycursor.execute("DELETE FROM STUD_INFO_SYS WHERE ID_number=?",(uid,))
                mydb.commit()
                tree.delete(selected)
                viewList()
                viewCourseList()
            
        def update(index):
            def thisUpdate(studentInfo):
                select = tree.selection()
                for selected in select:
                    
                    mycursor.execute("UPDATE STUD_INFO_SYS SET ID_number=?,name=?,course_code=?,year_level=?,gender=?\
                                     WHERE ID_number=?", (ID.get(),name.get(),course.get(),ylevel.get(),gender.get(),\
                                        tree.set(selected,'#1')))
                    mydb.commit()
                    messagebox.showinfo("Student updated successfully")
                    viewList()
                    viewCourseList()
                
            infoItem = tree.focus()
            values = tree.item(infoItem,"values")
            
            topUpS=Toplevel()
            topUpS.title('UPDATE STUDENTS')
            topUpS.geometry("540x363")
            topUpS.resizable(0,0)
            topUpS.geometry("+{}+{}".format(positionRight+400, positionDown+190))
            
            studentInfo = tree.item(index)['values']
            
            MainFrame2 = Frame(topUpS, bg="#eaebeb")
            MainFrame2.grid()
                    
            DataFrame2 = Frame(MainFrame2,bd=1, width=1300, height=400, padx=20, pady=20, bg ="cadetblue1")
            DataFrame2.pack(side=BOTTOM)
                    
            DataAdd2=LabelFrame(DataFrame2, width=1000, height=600, padx=20, bg="cadetblue1", font=('Palatino Linotype',20,'bold'),text="Student's Information", fg="black")
            DataAdd2.pack(side=LEFT)
                    
            SILable = Label(DataAdd2, font=('Apple SD Gothic Neo',13, 'bold'),text="Student ID  ", padx=2, pady=2, bg ="cadetblue1", fg="black")
            SILable.grid(row=0, column=0, sticky=W)
            ID = Entry(DataAdd2, font=('Apple SD Gothic Neo',13),textvariable=StdID, width=39)
            ID.grid(row=0, column=1, pady=8)
                    
            FLabel = Label(DataAdd2, font=('Apple SD Gothic Neo',13, 'bold'),text="Name  ", padx=2, pady=2, bg ="cadetblue1", fg="black")
            FLabel.grid(row=1, column=0, sticky=W)
            name = Entry(DataAdd2, font=('Apple SD Gothic Neo',13),textvariable=Name, width=39)
            name.grid(row=1, column=1, pady=8)
                    
            CLabel = Label(DataAdd2, font=('Apple SD Gothic Neo',13, 'bold'),text="Course ", padx=2, pady=2, bg ="cadetblue1", fg="black")
            CLabel.grid(row=2, column=0, sticky=W)
            course = Entry(DataAdd2, font=('Apple SD Gothic Neo',13),textvariable=Course, width=39)
            course.grid(row=2, column=1, pady=8)
                    
            YLabel = Label(DataAdd2, font=('Apple SD Gothic Neo',13, 'bold'),text="Year Level ", padx=2, pady=2,  bg ="cadetblue1", fg="black")
            YLabel.grid(row=3, column=0, sticky=W)
            ylevel = Entry(DataAdd2, font=('Apple SD Gothic Neo',13),textvariable=YearLevel, width=39)
            ylevel.grid(row=3, column=1, pady=8)

            GLabel = Label(DataAdd2, font=('Apple SD Gothic Neo',13, 'bold'),text="Gender ", padx=2, pady=2,  bg ="cadetblue1", fg="black")
            GLabel.grid(row=4, column=0, sticky=W)
            gender = Entry(DataAdd2, font=('Apple SD Gothic Neo',13),textvariable=Gender, width=39)
            gender.grid(row=4, column=1, pady=8)

            update=Button(DataAdd2, text="UPDATE", command=lambda:thisUpdate(studentInfo), font=('Apple SD Gothic Neo', 15,'bold'), bg ="gray26", fg="black")
            update.grid(row=5, column=0, columnspan=3,pady=8)


                
        def viewAll():
            for item in treeSec.selection():
                treeSec.selection_remove(item)
            global there
            there=True
            viewList()
            there=False
            
        searchbar = Entry(mainFrame,font=('Apple SD Gothic Neo',12), width=30)
        searchbar.grid(row=1, column=0, padx=6, pady=5)
        searchbutton = Button(mainFrame, text="SEARCH",font = ('Apple SD Gothic Neo', 9, 'bold'),fg="black",bg= "gray68", width=13, command=search)
        searchbutton.grid(row=1, column=1, padx=6, pady=5)
            
        viewButton = Button(mainFrame, text="VIEW LIST", font = ('Apple SD Gothic Neo', 9, 'bold'),fg="black",bg= "gray68",width=13, command=viewAll)
        viewButton.grid(row=1, column=3, padx=6, pady=5)

        addButton = Button(mainFrame, text="ADD STUDENT", font = ('Apple SD Gothic Neo', 9, 'bold'),fg="black",bg= "gray68",width=16, command=add)
        addButton.grid(row=1, column=2, padx=6, pady=5)
            
        edit = Button(mainFrame, text="EDIT", font = ('Apple SD Gothic Neo', 9, 'bold'),fg="black",bg= "gray68", width=13, command=lambda:update(tree.focus()))
        edit.grid(row=1, column=5, padx=6, pady=5)
            
        delete = Button(mainFrame, text="DELETE",font = ('Apple SD Gothic Neo', 9, 'bold'),fg="black",bg= "gray68", width=13, command=delete)
        delete.grid(row=1, column=4, padx=6, pady=5)

        tree = ttk.Treeview(mainFrame, height=20)
        tree.grid(row=2, column=0, columnspan=7, padx=12, pady=10)
            
        s = ttk.Style(root)
        s.configure("Treeview.Heading", font=('Palatino Linotype',11,'bold'))
        s.configure(".", font=('Palatino Linotype',12))
                
        tree['columns'] = ("ID number", "Name","Course","Year Level","Gender")

        tree.column('#0',width=0, stretch=NO)
        tree.column("ID number", anchor=CENTER, width=125)
        tree.column("Name", anchor=CENTER, width=250)
        tree.column("Course", anchor=CENTER, width=250)
        tree.column("Year Level", anchor=CENTER, width=130)
        tree.column("Gender", anchor=CENTER, width=100)

        tree.heading("ID number", text="ID number", anchor=CENTER)
        tree.heading("Name", text="Name", anchor=CENTER)
        tree.heading("Course", text="Course", anchor=CENTER)
        tree.heading("Year Level", text="Year Level", anchor=CENTER)
        tree.heading("Gender", text="Gender", anchor=CENTER)

        tree.place(x=9,y=110,height=450)
        viewList()



viewCourseList()
global there
there=True
clicked()
there=False

treeSec.bind("<ButtonRelease-1>", clicked)
root.mainloop()
