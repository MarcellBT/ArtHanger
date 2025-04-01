import tkinter as tk
from tkinter import messagebox


def calculate_height():
    try:
        hanger_distance = float(hanger_entry.get())
        art_height = float(art_entry.get())
        art_width = float(art_width_entry.get())
        avg_adult_height = float(avg_height_entry.get()) if avg_height_entry.get() else 58.0
        wall_length = float(wall_length_entry.get()) if wall_length_entry.get() else 0.0
        num_pieces = int(num_pieces_entry.get()) if num_pieces_entry.get() else 1

        # User wants the center of art to be at the specified height (avg_adult_height)
        # The nail needs to be positioned higher to account for the hanging distance
        nail_position = avg_adult_height + (art_height/2 - hanger_distance)
        
        result_text = f"Nail position relative to the floor: {round(nail_position, 2)} inches"
        
        # Calculate horizontal positions to evenly space the pieces on the wall
        if wall_length and num_pieces > 0:
            total_art_width = num_pieces * art_width
            
            if total_art_width > wall_length:
                result_text += f"\nWarning: Total width of art pieces ({round(total_art_width, 2)} inches) exceeds wall length ({round(wall_length, 2)} inches)."
            else:
                # Calculate remaining space after accounting for art pieces
                remaining_space = wall_length - total_art_width
                
                # Calculate even spacing between pieces and edges
                spacing = remaining_space / (num_pieces + 1)
                
                # Calculate horizontal positions for each nail
                horizontal_positions = []
                for i in range(1, num_pieces + 1):
                    position = spacing * i + art_width * (i - 0.5)
                    horizontal_positions.append(round(position, 2))
                
                if num_pieces == 1:
                    result_text += f"\nHorizontal nail position: {horizontal_positions[0]} inches from the edge of the wall."
                else:
                    result_text += f"\nHorizontal nail positions (inches from the edge of the wall):"
                    for i, pos in enumerate(horizontal_positions):
                        result_text += f"\nPiece {i+1}: {pos}"

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

# Labels and Entries for the Art Piece
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
avg_height_entry.insert(0, "58")  # Display default mid-center height
avg_height_entry.pack()

tk.Label(root, text="Wall Length (inches, optional for centering)").pack()
wall_length_entry = tk.Entry(root)
wall_length_entry.pack()

# Add number of pieces entry
tk.Label(root, text="Number of Pieces (optional, for multiple pieces)").pack()
num_pieces_entry = tk.Entry(root)
num_pieces_entry.insert(0, "1")  # Default to 1 piece
num_pieces_entry.pack()

# Calculate Button
tk.Button(root, text="Calculate", command=calculate_height).pack()

# Run the application
root.mainloop()
