import tkinter as tk
import math

# Function to handle button clicks
def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + value)

# Function to clear the entry field
def clear():
    entry.delete(0, tk.END)

# Function to calculate the result
def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Function for square root calculation
def sqrt():
    try:
        value = float(entry.get())
        result = math.sqrt(value)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Function for exponentiation
def exponent():
    try:
        value = float(entry.get())
        result = math.pow(value, 2)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

# Main window setup
root = tk.Tk()
root.title("Advanced Calculator")

# Entry widget for displaying calculations
entry = tk.Entry(root, width=30, borderwidth=5, font=('Arial', 14), relief=tk.RAISED, justify='right')
entry.grid(row=0, column=0, columnspan=4)

# Define the button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ('C', 5, 0), ('sqrt', 5, 1), ('^2', 5, 2), ('exit', 5, 3)
]

# Add buttons to the window
for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(root, text=text, width=10, height=2, font=('Arial', 14), command=calculate)
    elif text == "C":
        button = tk.Button(root, text=text, width=10, height=2, font=('Arial', 14), command=clear)
    elif text == "exit":
        button = tk.Button(root, text=text, width=10, height=2, font=('Arial', 14), command=root.quit)
    elif text == "sqrt":
        button = tk.Button(root, text=text, width=10, height=2, font=('Arial', 14), command=sqrt)
    elif text == "^2":
        button = tk.Button(root, text=text, width=10, height=2, font=('Arial', 14), command=exponent)
    else:
        button = tk.Button(root, text=text, width=10, height=2, font=('Arial', 14), command=lambda t=text: button_click(t))
    button.grid(row=row, column=col)

# Start the application
root.mainloop()
