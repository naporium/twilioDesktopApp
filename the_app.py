#!/usr/bin/python3
# feedback_template.py by Barron Stone
# lynda.com

# SOURCE TO TABLES: https://www.activestate.com/resources/quick-reads/how-to-display-data-in-a-table-using-tkinter/

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from jinja2 import Environment
from datetime import datetime
import os
import sys
from config import Config

from csvTools import (readTemplate,
                      getCsvData,
                      ExtractValidJinja2Variabbles,
                      read_raw_data_from_template,
                      isAnyHeader_inJinjaTemplate,
                      searchHeaders,
                      isContact_var_CsvHeaders,
                      contruct_messages,
                      )

from twilioSendMessage import send_message, run_send_a_message



# self.templt_file_name      # name to jinja 2 template
# self.full_path_template    # full path to jinja 2 template
# self.csv_file_name_value   # csv full path
# self.csv_file              # csv FULL PATH
# self.csv_f_name            # csv file name


class SmsAutomatic:
    def __init__(self, master):

        master.title('SMSAUTOMATIC')
        master.resizable(False, False)
        master.configure(background = '#e1d8b9')
        master.geometry("1200x600")

        self.ROOT_DIR = Config.ROOT_DIR
        print(f"[self.ROOT_DIR] {self.ROOT_DIR}")
        print(f"[self.TEMPLATE_FOLDER] {Config.TEMPLATE_FOLDER}")

        self.isNewDataWindowOpened = False

        self.frame_header = ttk.Frame(master=master)
        self.frame_header.pack()
        self.frame_header.config(width=400, height=400, relief=GROOVE)
        # create the window header
        self.header = ttk.Label(self.frame_header, text="CSV SMS SENDER 0.0.1", font=("Arial Bold", 24))
        self.header.pack( ipady=0, pady=15, padx=0)
        self.header.configure(foreground="Blue", width=25)
        # create the Description
        message1 = "We can send sms, to cell phones.\nHow it works? Please,follow the steps bellow." \
                   "\nDocumentation is available for details."

        descr = ttk.Label(self.frame_header, text=message1, font=("Arial Bold", 16), )
        descr.pack(side="top", ipady=5, padx=20, pady=20)

        # NOTEBOOK WIDGET
        self.notebook = ttk.Notebook(master=master)
        self.notebook.pack(pady=30)
        self.notebook.config(height=600, width=400)
        # @
        #   TAB 1 STEP 1
        self.tab1 = ttk.Frame(self.notebook, )
        self.tab1.pack()
        self.tab1.config(height=600, width=400)
        # create the window header
        tab1_description = ttk.Label(self.tab1,
                                    text="Select one .csv file",
                                    font=("Arial Bold", 12))
        tab1_description.pack(side="top", ipady=10, padx=30, )
        tab1_description.configure(foreground="blue")

        # Draw the button that opens the file picker)
        open_files = ttk.Button(self.tab1, text="choose .csv files", command=self.clicked)
        open_files.pack(fill="x")

        cancelbtn = ttk.Button(self.tab1, text="Exit", command=self.cancel_operation)
        cancelbtn.pack(fill="x")

        # @@
        # TAB 2 STEP 2
        self.tab2 = ttk.Frame(self.notebook)
        self.tab2.config(height=600, width=400)
        # create the window header
        tab2_description = ttk.Label(self.tab2, text="Select a template message", font=("Arial Bold", 12))
        tab2_description.pack(side="top", ipady=10, padx=30, )
        tab2_description.configure(foreground="blue")

        # add buttons
        self.templates_message_files = StringVar()
        combobox = ttk.Combobox(self.tab2, textvariable=self.templates_message_files)
        combobox.pack(fill="x")
        self.j2_values = self.load_values_for_drop_down()
        combobox.config(values = self.j2_values)
        self.templates_message_files.set( self.j2_values[0])

        # Draw the button that opens the file picker)
        open_files = ttk.Button(self.tab2, text="Select file and go to Step3", command=self.gotoStep3)
        open_files.pack(fill="x")
        cancelbtn = ttk.Button(self.tab2, text="Exit", command=self.cancel_operation)
        cancelbtn.pack(fill="x")

        # @@@
        # TAB 3 STEP 3
        self.tab3 = ttk.Frame(self.notebook, height="600")

        self.frame1 = ttk.Frame(self.tab3, height="300")
        self.frame1.pack()

        self.frame1_btn1_load_data = ttk.Button(master=self.frame1, text="Load Data", command=lambda: self.openNewWindow(master))
        self.frame1_btn1_load_data.pack(fill="x")
        cancelbtn1 = ttk.Button(self.frame1, text="Exit", command=self.cancel_operation)
        cancelbtn1.pack(fill="x")


        # ADD FRAMES TO THE NOTEBOOK
        # TODO: ADD a feature that allows users to add a new template message,
        self.notebook.add(self.tab1, text="Step 1")
        self.notebook.add(self.tab2 , text="Step 2")
        self.notebook.add(self.tab3, text="Step 3")
        self.notebook.tab(0, state="normal")    # Active mode/normal state
        self.notebook.tab(1, state="disabled")  # turn on inactive mode
        self.notebook.tab(2, state="disabled")  # turn on inactive mode

    def cancel_operation(self):
        sys.exit()

    def show_results(self, text):
        messagebox.showinfo("Results", text)

    def show_error(self, text):
        messagebox.showerror("error", text)

    def clicked(self):
        """
        # Open the file picker and sen the selected files to the process_files function
        :return:
        """
        self.csv_file = filedialog.askopenfilename()
        self.process_files(self.csv_file)
        # WE CAN LOAD THE DATA HERE INSTEAD
        self.csv_f_name = self.csv_file.split("/")[-1]

        # mudar tab
        # desactivar tab 1
        self.notebook.tab(1, state="normal")
        self.notebook.select(1)
        # alterara as propriedades de uma notebook tab
        # é equivalente ao .configure dos outros widgets
        self.notebook.tab(0, state="disabled")  # desactivar
        self.notebook.tab(1, state="normal")  # desactivar

    def process_files(self, file_name):
        # TODO
        #  DELETE THIS FUNCTION or processa data here or in clicked method
        print(f"[ OUTPUT - File to Process] - {file_name}")

        # ERASE

    def load_values_for_drop_down(self):

        template_file_paths = Config.TEMPLATE_FOLDER  # default is "MessageTemplates"
        print("template_file_paths", template_file_paths)
        if not os.path.exists(template_file_paths):
            self.show_error("A pasta para mensagens 'template' nao existe")
            self.cancel_operation()
        elif not os.path.isdir(template_file_paths):
            self.show_error("Existe um ficheiro de nome MessageTemplates. Deverá ser uma pasta")
            self.cancel_operation()
        else:
            files_lst = os.listdir(template_file_paths)
            print("files_lst", files_lst)
            return files_lst

    def gotoStep3(self):
        self.notebook.tab(2, state="normal")  # DEACTIVATE TAB
        self.notebook.select(2)
        self.notebook.tab(1, state="disabled")  # DEACTIVATE TAB
        self.resultado_escolhido_do_drop_down = self.templates_message_files.get()  # Which file, User have choosen from Dropdown
        self.template_full_path = os.path.join(self.ROOT_DIR, Config.TEMPLATE_FOLDER)
        self.template_full_path = os.path.join(self.template_full_path, self.resultado_escolhido_do_drop_down)

    def loadFrame1Data(self):
        self.templt_file_name_value = ttk.Label(master=self.frame1, text="template name:", font=("Arial Bold", 14))
        self.templt_file_name_value.grid(row=1, column=0)

        self.templt_file_name = ttk.Label(master=self.frame1, text=self.template_full_path, font=("Arial italic", 14))
        self.templt_file_name.grid(row=1,column=1)
        self.csv_file_name = ttk.Label(master=self.frame1, text="csv file").grid(row=2, column=0)
        self.csv_file_name_value = ttk.Label(master=self.frame1, text=self.csv_file).grid(row=2, column=1)

    def fake_send_message(self,):
        # TODO
        #  When not to send real messages
        self.report_file_name = str(datetime.now()) + "Report.csv"
        report_file_path = os.path.join(self.ROOT_DIR, Config.REPORT_FOLDER)
        self.report_file_path = os.path.join(report_file_path, self.report_file_name)
        # WRITE REPORT IN CSV FILE
        write_csv_fake_report(self.report_file_path, self.data_messages)

    # def send_message(self,):
    #     # TODO
    #     self.report_file_name = str(datetime.now()) + "Report.csv"
    #     report_file_path = os.path.join(self.ROOT_DIR, Config.REPORT_FOLDER)
    #     self.report_file_path = os.path.join(report_file_path, self.report_file_name)
    #     # WRITE REPORT IN CSV FILE
    #
    #     for row in self.data_messages:
    #         message = send_message(to_send_number=row[1], body_message=row[0])
    #         print("message[0]: ", message[0])
    #         print("message[0].sid: ", message[0].sid)
    #         print("message[1].message.sid: ", message[1])
    #
    #     write_csv_fake_report(self.report_file_path, self.data_messages)


    def onclose(self, win):
        """ #Func to be called when window is closing, passing the window name"""
        # Set it to close
        self.isNewDataWindowOpened = False
        win.destroy()  # Destroy the window

    def openNewWindow(self, master):
        """
        function to open a new windown on a button click
        :param master:
        :return: <None>
        """
        # self.templt_file_name      # name to jinja 2 template
        # self.full_path_template    # full path to jinja 2 template
        # self.csv_file_name_value   # csv full path
        # self.csv_file              # csv FULL PATH
        # self.csv_f_name            # csv file name

        if self.isNewDataWindowOpened == False:

            #self.frame1_btn1_load_data.state(DISABLED)
            # Toplevel object which will
            # be treated as a new window
            self.newWindow = Toplevel(master)

            # sets the title of the
            # Toplevel widget
            self.newWindow.title("Data in Files")

            # sets the geometry of toplevel
            self.newWindow.geometry("1200x770")

            self.newWindow.resizable(False, False)

            # A Label widget to show in toplevel
            #Label(master=self.newWindow,
            #      text="This is a new window").pack()

            #
            # PREPARE TO LOAD DATA
            csv = self.csv_file  # csv full file path chosen by user
            j2template = self.template_full_path  # jinja template full file path chosen by user

            # TODO: Adjust Backend functions to Load data, and GUI
            #  i)   Create a new frame in Gui with a DROP BOX FOR ALLOWED
            #        headers found both in csv file and template   ???
            #  ii)  SHOW WARNING IF ERRORS WHILE READING CSV DATA
            #  iii) SHOW WARNING IF ERRORS WHILE READING TEMPLATES
            #  iv)  SHOW WARNING if only not all variables corresponds to header
            #  v)   SHOW WARNING IF template as a variable and not correspond to any header
            #  #
            #  1. CREATE/ADAPT existing FUNCTION THAT catches cell phone numbers for twilio,
            #     and compose messages
            #  1.1. This function also should say how many chars / streams for each message
            #  1.2  Average chars in messages
            #  1.3  Prevision total Cost for each message
            #  1.4  Prevision total cost for all messages
            #  1.5  REFLECT this data in GUI

            # LOAD DATA FROM CSV FILE
            try:
                headers, csv_data, row_counter = getCsvData(file_name=csv)
            except OSError as error:
                print("Error", error)
                raise ValueError( "Error while attempting to read csv file")
            #
            # LOAD DATA FROM TEMPLATE
            print(f"[OUTPUT] self.csv_file: {self.csv_file}")
            print(f"[OUTPUT]  self.template_full_path : { self.template_full_path }")
            print(f"[OUTPUT] headers: {headers}")
            print(f"[OUTPUT] csv_data: {csv_data}")
            print(f"[OUTPUT] row_counter: {row_counter}")
            raw_jinja2_template_data = read_raw_data_from_template(j2template)
            print(f"[OUTPUT] raw_jinja2_template_data: {raw_jinja2_template_data}")

            vars_names, results = ExtractValidJinja2Variabbles(raw_jinja2_template_data)
            headers_versus_template_vars = isAnyHeader_inJinjaTemplate(headers=headers, template_vars=vars_names)

            if headers_versus_template_vars == []:
                headers_versus_template_vars = "CSV HEADERS NAME DON T MACTH WITH ANY OF TEMPLATE VARIABLES"
                print(headers_versus_template_vars)
            # COMMENT
            recompiled_searced_headers = searchHeaders(headers=headers, patterns=vars_names)
            print(f"[ recompiled_searced_headers ] :{ recompiled_searced_headers}")
            # FALSE if contact is not in vas True otherwhise
            boolean_state, found_contact_present = isContact_var_CsvHeaders(headers)
            if boolean_state is True:
                is_contact_present = (found_contact_present, "We have found:  ['contact''] in CSV HEADERS. We will use the number to send message")
                self.CONTACTO_CSV_NAME = found_contact_present[0][0]
                print(f"self.CONTACTO_CSV_NAME: {self.CONTACTO_CSV_NAME}")
            else:
                is_contact_present = (found_contact_present, "We didn 't have found any ['contact'] in CSV headers ")

            #if boolean_state is True:
            self.data_messages = contruct_messages(csv_file=self.csv_file,
                                              template_name=self.resultado_escolhido_do_drop_down,
                                              recompiled_searced_headers=recompiled_searced_headers,
                                              csv_contact_header=self.CONTACTO_CSV_NAME)


            # data_messages --> list
            # [<message>, <phone_number>, <number of chars in message>, <segment>]
            print(self.data_messages)

