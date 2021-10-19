# Libraries to pip install: kivy, kivymd and opencv
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivy.uix.camera import Camera
import sqlite3

### Formating variables for database functions
sqliteform = "INSERT INTO Persons (First_Name, Middle_Initial, Surname, Date_Of_Birth, Gender, Site, VacType) VALUES (?,?,?,?,?,?,?)"
####
### Conecting and creating a DB if it does not exist. Also Creating a table if it does not exist
conn = sqlite3.connect("app.db")
dbcursor = conn.cursor()
dbcursor.execute("""CREATE TABLE IF NOT EXISTS Persons (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    First_Name TEXT NOT NULL,
    Middle_Initial TEXT NOT NULL
        CHECK(length(Middle_Initial)=1),
    Surname TEXT,
    Date_Of_Birth TEXT,
    Gender TEXT CHECK (Gender IN ("M", "F")),
    Site TEXT,
    VacType TEXT CHECK (VacType IN ("ASTRAZENICA", "SINOPHARM", "PFIZER", "SINOPHARM", "JOHNSON & JOHNSON"))
        )
            """)
###
#dbcursor.execute("DROP TABLE Persons") ### Function to clear table if needed

Window.size = (412, 732) ### Function to change window size for testing, must take out when implenting as apk

### KV code for GUI layout ###
KV = '''

<MyLayout>:
    MDScreen:
        name: "main_screen"
        BoxLayout:
            orientation: "vertical"
            size: self.size
            padding: 15, 15
            spacing: 7
        
            MDToolbar:
                title: "AppName"
                # md_bg_color: app.theme_cls.primary_color
                left_action_items: [["trash-can", lambda x: root.clear_button_dialog()]]
                right_action_items: [["database-arrow-right", lambda x: root.data_button("data_screen")]]
                anchor_title: "center"
        
            MDLabel:
                text: "Please Enter/Scan Data"
                size_hint: 1, 0.1
                font_size: "15dp"
                halign: "center"
                background_color: (0.8, 0.8, 0.8, 1)
                canvas.before:
                    Color:
                        rgba: self.background_color
                    Rectangle:
                        size: self.size
                        pos: self.pos
        
            MDLabel:
                text: "NAME:"
                size_hint: 1, 0.08
                font_size: "14dp"
        
            BoxLayout:
                orientation: "horizontal"
                spacing: 7
                size_hint: 1, 0.05
                MDTextField:
                    id: f_name
                    helper_text: "First Name"
                    helper_text_mode: "persistent"
        
                MDTextField:
                    id: m_name
                    helper_text: "Middle Initial"
                    helper_text_mode: "persistent"
        
                MDTextField:
                    id: s_name
                    helper_text: "Surname"
                    helper_text_mode: "persistent"
        
            MDLabel:
                text: "DATE OF BIRTH:"
                font_size: "14dp"
                size_hint: 1, 0.09
        
            BoxLayout:
                orientation: "horizontal"
                spacing: 7
                size_hint: 1, 0.05
        
                MDTextField:
                    id: year
                    helper_text: "Year"
                    helper_text_mode: "persistent"
        
                MDTextField:
                    id: month
                    helper_text: "Month"
                    helper_text_mode: "persistent"
        
                MDTextField:
                    id: day
                    helper_text: "Day"
                    helper_text_mode: "persistent"
        
                #Label:
        
            BoxLayout:
                orientation: "horizontal"
                spacing: 7
                size_hint: 1, 0.2
        
                MDLabel:
                    text: "GENDER:"
                    font_size: "14dp"
                    size_hint: 1, 1
        
                MDTextField:
                    id: gender_id
                    hint_text: "Choose Option"
                    on_focus: if self.focus: root.drop_gender()
                    pos_hint: {"center_y": 0.5}
        
            BoxLayout:
                orientation: "horizontal"
                size_hint: 1, 0.1
                spacing: 0
        
                MDLabel:
                    text: "VACCINATION SITE:"
                    font_size: "14dp"
                    size_hint: 0.6, 1
        
                MDTextField:
                    id: site
        
            BoxLayout:
                size_hint: 1, 0.2
                spacing: 7
                MDLabel:
                    text: "VACCINATION TYPE:"
                    font_size: "14dp"
        
                MDTextField:
                    id: vac_type
                    hint_text: "Choose Option"
                    on_focus: if self.focus: root.drop()
                    pos_hint: {"center_y": 0.5}
        
        
            BoxLayout:
                spacing: 70
                size_hint: 1, 0.5
        
                MDFillRoundFlatIconButton:
                    id: camera
                    text: "ScanCard"
                    halign: "center"
                    size_hint: 1, 0.5
                    icon: "camera"
                    font_size: 15
                    on_release:
                        root.current = "camera_screen"
                        root.transition.direction = "right"
        
                MDRoundFlatIconButton:
                    id: submit
                    text: "Submit"
                    size_hint: 1, 0.5
                    font_size: 15
                    icon: "checkbox-marked"
                    on_release: root.submit()
    
    MDScreen:
        name: "camera_screen"
        BoxLayout:
            orientation: "vertical"
            padding: 7
            spacing: 0
            size: self.size
            MDToolbar:
                title: "Scan Vaccination Card"
                anchor_title: "center"
                left_action_items: [["camera-flip", lambda x: root.flip_camera()]]
                right_action_items: [["chevron-right-box", lambda x: root.back_button("main_screen")]]
            Camera: 
                id: camera_id
                resolution: (720, 1280)
                play: True
            MDFloatingActionButton:
                icon: "camera"
                pos_hint: {"center_x" : 0.5}
                size_hint_y: 0.1
                on_release: root.capture()
    
    MDScreen:
        name: "data_screen"
        BoxLayout:
            padding: 7
            orientation: "vertical"
            MDToolbar:
                title: "Database Entries"
                anchor_title: "center"
                left_action_items: [["chevron-left-box", lambda x: root.back_button2("main_screen")]]
            ScrollView:
                MDList:
                    id: container
                        
            MDFillRoundFlatButton:
                text: "Refresh"
                on_release: root.refresh()
                halign: "center" 
                pos_hint: {"center_x": 0.5}
                size_hint_y: 0.1
'''
####
Builder.load_string(KV) ### Loads the KV code ###

