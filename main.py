import tkinter as tk
from tkinter import messagebox


def calculate_height():
    try:
        hanger_distance = int(hanger_entry.get())
        art_height = int(art_entry.get())
        art_width = int(art_width_entry.get())
        avg_adult_height = avg_height_entry.get()
        wall_height = wall_var.get()
        wall_length = wall_length_entry.get()
        num_pieces = num_pieces_entry.get()

        if avg_adult_height:
            avg_adult_height = int(avg_adult_height)
        else:
            avg_adult_height = 58  # Default average eye level

        # Determine wall height based on selection
        if wall_height == "Average (7-8 feet)":
            wall_height_value = 96  # Assuming 8 feet as standard
        elif wall_height == "Tall (9 feet)":
            wall_height_value = 108
        else:
            wall_height_value = 120

        center_height = avg_adult_height  # Eye-level recommendation
        picture_center = art_height / 2
        recommended_hanger_height = center_height - picture_center + hanger_distance

        result_text = f"Recommended picture hanging height: {round(recommended_hanger_height)} inches"

        # Calculate centering if wall length is provided
        if wall_length:
            wall_length = int(wall_length)
            if num_pieces:
                num_pieces = int(num_pieces)
                spacing = (wall_length - (num_pieces * art_width)) / (num_pieces + 1)
                positions = [round(spacing * (i + 1) + (i * art_width)) for i in range(num_pieces)]
                result_text += f"\nSuggested horizontal positions: {positions} inches from the edge."
            else:
                center_position = round((wall_length - art_width) / 2)
                result_text += f"\nSuggested horizontal position: {center_position} inches from the edge."

        messagebox.showinfo("Result", result_text)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create main window
root = tk.Tk()
root.title("Franklin Arts Calculator")
root.geometry("450x650")

# Load images (ensure they are .png format)
hanger_img = tk.PhotoImage(file="hanger-distance.png")
art_img = tk.PhotoImage(file="picture-height.png")
avg_height_img = tk.PhotoImage(file="average-height.png")

# Labels and Entries
tk.Label(root, text="Hanger Distance (inches)").pack()
tk.Label(root, image=hanger_img).pack()
hanger_entry = tk.Entry(root)
hanger_entry.pack()

tk.Label(root, text="Art Height (inches)").pack()
tk.Label(root, image=art_img).pack()
art_entry = tk.Entry(root)
art_entry.pack()

tk.Label(root, text="Art Width (inches)").pack()
art_width_entry = tk.Entry(root)
art_width_entry.pack()

tk.Label(root, text="Average Adult Height (inches, optional)").pack()
tk.Label(root, image=avg_height_img).pack()
avg_height_entry = tk.Entry(root)
avg_height_entry.pack()

tk.Label(root, text="Wall Height").pack()
wall_var = tk.StringVar(value="Average (7-8 feet)")
tk.OptionMenu(root, wall_var, "Average (7-8 feet)", "Tall (9 feet)", "Taller (9+ feet)").pack()

tk.Label(root, text="Wall Length (inches, optional for centering)").pack()
wall_length_entry = tk.Entry(root)
wall_length_entry.pack()

tk.Label(root, text="Number of Pieces (optional for multiple pieces)").pack()
num_pieces_entry = tk.Entry(root)
num_pieces_entry.pack()

# Calculate Button
tk.Button(root, text="Calculate", command=calculate_height).pack()

# Run the application
root.mainloop()