# COMPOSE FINAL MESSAGE

            # #### BEGIN GUI
            # ##
            # ### CSV DATA
            main_frame = ttk.Frame(master=self.newWindow)
            main_frame.configure(width="700", height="400")
            main_frame.pack(fill="x")

            empty = ttk.Label(master=main_frame,
                              text="CSV FILE DATA",
                              font=("Arial Bold", 12))
            empty.pack(side="top", ipady=10, padx=30, )
            empty.configure(foreground="blue")

            frameX = ttk.Frame(master=self.newWindow, relief="groove")
            frameX.configure(width="700", height="400")
            frameX.pack(fill="x", padx="10")

            csv_file_name = ttk.Label(master=frameX, text="CSV FILENAME", width="20")
            csv_file_name.grid(row=0, column=0, pady=5)
            entry = Entry(master=frameX, relief=GROOVE, width=100)
            entry.grid(row=0, column=1, padx="10", columnspan=100)
            entry.insert(END, '%s' % (csv.split("/")[-1]))

            csv_full_path = ttk.Label(master=frameX, text="CSV FILEPATH", width="20")
            csv_full_path.grid(row=1, column=0, pady=5, padx=20)
            entry1 = Entry(master=frameX, relief=GROOVE, width=100, )
            entry1.grid(row=1, column=1, padx="10", columnspan=100)
            entry1.insert(END, '%s' % (csv))

            h = ttk.Label(master=frameX, text="HEADERS", width="20")
            h.grid(row=2, column=0, pady=5)
            he = Entry(master=frameX, relief=GROOVE, width=100)
            he.grid(row=2, column=1, padx="10", columnspan=50)
            he.insert(END, '%s' % headers)

            nr = ttk.Label(master=frameX, text="DATA ROW #", width="20")
            nr.grid(row=3, column=0, pady=5)
            ntr = Entry(master=frameX, relief=GROOVE, width=100)
            ntr.grid(row=3, column=1, padx="10", columnspan=50)
            ntr.insert(END, '%d' % row_counter)

            # ###
            # ### TEAMPLATE MESSAGE
            main_frame2 = ttk.Frame(master=self.newWindow)
            main_frame2.configure(width="700", height="400")
            main_frame2.pack(fill="x")

            empty2 = ttk.Label(master=main_frame2,
                               text="TEMPLATE MESSAGE",
                               font=("Arial Bold", 12))
            empty2.pack(side="top", ipady=10, padx=30, )
            empty2.configure(foreground="blue")

            frameY = ttk.Frame(master=self.newWindow, relief="groove")
            frameY.configure(width="700", height="400")
            frameY.pack(fill="x", padx="10")

            tpl_name = ttk.Label(master=frameY, text="TEMPLATE NAME", width="20")
            tpl_name.grid(row=0, column=0, pady=5)
            tpl_entry = Entry(master=frameY, relief=GROOVE, width=100)
            tpl_entry.grid(row=0, column=1, padx="10", columnspan=100)
            tpl_entry.insert(END, '%s' % (j2template.split("/")[-1]))

            tpl_full_path = ttk.Label(master=frameY, text="TEMPLATE FILEPATH", width="20")
            tpl_full_path.grid(row=1, column=0, pady=5, padx=20)
            tpl_entry1 = Entry(master=frameY, relief=GROOVE, width=100, )
            tpl_entry1.grid(row=1, column=1, padx="10", columnspan=100)
            tpl_entry1.insert(END, '%s' % j2template)

            # LOAD MESSAGE DATA: CALL:
            ## vars_name ,raw_jinja2_template_data

            #print(j2template.split("/")[-1])
            self.message = readTemplate(template_name=j2template.split("/")[-1])
            self.message = self.message.split("\n")[0]

            raw_message = ttk.Label(master=frameY, text="RAW MESSAGE", width="20")
            raw_message.grid(row=2, column=0, pady=5)
            raw_message = Entry(master=frameY, relief=GROOVE, width=100)
            raw_message.grid(row=2, column=1, padx="10", columnspan=50)
            raw_message.insert(END, '%s' % raw_jinja2_template_data)

            t_var = ttk.Label(master=frameY, text="TEMPLATE VARS", width="20")
            t_var.grid(row=3, column=0, pady=5)
            t_var = Entry(master=frameY, relief=GROOVE, width=100)
            t_var.grid(row=3, column=1, padx="10", columnspan=50)
            t_var.insert(END, '%s' % ", ".join(vars_names))

            mens_ = ttk.Label(master=frameY, text="APROX. CHAR NUMBER", width="20")
            mens_.grid(row=4, column=0, pady=5)
            mesn_number = Entry(master=frameY, relief=GROOVE, width=100)
            mesn_number.grid(row=4, column=1, padx="10", columnspan=50)
            mesn_number.insert(END, '%d' % len(self.message))

            # ###
            # ### SEND MESSAGE
            main_frame3 = ttk.Frame(master=self.newWindow)
            main_frame3.configure(width="700", height="400")
            main_frame3.pack(fill="x")

            #if is_contact_present is True:
            empty3 = ttk.Label(master=main_frame3,
                               text="READY TO SEND MESSAGES",
                               font=("Arial Bold", 12))
            empty3.pack(side="top", ipady=10, padx=30, )
            empty3.configure(foreground="blue")
            #else:
            #     empty3 = ttk.Label(master=main_frame3,
            #                        text="NOT READY TO SEND MESSAGES",
            #                        font=("Arial Bold", 12))
            #     empty3.pack(side="top", ipady=10, padx=30, )
            #     empty3.configure(foreground="red")
            # # TODO
            #  PREPARE DATA TO SEND MESSAGES
            #  GET TEMPLATE MESSAGE AND NUMBER TO SEND [list]
            frameZ = ttk.Frame(master=main_frame3, relief="groove")
            frameZ.configure(width="900", height="400")
            frameZ.pack(fill="x", padx="10")

            headVtempl= ttk.Label(master=frameZ, text="HEADERS VERSUS VARS", width="30")
            headVtempl.grid(row=0, column=0, padx=5 ,pady=5)
            headVtempl_entry = Entry(master=frameZ, relief=GROOVE, width=100)
            headVtempl_entry.grid(row=0, column=1, padx="10", columnspan=100)
            headVtempl_entry.insert(END, '%s' % headers_versus_template_vars)

            fmhv = ttk.Label(master=frameZ, text="FORCE MATCH VARS IN HEADERS", width="30")
            fmhv.grid(row=1, column=0, padx=5 ,pady=5)
            fmhv_entry = Entry(master=frameZ, relief=GROOVE, width=100)
            fmhv_entry.grid(row=1, column=1, padx="10", columnspan=100)
            fmhv_entry.insert(END, '%s' % recompiled_searced_headers)

            findContact = ttk.Label(master=frameZ, text="Final Destination cellphone number", width="30")
            findContact.grid(row=2, column=0, padx=5 ,pady=5)
            findContact_entry = Entry(master=frameZ, relief=GROOVE, width=100)
            findContact_entry.grid(row=2, column=1, padx="10", columnspan=100)
            findContact_entry.insert(END, '%s' '%s' % (str(is_contact_present[0]), str(is_contact_present[1])))

            # [<message>, <phone_number>, <number of chars in message>, <segment>]
            #print(self.data_messages)
            # TODO: Here we should arrange a widget with elevator
            #for count, line in enumerate(self.data_messages, start=3):
            #    temp_var = "L" + str(count)
            #    temp_var_entry = temp_var + "_e"
            #    temp_var = ttk.Label(master=frameZ, text="DATA TO SEND", width="30")
            #    temp_var.grid(row=count, column=0, padx=5, pady=5)
            #    temp_var_entry = Entry(master=frameZ, relief=GROOVE, width=100)
            #    temp_var_entry.grid(row=count, column=1, padx="10", columnspan=100)
            #    temp_var_entry.insert(END, '[MESSAGE] %s ' ' [PHONENUMBER]%s ' ' [#CHARS] %s ' ' [SEGMENT]%s '% (str(line[0]), str(line[1]),str(line[2]), str(line[3])))

            # recompiled_searced_headers
            # INSERT SEND MESSAGE BUTTON
            # btn3 = ttk.Button(master=main_frame3, text="SEND MESSAGE(S)", command=self.fake_send_message)
            btn3 = ttk.Button(master=main_frame3,
                              text="SEND MESSAGE(S)",
                              command=lambda: run_send_a_message(self.data_messages))
            btn3.pack()

            self.isNewDataWindowOpened = True
            self.newWindow.protocol('WM_DELETE_WINDOW',
                                    lambda: self.onclose(self.newWindow))  # If it is closed then set it to False
        else:
            pass


def setup():
    # validate folder
    env = Environment()
    with open(sys.argv[1]) as template:
        env.parse(template.read())

    # TODO
    #  1 . validate template folder read write permissions, and existence. (create folder)
    #  2 . Check for available/readable templates (Create a template for example purposes)
    #  3 . Check for Available twilio Env variables
    #  4 . Check that tkinter is available in OS
    #  5 . Check that twilio is installed


def main():
    root = Tk()
    feedback = SmsAutomatic(root)
    root.mainloop()


if __name__ == "__main__":
    main()