class MyLayout(ScreenManager):

### Dropdown option for vaccine types and gender
    def on_kv_post(self, base_widget):
        caller = self.ids.vac_type
        self.dropdown = MDDropdownMenu(
            caller = caller,
            items = [{"viewclass": "OneLineListItem", "text":"ASTRAZENICA", "on_release": lambda x=f"ASTRAZENICA": self.set_item(x)},
                     {"viewclass": "OneLineListItem", "text":"SINOPHARM", "on_release": lambda x=f"SINOPHARM": self.set_item(x)},
                     {"viewclass": "OneLineListItem", "text":"PFIZER", "on_release": lambda x=f"PFIZER": self.set_item(x)},
                     {"viewclass": "OneLineListItem", "text":"JOHNSON & JOHNSON", "on_release": lambda x=f"JOHNSON & JOHNSON": self.set_item(x)}],
            width_mult= 4
        )

        caller2 = self.ids.gender_id
        self.gender = MDDropdownMenu(
            caller = caller2,
            items = [{"viewclass": "OneLineListItem", "text": "M", "on_release": lambda x=f"M": self.set_gender(x)},
                     {"viewclass": "OneLineListItem", "text": "F", "on_release": lambda x=f"F": self.set_gender(x)}],
            width_mult = 4
        )
    def set_item(self, text_item):
        self.ids.vac_type.text = text_item
        self.dropdown.dismiss()
    def set_gender(self, text_item):
        self.ids.gender_id.text = text_item
        self.gender.dismiss()

    def drop_gender(self):
        self.gender.open()
    def drop(self):
        self.dropdown.open()
###
### Toolbar Button Functions
    def data_button(self,screen):
        self.current = screen
        self.transition.direction = "left"
    def back_button2(self, screen):
        self.current = screen
        self.transition.direction = "right"
###
### Initializing dialog for clear data confirmation pop up
    dialog1 = None
