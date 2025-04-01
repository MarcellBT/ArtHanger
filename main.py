import tkinter as tk
from tkinter import messagebox, ttk


def update_art_entries():
    # Clear existing entries in art_entries_frame
    for widget in art_entries_frame.winfo_children():
        widget.destroy()
    
    try:
        num_pieces = int(num_pieces_entry.get()) if num_pieces_entry.get() else 1
    except ValueError:
        num_pieces = 1
        num_pieces_entry.delete(0, tk.END)
        num_pieces_entry.insert(0, "1")
    
    # If "Same Size" is checked, show only one set of entries
    if same_size_var.get():
        tk.Label(art_entries_frame, text="Art Height (inches)").pack()
        tk.Label(art_entries_frame, image=art_img).pack()
        global art_entry
        art_entry = tk.Entry(art_entries_frame)
        art_entry.pack()

        tk.Label(art_entries_frame, text="Art Width (inches)").pack()
        global art_width_entry
        art_width_entry = tk.Entry(art_entries_frame)
        art_width_entry.pack()
    else:
        # Show entries for each piece
        global art_entries
        art_entries = []
        
        for i in range(num_pieces):
            piece_frame = tk.Frame(art_entries_frame)
            piece_frame.pack(pady=5)
            
            tk.Label(piece_frame, text=f"Piece {i+1}").grid(row=0, column=0, columnspan=2)
            
            tk.Label(piece_frame, text="Height (inches):").grid(row=1, column=0, sticky="w")
            height_entry = tk.Entry(piece_frame, width=10)
            height_entry.grid(row=1, column=1, padx=5)
            
            tk.Label(piece_frame, text="Width (inches):").grid(row=2, column=0, sticky="w")
            width_entry = tk.Entry(piece_frame, width=10)
            width_entry.grid(row=2, column=1, padx=5)
            
            art_entries.append((height_entry, width_entry))


def on_num_pieces_change(*args):
    update_art_entries()


def calculate_height():
    try:
        hanger_distance = float(hanger_entry.get())
        avg_adult_height = float(avg_height_entry.get()) if avg_height_entry.get() else 58.0
        wall_length = float(wall_length_entry.get()) if wall_length_entry.get() else 0.0
        num_pieces = int(num_pieces_entry.get()) if num_pieces_entry.get() else 1
        
        # Get art dimensions based on Same Size checkbox
        if same_size_var.get():
            # All pieces have the same dimensions
            art_height = float(art_entry.get())
            art_width = float(art_width_entry.get())
            
            # All pieces have the same dimensions
            art_heights = [art_height] * num_pieces
            art_widths = [art_width] * num_pieces
        else:
            # Each piece has its own dimensions
            art_heights = []
            art_widths = []
            
            for height_entry, width_entry in art_entries:
                art_heights.append(float(height_entry.get()))
                art_widths.append(float(width_entry.get()))

        # Calculate nail positions for each piece
        nail_positions = []
        for height in art_heights:
            # Calculate nail height to place center of art at the specified height
            nail_position = avg_adult_height + (height/2 - hanger_distance)
            nail_positions.append(round(nail_position, 2))
        
        result_text = "Nail positions relative to the floor:\n"
        for i, pos in enumerate(nail_positions):
            result_text += f"Piece {i+1}: {pos} inches\n"
        
        # Calculate horizontal positions to evenly space the pieces on the wall
        if wall_length and num_pieces > 0:
            total_art_width = sum(art_widths)
            
            if total_art_width > wall_length:
                result_text += f"\nWarning: Total width of art pieces ({round(total_art_width, 2)} inches) exceeds wall length ({round(wall_length, 2)} inches)."
            else:
                # Calculate remaining space after accounting for art pieces
                remaining_space = wall_length - total_art_width
                
                # Calculate even spacing between pieces and edges
                spacing = remaining_space / (num_pieces + 1)
                
                # Calculate horizontal positions for each nail
                horizontal_positions = []
                current_position = spacing
                
                for i, width in enumerate(art_widths):
                    position = current_position + width/2
                    horizontal_positions.append(round(position, 2))
                    current_position += width + spacing
                
                result_text += "\nHorizontal nail positions (inches from the edge of the wall):\n"
                for i, pos in enumerate(horizontal_positions):
                    result_text += f"Piece {i+1}: {pos} inches\n"

        messagebox.showinfo("Result", result_text)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")


# Create main window
root = tk.Tk()
root.title("Franklin Arts Calculator")
root.geometry("500x700")

# Load images (ensure they are .png format)
hanger_img = tk.PhotoImage(file="hanger-distance.png")
art_img = tk.PhotoImage(file="picture-height.png")
avg_height_img = tk.PhotoImage(file="average-height.png")

# Main frame to organize the UI
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Labels and Entries for common inputs
ttk.Label(main_frame, text="Hanger Distance (inches)").pack(anchor="w")
ttk.Label(main_frame, image=hanger_img).pack()
hanger_entry = ttk.Entry(main_frame)
hanger_entry.pack(fill="x", pady=5)

ttk.Label(main_frame, text="Average Adult Height (inches)").pack(anchor="w")
ttk.Label(main_frame, image=avg_height_img).pack()
avg_height_entry = ttk.Entry(main_frame)
avg_height_entry.insert(0, "58")  # Display default mid-center height
avg_height_entry.pack(fill="x", pady=5)

ttk.Label(main_frame, text="Wall Length (inches)").pack(anchor="w")
wall_length_entry = ttk.Entry(main_frame)
wall_length_entry.pack(fill="x", pady=5)

# Number of pieces with trace for dynamic UI updates
ttk.Label(main_frame, text="Number of Pieces").pack(anchor="w")
num_pieces_var = tk.StringVar(value="1")
num_pieces_entry = ttk.Entry(main_frame, textvariable=num_pieces_var)
num_pieces_entry.pack(fill="x", pady=5)
num_pieces_var.trace_add("write", on_num_pieces_change)

# Same Size checkbox
same_size_var = tk.BooleanVar(value=True)
same_size_check = ttk.Checkbutton(
    main_frame, 
    text="Same Size for All Pieces", 
    variable=same_size_var,
    command=update_art_entries
)
same_size_check.pack(anchor="w", pady=5)

# Frame for art dimension entries
art_entries_frame = ttk.Frame(main_frame)
art_entries_frame.pack(fill="both", expand=True, pady=10)

# Initialize art entries
update_art_entries()

# Calculate Button
ttk.Button(main_frame, text="Calculate", command=calculate_height).pack(pady=10)

# Run the application
root.mainloop()
