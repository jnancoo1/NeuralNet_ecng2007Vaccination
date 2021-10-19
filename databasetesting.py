# Libraries to install: kivy, kivymd
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
import sqlite3
from kivy.core.window import Window

from kivymd.uix.list import ThreeLineListItem

Window.size=(412,732)

sqliteform = "INSERT INTO Persons (First_Name, Middle_Initial, Surname, Date_Of_Birth, Gender, Site, VacType) VALUES (?,?,?,?,?,?,?)"
conn = sqlite3.connect("test.db")
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
#dbcursor.execute("DROP TABLE Persons")

KV = '''

<MyLayout>:
    MDScreen:
        name: "screen1"
        BoxLayout:
            orientation: "vertical"
            size: self.size
            MDTextField:
                id: f_name
                helper_text: "First"
                helper_text_mode: "persistent"

            MDTextField:
                id: m_name
                helper_text: "Middle"
                helper_text_mode: "persistent"

            MDTextField:
                id: s_name
                helper_text: "Last"
                helper_text_mode: "persistent"
                
            MDTextField:
                id: year
                helper_text: "year"
                helper_text_mode: "persistent"
                
            MDTextField:
                id: month
                helper_text: "Month"
                helper_text_mode: "persistent"
                
            MDTextField:
                id: day
                helper_text: "Day"
                helper_text_mode: "persistent"
                
            MDTextField:
                id: gender
                helper_text: "Gender"
                helper_text_mode: "persistent"

            MDTextField:
                id: site
                helper_text: "Site"
                helper_text_mode: "persistent"

            MDTextField:
                id: type
                helper_text: "Type"
                helper_text_mode: "persistent"
                
            BoxLayout:
                orientation: "horizontal"
                MDRaisedButton:
                    id: submit
                    text: "Submit"
                    on_release: root.submit()
                MDRaisedButton:
                    id: switch
                    text: "Switch"
                    on_release:
                        root.current = "screen2"
    
    MDScreen:
        name: "screen2"
        BoxLayout:
            orientation: "vertical"
            spacing : 0
            MDToolbar: 
                title: "Database"
                left_action_items: [["chevron-left-box", lambda x: root.back_button("screen1")]]
            
            ScrollView:
                MDList:
                    id: container
                        
            MDRaisedButton:
                text: "Refresh"
                on_release: root.refresh()
                halign: "center"  

<Content>:
    orientation: "horizontal"
    MDLabel: 
        id: name_exp
              
'''
Builder.load_string(KV)

class Content(BoxLayout):
    pass

class MyLayout(ScreenManager):

    def refresh(self):

        dbcursor.execute("SELECT * FROM Persons ORDER BY person_id ASC")
        records = dbcursor.fetchall()
        self.ids.container.clear_widgets()

        for record in records:
            self.ids.container.add_widget(
                ThreeLineListItem(text=f'{record[0]}. {record[1]} {record[2]} {record[3]}',
                                  secondary_text=f'{record[5]}  {record[4]}',
                                  tertiary_text=f'{record[6]} {record[7]}')
            )



    def submit(self):
        f_name = self.ids.f_name.text.upper()
        m_name = self.ids.m_name.text.upper()
        s_name = self.ids.s_name.text.upper()
        year = self.ids.year.text
        month = self.ids.month.text
        day = self.ids.day.text
        site = self.ids.site.text
        gender = self.ids.gender.text.upper()
        vac = self.ids.type.text.upper()

        f_check = f_name.isalpha()
        m_check = m_name.isalpha()
        s_check = s_name.isalpha()
        y_check = year.isdigit()
        month_check = month.isdigit()
        d_check = day.isdigit()

        test_k = (f_name, m_name, s_name, str(year+"/"+month+"/"+day), gender, site, vac)
        dob = str(year+"/"+month+"/"+day)

        if f_check == False or m_check == False or s_check == False:
            toast("Invalid Name")
            temp = False
        else:
            temp = True

        if temp == False:
            pass
        elif len(m_name)!= 1:
            toast("Too many characters for Initial")
            self.ids.m_name.text = ""
        else:
            temp = True

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
        elif int(year) > 2008 or int(year) < 1920:
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
        elif int(day) < 10 and int(month) > 10:
            test_k = (f_name, m_name, s_name, str(year+"/"+month+"/0"+day), gender, site, vac)
            dob = str(year+"/"+month+"/0"+day)
            temp = True
        elif int(month) < 10 and int(day) > 10:
            test_k = (f_name, m_name, s_name, str(year+"/0"+month+"/"+day), gender, site, vac)
            dob = str(year+"/0"+month+"/"+day)
            temp = True
        elif int(day) < 10 and int(month) < 10:
            test_k = (f_name, m_name, s_name, str(year+"/0"+month+"/0"+day), gender, site, vac)
            dob = str(year+"/0"+month+"/0"+day)
            temp = True

        if temp == False:
            pass
        elif len(year) > 4:
            toast("Invalid Date of Birth")
            self.ids.year.text = ""
            temp = False
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

        if temp == False:
            pass
        elif gender not in ['M','F']:
            toast("Invalid Gender")
            self.ids.gender.text = ""
            temp = False
        else:
            temp = True

        if temp == False:
            pass
        elif vac not in ['PFIZER', 'SINOPHARM', 'ASTRAZENICA', 'JOHNSON & JOHNSON']:
            toast("Invalid Vaccination")
            self.ids.type.text = ""
            temp = False
        else:
            temp = True

        dbcursor.execute("SELECT First_Name, Middle_Initial, Surname, Date_Of_Birth FROM Persons WHERE "
                         "First_Name=? AND Middle_Initial=? AND Surname=? AND Date_Of_Birth=?", (f_name, m_name, s_name, dob))
        result = dbcursor.fetchone()


        if temp == True:
            if not result:
                try:
                    dbcursor.execute(sqliteform, test_k)
                    conn.commit()
                except sqlite3.IntegrityError:
                    toast("Too many characters for Initial")
                    self.ids.m_name.text = ""
            else:
                toast("Entry Already Exists")
        else:
            pass

    def back_button(self, screen):
        self.current = screen

class SqlApp(MDApp):

    def build(self):
        return MyLayout()

SqlApp().run()