### Button to call clear data confirmation dialog
    def clear_button_dialog(self):
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title = "Clear Data?",
                buttons = [
                    MDFlatButton(text = "CANCEL", on_release = self.close_dialog),
                    MDRectangleFlatButton(text = "YES", on_release = self.confirm_clear),
                ]
            )
        self.dialog1.open()
    def close_dialog(self, obj): ### Cancel confirmation function
        self.dialog1.dismiss()
    def confirm_clear(self, obj): ### Confirm clear data function
        self.dialog1.dismiss()
        self.ids.f_name.text = ""
        self.ids.m_name.text = ""
        self.ids.s_name.text = ""
        self.ids.year.text = ""
        self.ids.month.text = ""
        self.ids.day.text = ""
        self.ids.gender_id.text = ""
        self.ids.site.text = ""
        self.ids.vac_type.text = ""
###
### CameraScreen Toolbar button functions
    def flip_camera(self):
        print("pressed")
    def back_button(self, screen):
        self.current = screen
        self.transition.direction = "left"
###
### Function for Camera button to capture image ###
    def capture(self):
        camera = self.ids.camera_id
        camera.export_to_png("./imgcapture.png")
        print("image taken")
###
### Function for refreshing the database list
    def refresh(self):
        ### Fetches data from database
        dbcursor.execute("SELECT * FROM Persons ORDER BY person_id ASC")
        records = dbcursor.fetchall() ### Assigsn data fetched to a variable
        self.ids.container.clear_widgets()
        ###
        ### Loops through variable and picks out the specific data in a specific order
        for record in records:
            self.ids.container.add_widget(
                ThreeLineListItem(text=f'{record[0]}. {record[1]} {record[2]} {record[3]}',
                                  secondary_text=f'{record[5]}  {record[4]}',
                                  tertiary_text=f'{record[6]} {record[7]}')
            )
        ###
###
### Initializing dialog for confirmation pop up
    dialog2 = None
