from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '304')
Config.set('graphics', 'height', '612')


class CreateAccount(Screen):
	name = ObjectProperty(None)
	email = ObjectProperty(None)
	password = ObjectProperty(None)
	password_again = ObjectProperty(None)

	def some(self):
		pass

	def reset(self):
		self.namee.text = ""
		self.email.text = ""
		self.password.text = ""
		self.password_again.text = ""

	def save(self):
		null_check = bool(self.namee.text and self.email.text)
		validity_check = bool(self.email.text.count("@")==1 and self.email.text.count(".")>0)
		password_check = bool(self.password.text == self.password_again.text)
		if (null_check and validity_check):
			if (password_check):
				create_account = sqlite3.connect('src/profile_info.db')
				cur = create_account.cursor()
				cur.execute('''CREATE TABLE IF NOT EXISTS Account(ID INTEGER PRIMARY KEY AUTOINCREMENT, 
					Name TEXT NOT NULL, Password TEXT NOT NULL, Email Text NOT NULL)''')
				cur.execute('''INSERT INTO Account(Name, Password, Email) VALUES(?, ?, ?)''',
					(str(self.namee.text), str(self.password.text), str(self.email.text)))
				create_account.commit()
				create_account.close()
				window.current = "login"
			else:
				passwordMismatch()
		else:
			invalidForm()

	def cancel(self):
		window.current = "login"


class Login(Screen):
	def create(self):
		window.current = "create"
		#self.reset()
	
class DashBoard(Screen):
    pass
class OpenIssue(Screen):
    pass
class IssueDetail(Screen):
    pass
class WindowManager(ScreenManager):
    pass
    
def invalidForm():
	invalid_pop = Popup(title="Invalid Form",
		content = Label(text="Please enter the valid credentials."),
		size_hint = (None, None),size=(700, 700))
	invalid_pop.open()

def invalidLogin():
	pass

def passwordMismatch():
	mismatch_pop = Popup(title="Password Mismatch",
		content = Label(text="Please use the same password."),
		size_hint = (None, None), size=(700, 700))
	mismatch_pop.open()

kv = Builder.load_file("SmartPole.kv")

window = WindowManager()


screens = [Login(name="login"), CreateAccount(name="create"), DashBoard(name="dash"),
OpenIssue(name="open_issue"), IssueDetail(name="detail")]

for screen in screens:
	window.add_widget(screen)

window.current = "login"

class MainScreenApp(App):
    def build(self):
        return window

if __name__=="__main__":
    MainScreenApp().run()