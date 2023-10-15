from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
import pyrebase
from mail import *
from mail import otpnum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import keyboard
import time
import requests

Window.size = {320,600}

firebaseConfig = {
    'apiKey': "AIzaSyCn08y_A9zVGHXmZ5BjYCH6Yzxtaln_w0w",
    'authDomain': "auth-b1cff.firebaseapp.com",
    'databaseURL': "https://auth-b1cff-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "auth-b1cff",
    'storageBucket': "auth-b1cff.appspot.com",
    'messagingSenderId': "437794596428",
    'appId': "1:437794596428:web:cf948e7fa21d030126b6e9"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
address = ""
class MainScreen(Screen):
    pass

class AmbulanceScreen(Screen):
    def conditions_select(self):
        conditions = [
            {
                "viewclass": "OneLineListItem",
                "text": "More severe",
                "on_release": lambda x = "More severe": self.change_condition(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Severe",
                "on_release": lambda x = "Severe": self.change_condition(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Moderate",
                "on_release": lambda x = "Moderate": self.change_condition(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Light",
                "on_release": lambda x = "Light": self.change_condition(x)
            }
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.condition,
            items = conditions,
            width_mult = 4
        )
        self.menu.open()

    def change_condition(self,x):
        self.ids.condition.text = x
        self.menu.dismiss()

    def select_hospital(self):
        hospitals = [
            {
                "viewclass": "TwoLineListItem",
                "text": "Swathi Clinic",
                "secondary_text": "38, 13th Cross Road, Veerabhadra Nagar, Banashankari 1st Stage, Banashankari, Bengaluru",
                "on_release": lambda x = "Swathi Clinic": self.change_hospital(x)
            },
            {
                "viewclass": "TwoLineListItem",
                "text": "ESIC Corporation",
                "secondary_text": "WGRQ+6HW, Hosakerehalli Main Road, 1st phase Girinagar, Phase 2, Banashankari, Bengaluru",
                "on_release": lambda x = " ESIC Corporation": self.change_hospital(x)
            },
            {
                "viewclass": "TwoLineListItem",
                "text": "Tirumala Healthcare",
                "secondary_text": "809, 2nd Phase, Kalidasa Nagar, Dattatreya Nagar, Hosakerehalli, Bengaluru",
                "on_release": lambda x = "Tirumala Healthcare": self.change_hospital(x)
            },
            {
                "viewclass": "TwoLineListItem",
                "text": "Vittala International Institute of Ophthalmology",
                "secondary_text": "2nd Cross, 1, 2nd Main Road, 7th Block, Banashankari 3rd Stage, Hosakerehalli, Bengaluru",
                "on_release": lambda x = "Vittala International Institute of Ophthalmology": self.change_hospital(x)
            }
        ]
        self.menu = MDDropdownMenu(
            caller = self.ids.hospital,
            items = hospitals,
            width_mult = 4
        )
        self.menu.open()

    def change_hospital(self,x):
        self.ids.hospital.text = x
        self.menu.dismiss()

    def open_map(self):
        def get_curr_loclick():
            global latitude
            global longitude 
            chrome_options = Options()   # Initialize the web driver with the headless options
            chrome_options.add_argument('--window-size=2x2')  # Set window size

            # Initialize the web driver with the headless options
            driver = webdriver.Chrome(options=chrome_options)
            url = 'https://www.gps-coordinates.net/my-location'
            driver.get(url)
            driver.implicitly_wait(5)
            try:
                accept_cookies = driver.find_element(By.ID, 'accept-cookies')
                accept_cookies.click()
            except Exception as e:
                pass

            # If the page has a search form, fill it and simulate a user interaction
            try:
                search_input = driver.find_element(By.ID, 'search-input')
                search_input.send_keys('Your Location')
                search_input.send_keys(Keys.RETURN)
            except Exception as e:
                pass

            # Wait for the page to stabilize after interactions
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.visibility_of_element_located((By.ID, 'lat')))

            # Get the page source
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            element_lat = soup.find(id='lat')
            if element_lat:
                latitude=element_lat.text
                print("Latitude:",latitude )
            else:
                print("Element with id 'lat' not found")
            element_lon = soup.find(id='lng')
            if element_lon:
                longitude= element_lon.text
                print("Longitude:",longitude)
            else:
                print("Element with id 'lon' not found")
            latitude=latitude[0:9]
            longitude=longitude[0:10]
            driver.quit()
            base_url = "https://www.google.com/maps/search/?api=1&query="
            query = f"{latitude},{longitude}"
            gmaps_url = base_url + query

            return gmaps_url
        global url
        url = get_curr_loclick()

        def get_curr_address():
            get_curr_loclick()
            geolocator = Nominatim(user_agent="reverse_geocoder")
            location = f"{latitude}, {longitude}"
            address = geolocator.reverse(location, exactly_one=True)
            if address:
                return(address.address)
            else:
                print("not found")

        address = get_curr_address()
        self.ids.textfield.text = address

        '''def availabe_display():
            api_key = 'AIzaSyAMfpWeT_ak2ffFWqlLbe9eFYRoVzlX2hU'
            get_curr_loclick()
            radius_km = 5  # Change this value to your desired radius in kilometers
            radius_meters = radius_km * 1000
            place_type = 'hospital'
            url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius_meters}&type={place_type}&key={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                if results:
                    print("Nearby Hospitals:")
                    d=dict()
                    for place in results:
                        name = place.get('name', 'N/A')
                        address = place.get('vicinity', 'N/A')
                        d[name]=[address]
                        print(f"Name: {name}, Address: {address}")
                else:
                    print("No hospitals found nearby.")
            else:
                print(f"Error: {response.status_code}")
            return d
        hospital_list = availabe_display()'''
    
    def book(self):
        self.dialog = MDDialog(
            title="Ambulance has been booked",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                )
            ]
        )
        self.dialog.open()
        if username is not None:
            send_mail_booked(username,"7483611935",url)
        send_mail_driver("rktb2872@gmail.com")
        self.open_map()
        
    def close(self):
        self.dialog.dismiss()

class PoliceScreen(Screen):
    pass

class FirstAidScreen(Screen):
    pass

class LoginPage(Screen):
    def login(self):
        # Accessing credentials and validating
        global username
        username = self.ids.username.text
        self.login_password = self.ids.password.text
        try:
            global user
            user = auth.sign_in_with_email_and_password(username, self.login_password)
            self.manager.transition = SlideTransition(direction = 'left')
            self.manager.current = "main"
        except:
            self.dialog = MDDialog(text = "Invalid credentials")
            self.dialog.open()

class SignUpPage(Screen):
    def signup(self):
        global username
        username = self.ids.username.text
        self.sign_password = self.ids.password.text
        confirm_pass = self.ids.confirm_password.text
        if self.sign_password == confirm_pass:
            send_mail_otp(username)
            self.manager.transition = SlideTransition(direction = 'left')
            self.manager.current = "otpscreen"
        else:
            self.ids.password.error = "Password is not matching"

class OTPScreen(Screen):
    def goback(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'signup'

    def verify_otp(self):
        otp = self.ids.otp_input.text
        username = self.manager.get_screen('signup').ids.username.text
        password = self.manager.get_screen('signup').ids.password.text
        if(int(otpnum) == int(otp)):
            try:
                global user
                user = auth.create_user_with_email_and_password(username, password)
                self.manager.transition.direction = 'left'
                self.manager.current = "main"
            except:
                self.dialog = MDDialog(text = "Invalid credentials")
                self.dialog.open()
        else:
            self.dialog = MDDialog(text = "Invalid otp")
            self.dialog.open()

class ProfileScreen(Screen):
    def dropdown_gender(self):
        self.genders = [
            {
                "viewclass": "OneLineListItem",
                "text": "Male",
                "on_release": lambda x = "Male": self.change_gender(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Female",
                "on_release": lambda x = "Female": self.change_gender(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Other",
                "on_release": lambda x = "Other": self.change_gender(x)
            }
        ]
        self.menu1 = MDDropdownMenu(
            caller = self.ids.gender,
            items = self.genders,
            width_mult = 4
        )
        self.menu1.open()
    
    def change_gender(self,x):
        self.ids.gender.text = x
        self.menu1.dismiss()

    def dropdown_blood(self):
        self.groups = [
            {
                "viewclass": "OneLineListItem",
                "text": "A+",
                "on_release": lambda x = "A+": self.change_blood(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "A-",
                "on_release": lambda x = "A-": self.change_blood(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "B+",
                "on_release": lambda x = "B+": self.change_blood(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "B-",
                "on_release": lambda x = "B-": self.change_blood(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "AB+",
                "on_release": lambda x = "AB+": self.change_blood(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "AB-",
                "on_release": lambda x = "AB-": self.change_blood(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "O+",
                "on_release": lambda x = "O+": self.change_blood(x)
            },
            {
                "viewclass": "OneLineListItem",
                "text": "O-",
                "on_release": lambda x = "O-": self.change_blood(x)
            }
        ]
        self.menu2 = MDDropdownMenu(
            caller = self.ids.blood,
            items = self.groups,
            width_mult = 4
        )
        self.menu2.open()
    
    def change_blood(self,x):
        self.ids.blood.text = x
        self.menu2.dismiss()

    def saveprofile(self):
        data = {"name": self.ids.name.text,
            "age": self.ids.age.text,
            "gender": self.ids.gender.text,
            "blood group": self.ids.blood.text,
            "Phone number": self.ids.phno.text,
            "emergency contact number": self.ids.ephno.text
            }
        if user is not None:
            db.child("users").child(user['localId']).set(data)
        
        self.manager.transition = SlideTransition(direction = 'right')
        self.manager.current = "main"

class EmergencyApp(MDApp):
    def profile(self):
        self.root.transition = SlideTransition(direction = 'left')
        self.root.current = "profile"

    def go_back(self):
        self.root.transition = SlideTransition(direction = 'right')
        self.root.current = "main"

    def emergency(self):
        self.dialog = MDDialog(
            text = "Do you really want to send emergency alert?",
            buttons = [
                MDFlatButton(
                    text = "CANCEL",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_release = self.close_emergency,
                ),
                MDFlatButton(
                    text = "SEND",
                    theme_text_color = "Custom",
                    text_color = self.theme_cls.primary_color,
                    on_press=self.send_alert()
                ),
            ]
        )
        self.dialog.open()

    def close_emergency(self,instance):
        self.dialog.dismiss()

    def send_alert(self):
        send_mail_alert("asleshat5@gmail.com","Ashlesha",address)

EmergencyApp().run()