### Submit button function to call submission confirmation dialog
    def submit(self):
        if not self.dialog2:
            self.dialog2 = MDDialog(
                title = "CONFIRM SUBMISSION",
                buttons = [
                    MDFlatButton(text = "CANCEL", on_release = self.cancel_confirm),
                    MDRectangleFlatButton(text = "CONFIRM", on_release = self.submit_confirm)
                ]
            )
        ### Initializing textfield ids to call in functions
        f_name = self.ids.f_name.text.upper()
        m_name = self.ids.m_name.text.upper()
        s_name = self.ids.s_name.text.upper()
        year = self.ids.year.text
        month = self.ids.month.text
        day = self.ids.day.text
        site = self.ids.site.text.upper()
        gender_id = self.ids.gender_id.text
        vac_type = self.ids.vac_type.text
        ###
        ### Variables for checking text variable constraints
        f_check = f_name.isalpha()
        m_check = m_name.isalpha()
        s_check = s_name.isalpha()
        y_check = year.isdigit()
        month_check = month.isdigit()
        d_check = day.isdigit()
        ###
        ### Function to prompt user to complete information if textfields are blank
        if f_name != "" and s_name != "" and m_name != "" and year != "" and month != "" and day != "" and gender_id != "" and site != "" and vac_type != "":
            temp = True
        else:
            toast("Please Complete Information")
            temp = False
        ###
        ### Check for Valid Names
        if temp == False:
            pass
        elif f_check == False or m_check == False or s_check == False:
            toast("Invalid Name")
            temp = False
        else:
            temp = True
        ###
        ### Check for length of charcter for Initial
        if temp == False:
            pass
        elif len(m_name)!= 1:
            toast("Too many characters for Initial")
            self.ids.m_name.text = ""
            temp = False
        else:
            temp = True
        ###
        ### Check for Valid Date of Births
        if temp == False:
            pass
        elif y_check == False or month_check == False or d_check == False:
            toast("Invalid Date of Birth")
            self.ids.year.text = ""
            self.ids.month.text = ""
            self.ids.day.text = ""
            temp = False
        else:
            temp = True

        if temp == False:
            pass
        elif int(year) > 2009 or int(year) < 1921:
            toast("Invalid Date of Birth, Age out of Range")
            self.ids.year.text = ""
            temp = False
        else:
            temp = True

        if len(day) > 2 or len(month) > 2:
            toast("Invalid Date Of Birth")
            self.ids.day.text = ""
            self.ids.month.text = ""
            temp = False
        else:
            pass

        if temp == False:
            pass
        elif int(month)>12 or int(month)<1:
            toast("Invalid Date of Birth, Invalid Month")
            self.ids.month.text = ""
            temp = False
        elif (int(month)==1 or int(month)==3 or int(month)==5 or int(month)==7 or int(month)==8 or int(month)==10 or int(month)==12) and (int(day)<1 or int(day)>31):
            toast("Invalid Date of Birth, Invalid Day")
            self.ids.day.text = ""
            temp = False
        elif int(month)==2 and (int(day)<1 or int(day)>29):
            toast("Invalid Date of Birth, Invalid Day")
            self.ids.day.text = ""
            temp = False
        elif (int(month)==4 or int(month)==6 or int(month)==9 or int(month)==11) and (int(day)<1 or int(day)>30):
            toast("Invalid Date of Birth, Invalid Day")
            self.ids.day.text = ""
            temp = False

        else:
            temp = True
        ###
        ### Check for Valid Gender
        if temp == False:
            pass
        elif gender_id not in ['M','F']:
            toast("Invalid Gender")
            self.ids.gender_id.text = ""
            temp = False
        else:
            temp = True
        ###
        ### Check for valid Vaccine
        if temp == False:
            pass
        elif vac_type not in ['PFIZER', 'SINOPHARM', 'ASTRAZENICA', 'JOHNSON & JOHNSON']:
            toast("Invalid Vaccination")
            self.ids.vac_type.text = ""
            temp = False
        else:
            temp = True
        ###
        ### After all checks pass, confirmation dialog is opened
        if temp == False:
            pass
        else:
            self.dialog2.open()
    ###
    ### Cancel submission function
    def cancel_confirm(self,obj):
        self.dialog2.dismiss()
    ###
    ### Confirm submission function
    def submit_confirm(self,obj):
        ### Initializing textfield ids to call in functions
        f_name = self.ids.f_name.text.upper()
        m_name = self.ids.m_name.text.upper()
        s_name = self.ids.s_name.text.upper()
        year = self.ids.year.text
        month = self.ids.month.text
        day = self.ids.day.text
        site = self.ids.site.text
        gender_id = self.ids.gender_id.text.upper()
        vac_type = self.ids.vac_type.text.upper()
        ###
        ### Variables to format for proper execution of writing to database function
        test_k = (f_name, m_name, s_name, str(year+"/"+month+"/"+day), gender_id, site, vac_type)
        dob = str(year+"/"+month+"/"+day)
        ###
        ### If Statements to format birthdates and months correctly if user enters values less than 10
        if (int(day)<10 and int(month)>10 and len(day)<2) or (int(day)<10 and int(month)<10 and len(day)<2 and len(month)==2):
            test_k = (f_name, m_name, s_name, str(year+"/"+month+"/0"+day), gender_id, site, vac_type)
            dob = str(year+"/"+month+"/0"+day)
        elif (int(month)<10 and int(day)>10 and len(month)<2) or (int(day)<10 and int(month)<10 and len(month)<2 and len(day)==2):
            test_k = (f_name, m_name, s_name, str(year+"/0"+month+"/"+day), gender_id, site, vac_type)
            dob = str(year+"/0"+month+"/"+day)
        elif int(day)<10 and int(month) <10 and len(day)<2 and len(month)<2:
            test_k = (f_name, m_name, s_name, str(year+"/0"+month+"/0"+day), gender_id, site, vac_type)
            dob = str(year+"/0"+month+"/0"+day)
        ###
        ### Opens Confirmation Dialog.
        self.dialog2.dismiss()
        ###
        ### Function to check if first name, middle initial, surname and date of birth already exist
        dbcursor.execute("SELECT First_Name, Middle_Initial, Surname, Date_Of_Birth FROM Persons WHERE "
                         "First_Name=? AND Middle_Initial=? AND Surname=? AND Date_Of_Birth=?", (f_name, m_name, s_name, dob))
        exists = dbcursor.fetchone()
        ###
        ### Try block to submit data to database
        if not exists:
            try:
                dbcursor.execute(sqliteform, test_k)
                conn.commit()
                toast("Submitted")
            except sqlite3.IntegrityError:
                toast("Too many characters for Initial")
                self.ids.m_name.text = ""
        else:
            toast("Entry Already Exists!")
    ###
### App class to build app
class TestApp(MDApp):
    def build(self):
        return MyLayout()
TestApp().run()
