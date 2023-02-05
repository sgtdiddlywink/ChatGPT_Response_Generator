import openai
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont

"""Simple script for a gui that utilizes openai's API to create responses to comments from a post on your choice of forum."""

# CONSTANTS
KEY = "YOUR API KEY HERE"

# Create key object from your API Key
openai.api_key = KEY


# Create function to generate a response using ChatGPT
def generate_response():
	input_comment = input_target_entry.get().strip()  # Grab the text from the input box
	response = response_var.get()
	# Check to see if anything was provided in the input box
	if input_comment == "":
		output_text.delete("1.0", tk.END)  # Delete anything in the output box
		output_text.insert(tk.END, "No comment provided. Try again.")  # Insert output in box
	forum = forum_var.get()  # Grabs the forum selection
	chat_engine = "text-davinci-002"  # Specify the OpenAI engine to utilize
	# Initial prompt fed to the OpenAI engine
	input_prompt = (f"Generate a {response} response to the following comment on the this {forum}:\n"
					f"{input_comment}\n"
					f"Context: I am responding to a stranger on the internet to a comment they made.")
	try:
		# Response from OpenAI and form a object from it
		comp = openai.Completion.create(
			engine=chat_engine,
			prompt=input_prompt,
			max_tokens=1024,
			n=1,
			stop=None,
			temperature=.5,
		)
		response = comp.choices[0].text
		output_text.delete("1.0", tk.END)
		output_text.insert(tk.END, response)
	# Error Handling
	except openai.error.RateLimitError:
		output_text.delete("1.0", tk.END)
		output_text.insert(tk.END, "You exceed your current quota with OpenAI, check your plan and billing details.")
	except openai.error.AuthenticationError:
		output_text.delete("1.0", tk.END)
		output_text.insert(tk.END, "Incorrect API Key provided. Check python script Constants and try again.")


# Create a Custom Tkinter gui
window = tk.Tk()
window.title("Response Generator")
window.geometry("700x350")

# Create container for tk gui
container = ttk.Frame(window, padding=10)
container.grid(column=0, row=0)

# Create row for different selections of forums. Add more in forum options list below
forum_label = ttk.Label(container,text="Specify Forum: ", font=("Helvetica", 16))
forum_label.grid(column=0, row=0, sticky="W")
forum_var = tk.StringVar()  # Utilize to dynamically update the forum type
forum_var.set("Forum")  # This will initially set the dropdown menu to "Reddit"
forum_options = ["Reddit", "Twitter", "Facebook", "Instagram", "Forum"]
forum_dropdown = ttk.Combobox(container, values=forum_options, font=("Helvetica", 16))
forum_dropdown.grid(column=1, row=0, sticky="E")  # Specify location of dropdown menu

# Create row for dropdown menu for the different types of responses
response_type_label = ttk.Label(container, text="Response Type: ", font=("Helvetica", 16))
response_type_label.grid(column=0, row=1, sticky="W", pady=5, padx=5)
response_var = tk.StringVar()
response_var.set("Normal")
response_options = ["Normal", "Witty", "Mean", "Encouraging", "Nice", "Teen Angst", "Brutally Honest", "Eye Opening", "Apologetic", "Super Mean", "Super Nice"]
response_dropdown = ttk.Combobox(container, values=response_options, font=("Helvetica", 16))
response_dropdown.grid(column=1, row=1, sticky="E", pady=5, padx=5)  # Specify location of dropdown menu

# Create row for specifying initial target comment
input_label = ttk.Label(container, text="Comment: ", font=("Helvetica", 16))  # Create label
input_label.grid(column=0, row=2, sticky="W")  # Specify location of input label
input_target = tk.StringVar()  # Utilize to dynamically update input string variable
input_target_entry = ttk.Entry(container, textvariable=input_target, width=21, font=("Helvetica", 16))
input_target_entry.grid(column=1, row=2, columnspan=2, sticky="E")

# Generate button for response & customize size and location
generate_button = tk.Button(container, text="Generate a Response", command=generate_response)
helv16 = tkFont.Font(family="Helvetica", size=16, weight="bold")
generate_button['font'] = helv16
generate_button.grid(column=0, row=4, sticky="W", pady=10)

# Create area for the generated response to appear
output_text = tk.Text(container, height=5, width=50, font=("Helvetica", 16))
output_text.grid(column=0, row=5, columnspan=2)

# Loop the window to keep it open and functioning
window.mainloop()
