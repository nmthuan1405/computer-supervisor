from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.image import Image
from io import BytesIO
import socket
from _thread import start_new_thread
''' 
The HOST name is set to localhost/127.0.0.1 for testing purposes.
I have tested it on my local networks server.
'''
HOST = '127.0.0.1'
PORT = 5455
'''
This is my first app attempt with the kivy module for python.
It is super basic and follows the outline of some web tutorials.

'''

	
class MyCamera(App):
	def build(self):
		layout = BoxLayout(orientation='vertical')

		self.webcam = Camera(play=True)
		self.webcam.resolution = (500,500)

		self.cameraButton = Button(text='Take Photo')
		self.cameraButton.size_hint = (.5,.2)
		self.cameraButton.pos_hint = {'x':.25,'y':.75}
		self.cameraButton.bind(on_press=self.onButton)
		layout.add_widget(self.webcam)
		layout.add_widget(self.cameraButton)
		return layout
	def onButton(self,*args):
		texture = self.webcam.export_as_image()
		b_io = BytesIO()
		texture.save(b_io,fmt='png')
		#im = Image(texture,fmt='png')
		start_new_thread(sendImage,(b_io.getvalue(),))

def sendImage(tmp):
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as soc:
		soc.connect((HOST,PORT))
		soc.send(tmp)

if __name__ == '__main__':
	app = MyCamera()
	app.run()
