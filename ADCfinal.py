import sqlite3
import sys
from tkinter import *
from escpos import printer
import datetime
root = Tk()

root.title('Agarwal Dental Centre')
root.attributes('-fullscreen', False)
conn = sqlite3.connect('patient_info.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTs patient (
		name text,
		phone text,
		address text,
		age integer,
		info text,
		Patient_ID integer,
		PRIMARY KEY ("Patient_ID") 
		)""")

c.execute("""CREATE TABLE IF NOT EXISTs Appointments (
		p_id text,
		appno text,
		date text
		)""")



appno = 0



def submit_success():
	#root.withdraw()
	global success
	success = Tk()
	success.title('Success')
	success.geometry("500x200")
	conn = sqlite3.connect('patient_info.db')
	c = conn.cursor()
	c.execute("SELECT * FROM patient ORDER BY Patient_ID DESC LIMIT 1")
	records = c.fetchall()
	print(records)

	print_records = ''
	for record in records:
		print_records += str(record[0]) + "		" + str(record[1]) + "	"+ str(record[2]) + "	"+ str(record[3]) + "	" +str(record[4]) + "	" +str(record[5]) + "\n"

	query_label = Label(success, text=print_records)
	query_label.grid(row=0, column=0, columnspan=2)

	

def view_command():
    Listbox1.delete(0,END)
    for row in view():
        Listbox1.insert(END,row)


def view():
	conn = sqlite3.connect('patient_info.db')
	c = conn.cursor()
	c.execute("SELECT * FROM appointments" )
	row = c.fetchall()
	c.close()
	return row

def search_command():
    Listbox1.delete(0,END)
    for row in search(Entry11.get(),Entry12.get(),Entry13.get()):
        Listbox1.insert(END,row)


def search(name="",phone="",Patient_ID=""):
    conn=sqlite3.connect("patient_info.db")
    c=conn.cursor()
    c.execute("SELECT * FROM patient WHERE name=? OR phone=? OR Patient_ID=?",(name,phone,Patient_ID))
    row=c.fetchall()
    conn.close()
    return row



def appointment():
	dateapp = datetime.datetime.now()
	print(dateapp)
	global appno
	appno = appno + 1
	print(appno)
	conn = sqlite3.connect('patient_info.db')
	c = conn.cursor()
	c.execute("INSERT INTO appointments VALUES (:p_id, :appno , :date )",
			{
				'p_id': Entry8.get(),
				'appno': appno,
				'date': dateapp
			})

	conn.commit()
	conn.close()
	Entry8.delete(0, END)
	view_command()


def submit():
	conn = sqlite3.connect('patient_info.db')
	c = conn.cursor()
	c.execute("INSERT INTO patient(name, phone, address, age, info) VALUES (:name, :phone, :address, :age, :info)",
			{
				'name': Entry1.get(),
				'phone': Entry2.get(),
				'address': Entry3.get(),
				'age': Entry4.get(),
				'info': Entry5.get()
			})

	conn.commit()

	conn.close()

	Entry1.delete(0, END)
	Entry2.delete(0, END)
	Entry3.delete(0, END)
	Entry4.delete(0, END)
	Entry5.delete(0, END)

	submit_success()




def delete():
	conn = sqlite3.connect('patient_info.db')
	c = conn.cursor()

	c.execute("DELETE from patient WHERE Patient_ID = " + Entry7.get())

	Entry7.delete(0, END)

	conn.commit()

	conn.close()



def update():
        conn = sqlite3.connect('patient_info.db')
        c = conn.cursor()

        record_id = Entry6.get()
        Entry6.delete(0, END)
        c.execute("""UPDATE patient SET
		name = :name,
		phone = :phone,
		address = :address,
		age = :age,
		info = :info 
		WHERE Patient_ID = :Patient_ID""",
		{
		'name': name_editor.get(),
		'phone': phone_editor.get(),
		'address': address_editor.get(),
		'age': age_editor.get(),
		'info': info_editor.get(),
		'Patient_ID': record_id
		})
        
        conn.commit()

        conn.close()
        editor.destroy()
        root.deiconify()




def edit():
	global editor
	editor = Tk()
	editor.title('Update A Record')
	editor.geometry("500x200")
	conn = sqlite3.connect('patient_info.db')
	c = conn.cursor()


	record_id = Entry6.get()
	c.execute("SELECT * FROM patient WHERE Patient_ID = " + record_id)
	records = c.fetchall()
	
	global name_editor
	global phone_editor
	global address_editor
	global age_editor
	global info_editor
	name_editor = Entry(editor, width=30)
	name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
	phone_editor = Entry(editor, width=30)
	phone_editor.grid(row=1, column=1)
	address_editor = Entry(editor, width=30)
	address_editor.grid(row=2, column=1)
	age_editor = Entry(editor, width=30)
	age_editor.grid(row=3, column=1)
	info_editor = Entry(editor, width=30)
	info_editor.grid(row=4, column=1)
	
	name_label = Label(editor, text="Name")
	name_label.grid(row=0, column=0, pady=(10, 0))
	phone_label = Label(editor, text="Phone")
	phone_label.grid(row=1, column=0)
	address_label = Label(editor, text="Address")
	address_label.grid(row=2, column=0)
	age_label = Label(editor, text="Age")
	age_label.grid(row=3, column=0)
	info_label = Label(editor, text="Other Info")
	info_label.grid(row=4, column=0)
	
	for record in records:
		name_editor.insert(0, record[0])
		phone_editor.insert(0, record[1])
		address_editor.insert(0, record[2])
		age_editor.insert(0, record[3])
		info_editor.insert(0, record[4])
	
	edit_btn = Button(editor, text="Save Record", command=update)
	edit_btn.grid(row=5, column=1, columnspan=2, pady=10, padx=10, ipadx=145)


Labelframe1 = LabelFrame(root)
Labelframe1.place(relx=0.006, rely=0.011, relheight=0.484
, relwidth=0.317)
Labelframe1.configure(relief='groove')
Labelframe1.configure(foreground="black")
Labelframe1.configure(text='''Add New Patient''')
Labelframe1.configure(background="#d9d9d9")
Labelframe1.configure(highlightbackground="#d9d9d9")
Labelframe1.configure(highlightcolor="black")

Entry1 = Entry(Labelframe1)
Entry1.place(relx=0.263, rely=0.225, height=24, relwidth=0.691
, bordermode='ignore')
Entry1.configure(background="white")
Entry1.configure(disabledforeground="#a3a3a3")
Entry1.configure(font="TkFixedFont")
Entry1.configure(foreground="#000000")
Entry1.configure(highlightbackground="#d9d9d9")
Entry1.configure(highlightcolor="black")
Entry1.configure(insertbackground="black")
Entry1.configure(selectbackground="blue")
Entry1.configure(selectforeground="white")

Entry2 = Entry(Labelframe1)
Entry2.place(relx=0.263, rely=0.315, height=24, relwidth=0.691
, bordermode='ignore')
Entry2.configure(background="white")
Entry2.configure(disabledforeground="#a3a3a3")
Entry2.configure(font="TkFixedFont")
Entry2.configure(foreground="#000000")
Entry2.configure(highlightbackground="#d9d9d9")
Entry2.configure(highlightcolor="black")
Entry2.configure(insertbackground="black")
Entry2.configure(selectbackground="blue")
Entry2.configure(selectforeground="white")

Entry3 = Entry(Labelframe1)
Entry3.place(relx=0.263, rely=0.404, height=24, relwidth=0.691
, bordermode='ignore')
Entry3.configure(background="white")
Entry3.configure(disabledforeground="#a3a3a3")
Entry3.configure(font="TkFixedFont")
Entry3.configure(foreground="#000000")
Entry3.configure(highlightbackground="#d9d9d9")
Entry3.configure(highlightcolor="black")
Entry3.configure(insertbackground="black")
Entry3.configure(selectbackground="blue")
Entry3.configure(selectforeground="white")

Entry4 = Entry(Labelframe1)
Entry4.place(relx=0.263, rely=0.494, height=24, relwidth=0.691
, bordermode='ignore')
Entry4.configure(background="white")
Entry4.configure(disabledforeground="#a3a3a3")
Entry4.configure(font="TkFixedFont")
Entry4.configure(foreground="#000000")
Entry4.configure(highlightbackground="#d9d9d9")
Entry4.configure(highlightcolor="black")
Entry4.configure(insertbackground="black")
Entry4.configure(selectbackground="blue")
Entry4.configure(selectforeground="white")

Entry5 = Entry(Labelframe1)
Entry5.place(relx=0.263, rely=0.584, height=24, relwidth=0.691
, bordermode='ignore')
Entry5.configure(background="white")
Entry5.configure(disabledforeground="#a3a3a3")
Entry5.configure(font="TkFixedFont")
Entry5.configure(foreground="#000000")
Entry5.configure(highlightbackground="#d9d9d9")
Entry5.configure(highlightcolor="black")
Entry5.configure(insertbackground="black")
Entry5.configure(selectbackground="blue")
Entry5.configure(selectforeground="white")

Label1 = Label(Labelframe1)
Label1.place(relx=0.347, rely=0.034, height=20, width=201
, bordermode='ignore')
Label1.configure(activebackground="#f9f9f9")
Label1.configure(activeforeground="black")
Label1.configure(background="#d9d9d9")
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(font="-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
Label1.configure(foreground="#000000")
Label1.configure(highlightbackground="#d9d9d9")
Label1.configure(highlightcolor="black")
Label1.configure(text='''Add New Patient''')

Label2 = Label(Labelframe1)
Label2.place(relx=0.07, rely=0.225, height=26, width=72
, bordermode='ignore')
Label2.configure(activebackground="#f9f9f9")
Label2.configure(activeforeground="black")
Label2.configure(background="#d9d9d9")
Label2.configure(disabledforeground="#a3a3a3")
Label2.configure(foreground="#000000")
Label2.configure(highlightbackground="#d9d9d9")
Label2.configure(highlightcolor="black")
Label2.configure(text='''Name''')

Label3 = Label(Labelframe1)
Label3.place(relx=0.088, rely=0.315, height=26, width=52
, bordermode='ignore')
Label3.configure(activebackground="#f9f9f9")
Label3.configure(activeforeground="black")
Label3.configure(background="#d9d9d9")
Label3.configure(disabledforeground="#a3a3a3")
Label3.configure(foreground="#000000")
Label3.configure(highlightbackground="#d9d9d9")
Label3.configure(highlightcolor="black")
Label3.configure(text='''Phone''')

Label4 = Label(Labelframe1)
Label4.place(relx=0.07, rely=0.404, height=26, width=62
, bordermode='ignore')
Label4.configure(activebackground="#f9f9f9")
Label4.configure(activeforeground="black")
Label4.configure(background="#d9d9d9")
Label4.configure(disabledforeground="#a3a3a3")
Label4.configure(foreground="#000000")
Label4.configure(highlightbackground="#d9d9d9")
Label4.configure(highlightcolor="black")
Label4.configure(text='''Address''')

Label5 = Label(Labelframe1)
Label5.place(relx=0.07, rely=0.494, height=26, width=82
, bordermode='ignore')
Label5.configure(activebackground="#f9f9f9")
Label5.configure(activeforeground="black")
Label5.configure(background="#d9d9d9")
Label5.configure(disabledforeground="#a3a3a3")
Label5.configure(foreground="#000000")
Label5.configure(highlightbackground="#d9d9d9")
Label5.configure(highlightcolor="black")
Label5.configure(text='''Age''')

Label6 = Label(Labelframe1)
Label6.place(relx=0.053, rely=0.584, height=26, width=86
, bordermode='ignore')
Label6.configure(activebackground="#f9f9f9")
Label6.configure(activeforeground="black")
Label6.configure(background="#d9d9d9")
Label6.configure(disabledforeground="#a3a3a3")
Label6.configure(foreground="#000000")
Label6.configure(highlightbackground="#d9d9d9")
Label6.configure(highlightcolor="black")
Label6.configure(text='''Other Info.''')

Button1 = Button(Labelframe1)
Button1.place(relx=0.228, rely=0.787, height=73, width=316
, bordermode='ignore')
Button1.configure(activebackground="#ececec")
Button1.configure(command = submit)
Button1.configure(activeforeground="#000000")
Button1.configure(background="#d9d9d9")
Button1.configure(command=submit)
Button1.configure(disabledforeground="#a3a3a3")
Button1.configure(foreground="#000000")
Button1.configure(highlightbackground="#d9d9d9")
Button1.configure(highlightcolor="black")
Button1.configure(pady="0")
Button1.configure(text='''Add Patient Record''')

Labelframe3 = LabelFrame(root)
Labelframe3.place(relx=0.334, rely=0.011, relheight=0.483
, relwidth=0.328)
Labelframe3.configure(relief='groove')
Labelframe3.configure(foreground="black")
Labelframe3.configure(text='''Appointments''')
Labelframe3.configure(background="#d9d9d9")
Labelframe3.configure(highlightbackground="#d9d9d9")
Labelframe3.configure(highlightcolor="black")

Entry8 = Entry(Labelframe3)
Entry8.place(relx=0.22, rely=0.203, height=24, relwidth=0.719
, bordermode='ignore')
Entry8.configure(background="white")
Entry8.configure(disabledforeground="#a3a3a3")
Entry8.configure(font="TkFixedFont")
Entry8.configure(foreground="#000000")
Entry8.configure(highlightbackground="#d9d9d9")
Entry8.configure(highlightcolor="black")
Entry8.configure(insertbackground="black")
Entry8.configure(selectbackground="blue")
Entry8.configure(selectforeground="white")

Label12 = Label(Labelframe3)
Label12.place(relx=0.034, rely=0.203, height=26, width=82
, bordermode='ignore')
Label12.configure(activebackground="#f9f9f9")
Label12.configure(activeforeground="black")
Label12.configure(background="#d9d9d9")
Label12.configure(disabledforeground="#a3a3a3")
Label12.configure(foreground="#000000")
Label12.configure(highlightbackground="#d9d9d9")
Label12.configure(highlightcolor="black")
Label12.configure(text='''Select ID''')



Label14 = Label(Labelframe3)
Label14.place(relx=0.254, rely=0.068, height=26, width=312
, bordermode='ignore')
Label14.configure(activebackground="#f9f9f9")
Label14.configure(activeforeground="black")
Label14.configure(background="#d9d9d9")
Label14.configure(disabledforeground="#a3a3a3")
Label14.configure(font="-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
Label14.configure(foreground="#000000")
Label14.configure(highlightbackground="#d9d9d9")
Label14.configure(highlightcolor="black")
Label14.configure(text='''Add Appointment''')


Button4 = Button(Labelframe3)
Button4.place(relx=0.237, rely=0.608, height=63, width=366
, bordermode='ignore')
Button4.configure(activebackground="#ececec")
Button4.configure(activeforeground="#000000")
Button4.configure(background="#d9d9d9")
Button4.configure(command=appointment)
Button4.configure(disabledforeground="#a3a3a3")
Button4.configure(foreground="#000000")
Button4.configure(highlightbackground="#d9d9d9")
Button4.configure(highlightcolor="black")
Button4.configure(pady="0")
Button4.configure(text='''Add Appointment and Print Token''')

Button5 = Button(Labelframe3)
Button5.place(relx=0.237, rely=0.811, height=63, width=366
, bordermode='ignore')
Button5.configure(activebackground="#ececec")
Button5.configure(activeforeground="#000000")
Button5.configure(background="#d9d9d9")
Button5.configure(command=appointment)
Button5.configure(disabledforeground="#a3a3a3")
Button5.configure(foreground="#000000")
Button5.configure(highlightbackground="#d9d9d9")
Button5.configure(highlightcolor="black")
Button5.configure(pady="0")
Button5.configure(text='''Add Appointment''')

Labelframe4 = LabelFrame(root)
Labelframe4.place(relx=0.334, rely=0.511, relheight=0.476
, relwidth=0.329)
Labelframe4.configure(relief='groove')
Labelframe4.configure(foreground="black")
Labelframe4.configure(text='''Search''')
Labelframe4.configure(background="#d9d9d9")
Labelframe4.configure(highlightbackground="#d9d9d9")
Labelframe4.configure(highlightcolor="black")

Label16 = Label(Labelframe4)
Label16.place(relx=0.389, rely=0.046, height=26, width=163
, bordermode='ignore')
Label16.configure(activebackground="#f9f9f9")
Label16.configure(activeforeground="black")
Label16.configure(background="#d9d9d9")
Label16.configure(disabledforeground="#a3a3a3")
Label16.configure(font="-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
Label16.configure(foreground="#000000")
Label16.configure(highlightbackground="#d9d9d9")
Label16.configure(highlightcolor="black")
Label16.configure(text='''Search Record''')

Label17 = Label(Labelframe4)
Label17.place(relx=0.034, rely=0.16, height=26, width=92
, bordermode='ignore')
Label17.configure(activebackground="#f9f9f9")
Label17.configure(activeforeground="black")
Label17.configure(background="#d9d9d9")
Label17.configure(disabledforeground="#a3a3a3")
Label17.configure(foreground="#000000")
Label17.configure(highlightbackground="#d9d9d9")
Label17.configure(highlightcolor="black")
Label17.configure(text='''By Name''')

Label18 = Label(Labelframe4)
Label18.place(relx=0.017, rely=0.275, height=26, width=112
, bordermode='ignore')
Label18.configure(activebackground="#f9f9f9")
Label18.configure(activeforeground="black")
Label18.configure(background="#d9d9d9")
Label18.configure(disabledforeground="#a3a3a3")
Label18.configure(foreground="#000000")
Label18.configure(highlightbackground="#d9d9d9")
Label18.configure(highlightcolor="black")
Label18.configure(text='''By Phone''')

Label19 = Label(Labelframe4)
Label19.place(relx=0.034, rely=0.412, height=26, width=102
, bordermode='ignore')
Label19.configure(activebackground="#f9f9f9")
Label19.configure(activeforeground="black")
Label19.configure(background="#d9d9d9")
Label19.configure(disabledforeground="#a3a3a3")
Label19.configure(foreground="#000000")
Label19.configure(highlightbackground="#d9d9d9")
Label19.configure(highlightcolor="black")
Label19.configure(text='''By Patient ID''')

Entry11 = Entry(Labelframe4)
Entry11.place(relx=0.236, rely=0.16, height=24, relwidth=0.666
, bordermode='ignore')
Entry11.configure(background="white")
Entry11.configure(disabledforeground="#a3a3a3")
Entry11.configure(font="TkFixedFont")
Entry11.configure(foreground="#000000")
Entry11.configure(highlightbackground="#d9d9d9")
Entry11.configure(highlightcolor="black")
Entry11.configure(insertbackground="black")
Entry11.configure(selectbackground="blue")
Entry11.configure(selectforeground="white")

Entry12 = Entry(Labelframe4)
Entry12.place(relx=0.236, rely=0.275, height=24, relwidth=0.666
, bordermode='ignore')
Entry12.configure(background="white")
Entry12.configure(disabledforeground="#a3a3a3")
Entry12.configure(font="TkFixedFont")
Entry12.configure(foreground="#000000")
Entry12.configure(highlightbackground="#d9d9d9")
Entry12.configure(highlightcolor="black")
Entry12.configure(insertbackground="black")
Entry12.configure(selectbackground="blue")
Entry12.configure(selectforeground="white")

Entry13 = Entry(Labelframe4)
Entry13.place(relx=0.236, rely=0.412, height=24, relwidth=0.666
, bordermode='ignore')
Entry13.configure(background="white")
Entry13.configure(disabledforeground="#a3a3a3")
Entry13.configure(font="TkFixedFont")
Entry13.configure(foreground="#000000")
Entry13.configure(highlightbackground="#d9d9d9")
Entry13.configure(highlightcolor="black")
Entry13.configure(insertbackground="black")
Entry13.configure(selectbackground="blue")
Entry13.configure(selectforeground="white")

Button6 = Button(Labelframe4)
Button6.place(relx=0.236, rely=0.526, height=73, width=356
, bordermode='ignore')
Button6.configure(activebackground="#ececec")
Button6.configure(activeforeground="#000000")
Button6.configure(background="#d9d9d9")
Button6.configure(command=search_command)
Button6.configure(disabledforeground="#a3a3a3")
Button6.configure(foreground="#000000")
Button6.configure(highlightbackground="#d9d9d9")
Button6.configure(highlightcolor="black")
Button6.configure(pady="0")
Button6.configure(text='''Search Record''')

Label20 = Label(root)
Label20.place(relx=0.784, rely=0.022, height=44, width=165)
Label20.configure(activebackground="#f9f9f9")
Label20.configure(activeforeground="black")
Label20.configure(background="#d9d9d9")
Label20.configure(disabledforeground="#a3a3a3")
Label20.configure(font="-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
Label20.configure(foreground="#000000")
Label20.configure(highlightbackground="#d9d9d9")
Label20.configure(highlightcolor="black")
Label20.configure(text='''Appointments''')

Labelframe2 = LabelFrame(root)
Labelframe2.place(relx=0.006, rely=0.511, relheight=0.473
, relwidth=0.317)
Labelframe2.configure(relief='groove')
Labelframe2.configure(foreground="black")
Labelframe2.configure(text='''Edit/Delete''')
Labelframe2.configure(background="#d9d9d9")

Button2 = Button(Labelframe2)
Button2.place(relx=0.316, rely=0.414, height=33, width=166
, bordermode='ignore')
Button2.configure(activebackground="#ececec")
Button2.configure(activeforeground="#000000")
Button2.configure(background="#d9d9d9")
Button2.configure(disabledforeground="#a3a3a3")
Button2.configure(command = edit)
Button2.configure(foreground="#000000")
Button2.configure(highlightbackground="#d9d9d9")
Button2.configure(highlightcolor="black")
Button2.configure(pady="0")
Button2.configure(text='''Edit''')

Button3 = Button(Labelframe2)
Button3.place(relx=0.298, rely=0.851, height=33, width=196
, bordermode='ignore')
Button3.configure(activebackground="#ececec")
Button3.configure(activeforeground="#000000")
Button3.configure(background="#d9d9d9")
Button3.configure(disabledforeground="#a3a3a3")
Button3.configure(foreground="#000000")
Button3.configure(command = delete)
Button3.configure(highlightbackground="#d9d9d9")
Button3.configure(highlightcolor="black")
Button3.configure(pady="0")
Button3.configure(text='''Delete''')

Entry6 = Entry(Labelframe2)
Entry6.place(relx=0.509, rely=0.253, height=24, relwidth=0.182
, bordermode='ignore')
Entry6.configure(background="white")
Entry6.configure(disabledforeground="#a3a3a3")
Entry6.configure(font="TkFixedFont")
Entry6.configure(foreground="#000000")
Entry6.configure(insertbackground="black")

Entry7 = Entry(Labelframe2)
Entry7.place(relx=0.509, rely=0.713, height=24, relwidth=0.182
, bordermode='ignore')
Entry7.configure(background="white")
Entry7.configure(disabledforeground="#a3a3a3")
Entry7.configure(font="TkFixedFont")
Entry7.configure(foreground="#000000")
Entry7.configure(insertbackground="black")

Label7 = Label(Labelframe2)
Label7.place(relx=0.298, rely=0.253, height=26, width=65
, bordermode='ignore')
Label7.configure(background="#d9d9d9")
Label7.configure(disabledforeground="#a3a3a3")
Label7.configure(foreground="#000000")
Label7.configure(text='''Select ID''')

Label8 = Label(Labelframe2)
Label8.place(relx=0.316, rely=0.713, height=26, width=65
, bordermode='ignore')
Label8.configure(background="#d9d9d9")
Label8.configure(disabledforeground="#a3a3a3")
Label8.configure(foreground="#000000")
Label8.configure(text='''Select ID''')

Label9 = Label(Labelframe2)
Label9.place(relx=0.298, rely=0.092, height=26, width=222
, bordermode='ignore')
Label9.configure(background="#d9d9d9")
Label9.configure(disabledforeground="#a3a3a3")
Label9.configure(font="-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
Label9.configure(foreground="#000000")
Label9.configure(text='''Edit Patient Record''')

Label10 = Label(Labelframe2)
Label10.place(relx=0.333, rely=0.552, height=34, width=195
, bordermode='ignore')
Label10.configure(background="#d9d9d9")
Label10.configure(disabledforeground="#a3a3a3")
Label10.configure(font="-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0")
Label10.configure(foreground="#000000")
Label10.configure(text='''Delete Patient Record''')

Listbox1 = Listbox(root)
Listbox1.place(relx=0.673, rely=0.087, relheight=0.901
, relwidth=0.319)
Listbox1.configure(background="white")
Listbox1.configure(disabledforeground="#a3a3a3")
Listbox1.configure(font="TkFixedFont")
Listbox1.configure(foreground="#000000")

root.mainloop()