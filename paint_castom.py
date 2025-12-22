import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("Hello CustomTkinter")
app.geometry("400x200")

# Add a label
label = ctk.CTkLabel(app, text="Hello, CustomTkinter!", font=("Helvetica", 20))
label.pack(pady=20)

# Add a button
button = ctk.CTkButton(app, text="Click Me", command=lambda: print("Button clicked!"))
button.pack(pady=10)

# Run the application
app.mainloop()