from tkinter import *
from tkinter import ttk
from contact_manager import Contact



class Interface:
    

    def __init__(self, data_query=Contact):

        self.data_query = data_query
        self.win = Tk()
        self.win.title('Contact List')
        self.win.config(bg="#42bcf5")
        self.win.minsize(600, 400)
        self.win.config(padx=10)
        self.win.geometry('640x500')
        self.win.resizable(width=False,height=False)
        self.create_left_icon()
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.style = ttk.Style()
        self.create_scrollbar()
        self.create_bottom_buttons()
        self.view_contacts()
        self.win.mainloop()


    def create_left_icon(self):
        photo = PhotoImage(file='Logo.gif')
        self.label = Label(image=photo)
        self.label.image = photo
        self.label.grid(row=0, column=0, padx=20, pady=20)

    def create_label_frame(self):
        self.labelframe = LabelFrame(text='Create New Contact', bg="#42bcf5", font='helvetica 10')
        self.labelframe.grid(row=0, column=1, padx=8, pady=20)
        self.name_labelfield = Label(self.labelframe, text='Name: ', bg='sky blue', fg='black')
        self.name_labelfield.grid(row=1, column=1, sticky='W', padx=2, pady=8)
        self.namefield = Entry(self.labelframe, width=40)
        self.namefield.grid(row=1, column=2, padx=15, pady=1)

        self.email_labelfield = Label(self.labelframe, text='Email: ', bg='sky blue', fg='black')
        self.email_labelfield.grid(row=2, column=1, sticky='W', padx=2, pady=8)
        self.emailfield = Entry(self.labelframe, width=40)
        self.emailfield.grid(row=2, column=2, padx=15, pady=1)

        self.num_labelfield = Label(self.labelframe, text='Tel.Number: ', bg='sky blue', fg='black')
        self.num_labelfield.grid(row=3, column=1, sticky='W', padx=2, pady=8)
        self.numfield = Entry(self.labelframe, width=40)
        self.numfield.grid(row=3, column=2, padx=15, pady=10)
        self.add_button = Button(self.labelframe, text='Add Contact', bg='blue', fg='white', width=50,
                                 command=self.on_add_contact_button_clicked)
        self.add_button.grid(row=4, column=1, columnspan=2, pady=5)

    def create_message_area(self):
        self.message = Label(text='', bg="#42bcf5", fg='black')
        self.message.grid(row=3, column=1)

    def create_tree_view(self):
        tree = self.tree = ttk.Treeview(height=10, columns=('email', 'number'))
        self.tree.grid(row=6, column=0, columnspan=3,)
        self.tree.heading('#0', text='Name', anchor=W, )
        self.tree.heading('email', text='Email Address', anchor=W)
        self.tree.heading('number', text='Contact Number', anchor=W)
        return tree




    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=6, column=3, columnspan=10, sticky='sn')

    def create_bottom_buttons(self):
        self.delete_button = Button(text='Delete Slected', command=self.on_delete_selected_button_clicked, bg="#42bcf5",
                                    fg='black')
        self.delete_button.grid(row=8, column=0, sticky=W, padx=20, pady=10)

        self.modify_button = Button(text='Modify Slected', command= self.open_modify_window, bg='purple', fg='white')
        self.modify_button.grid(row=8, column=1, sticky=E, padx=20, pady=10)

    def on_add_contact_button_clicked(self):
        self.add_new_contact()

    def on_delete_selected_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return

        self.delete_contact()

    def add_new_contact(self):
        if self.new_contacts_validated():
            query = 'INSERT INTO contact_list VALUES(NULL,?,?,?)'
            parameters = (self.namefield.get(), self.emailfield.get(), self.numfield.get())
            self.data_query.execute_db_query(query, parameters)
            self.message['text'] = 'New Contact {} added'.format(self.namefield.get())
            self.namefield.delete(0, END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
            self.view_contacts()

        else:
            self.message['text'] = '   name, email or number cannot be blank'

    def new_contacts_validated(self):
        return len(self.namefield.get()) > 1 and len(self.emailfield.get()) > 4 and len(self.numfield.get()) > 5

    def view_contacts(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM contact_list ORDER BY name desc'
        contact_entriers = self.data_query.execute_db_query(query)
        for row in contact_entriers:
            self.tree.insert('', 0, text=row[1], values=([2], row[3]))

    def delete_contact(self):
        print('hoi')
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contact_list WHERE name= ?'
        self.data_query.execute_db_query(query, (name,))
        self.message['text'] = f'Contact for {name} deleted'
        self.view_contacts()

    def open_modify_window(self):
        name = self.tree.item(self.tree.selection())['text']
        old_number = self.tree.item(self.tree.selection())['values'][1]
        self.transient = Toplevel()
        self.transient.title('Update Contact')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)




        Label(self.transient, text='Old Contact Number:').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_number), state='readonly').grid(row=1, column=2)


        Label(self.transient, text='New Phone Number:').grid(
            row=2, column=1)
        new_phone_number_entry_widget = Entry(self.transient)
        new_phone_number_entry_widget.grid(row=2, column=2)


        Button(self.transient, text='Update Contact', command=lambda: self.update_contacts(
            new_phone_number_entry_widget.get(), old_number, name)).grid(row=3, column=2, sticky=E)


        self.transient.mainloop()

    def update_contacts(self, newphone, old_phone,name):
        query = 'UPDATE contact_list SET number=? WHERE number =? AND name =?'
        parameters = (newphone, old_phone, name)
        self.data_query.execute_db_query(query, parameters)
        self.transient.destroy()
        self.message['text'] = 'Phone number of {} modified'.format(name)
        self.view_contacts()

