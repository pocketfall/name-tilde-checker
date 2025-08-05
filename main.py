import customtkinter as ctk
from requests import get
from bs4 import BeautifulSoup
from config import *

class NameSearcher(ctk.CTk):
	def __init__(self):
		super().__init__() # initialize customtkinter window

		# window customization
		self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
		self.resizable(False, False)
		self.title("¿ LLeva tilde ?")
		ctk.set_appearance_mode("dark")

		# variables and data
		self.tilde_url = "https://www.llevatilde.es/palabra/REPLACEME"
		self.tilde_url_wrong = "https://www.llevatilde.es"
		self.font = FONT 
		self.name_to_search = ctk.StringVar()
		self.output_label_text = ctk.StringVar()

		# create widgets
		self.create_widgets()

		# run app loop
		self.mainloop()
	
	def create_widgets(self):
		# base frame
		frame = ctk.CTkFrame(self, fg_color= GREY)
		frame.pack(fill= "both", expand= True)

		# output frame and label
		self.make_output(parent= frame)
		# output_frame = ctk.CTkFrame(self, fg_color= "blue")
		# output_label = ctk.CTkLabel(output_frame, font= (self.font[0], 32), textvariable= self.output_label_text)

		# entry
		entry_frame = ctk.CTkFrame(frame, fg_color= GREY)
		entry_field = ctk.CTkEntry(entry_frame, placeholder_text= "Salinas", textvariable= self.name_to_search, font= self.font)
		entry_field.pack(expand= True, fill= "x", padx= 10)
		entry_frame.pack(expand= True, fill= "both", pady= 5, padx= 5)
		### EntryWithTwoButtons(parent= self, text_variable= self.name_to_search, search_command= None, destroy_command= None, font= self.font)

		# search button
		buttons_frame = ctk.CTkFrame(frame, fg_color= GREY)
		search_button = ctk.CTkButton(buttons_frame, text= "Buscar", font= self.font, command= self.search_word,
								fg_color= BUTTON_DEFAULT, hover_color= BUTTON_HOVER, text_color= BLACK)
		search_button.pack(expand= True, fill= "both", side= "left")
		buttons_frame.pack(expand= True, fill= "both", padx= 5, pady= 5)
	
	def search_word(self):
		# search for the word that was input into the Entry
		word_to_search = self.name_to_search.get().lower() # make it lower case for safety
		search_url = self.tilde_url.replace("REPLACEME", word_to_search)
		
		# request answer from llevatilde.es
		try:
			request_response = get(search_url).content # get content to pass it into beautifulsoup
			soup = BeautifulSoup(request_response, "html.parser") # use the html parser

			# search for links in the html and get the one we want (one word following /palabra/ that is not separated by -)
			for link in soup.find_all("a"):
				link_string = link.get("href")
				if link_string.split("/")[-2] == "palabra" and "-" not in link_string.split("/")[-1]:
					print(link_string)
					true_response = BeautifulSoup(get(f"{str(self.tilde_url_wrong)}{str(link_string)}").content, "html.parser")
					output_label_text = true_response.title
					# <title>¿Lleva tilde ventura? | LlevaTilde.es</title>
					output_label_text_formatted = self.format_output_text(output_label_text)
					print(output_label_text_formatted)
					self.output_label.configure(text_color= WHITE)
					self.output_label_text.set(output_label_text_formatted)
		except:
			error_message = "La palabra introducida no fué encontrada en llevatilde.es"
			self.output_label.configure(text_color= RED)
			self.output_label_text.set(error_message)
	
	def format_output_text(self, text_to_edit):
		# formats text so it can fit better into the output label and frame
		# input:
		#	<title>¿Lleva tilde ventura? | LlevaTilde.es</title>
		
		edited_text = str(text_to_edit) # type is NOT string, instead is bs4 type
		edited_text = edited_text.replace("<title>", "").replace("</title>", "")	
		return edited_text

	def make_output(self, parent):
		# create output frame and label
		output_frame = ctk.CTkFrame(parent, fg_color= GREY)
		self.output_label = ctk.CTkLabel(output_frame, font= (self.font[0], OUTPUT_FONT_SIZE), textvariable= self.output_label_text)
		self.output_label.pack(expand= True, fill= "both")
		output_frame.pack(expand= True, fill= "both", side= "bottom", padx= 5, pady= 5)

if __name__ == "__main__":
	NameSearcher()
