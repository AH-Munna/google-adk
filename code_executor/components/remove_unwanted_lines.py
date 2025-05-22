import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from pyperclip import copy

def show_filter_gui(keyword:str):
    """Creates and runs the Tkinter GUI for filtering lines."""

    def process_filter():
        """Gets input from GUI, filters, and displays results."""
        keyword = keyword_entry.get()
        input_text = input_text_area.get("1.0", tk.END).strip() # Get all text

        if not keyword:
            messagebox.showerror("Error", "Keyword cannot be empty!")
            return

        if not input_text:
            lines = []
        else:
            # splitlines() handles different line endings gracefully
            lines = input_text.splitlines()

        # --- Filtering Logic (Keep lines containing the keyword) ---
        filtered_lines = [line for line in lines if keyword in line]
        # --- End Filtering Logic ---

        output_text = '\n'.join(filtered_lines)
        copy(output_text)

        # Update output area
        output_text_area.config(state=tk.NORMAL) # Enable writing
        output_text_area.delete("1.0", tk.END)    # Clear previous output
        output_text_area.insert(tk.END, output_text) # Insert new output
        output_text_area.config(state=tk.DISABLED) # Disable writing again

    # --- Setup the main window ---
    root = tk.Tk()
    root.title("Line Filter Tool")
    # Basic attempt at "beautiful" - using themed widgets and padding
    style = ttk.Style(root)
    style.theme_use('clam') # 'clam', 'alt', 'default', 'classic' are common options

    # Make window resizable
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1) # Input area row
    root.rowconfigure(3, weight=1) # Output area row
    root.geometry("1366x768")


    # --- Input Frame ---
    input_frame = ttk.Frame(root, padding="10 10 10 10")
    input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    input_frame.columnconfigure(1, weight=1) # Allow entry/text area to expand

    # Keyword input
    ttk.Label(input_frame, text="Keyword:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    keyword_entry = ttk.Entry(input_frame, width=40)
    keyword_entry.insert(0, keyword)
    keyword_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

    # --- Input Text Area ---
    ttk.Label(root, text="Enter Lines:").grid(row=1, column=0, padx=10, pady=(5,0), sticky=tk.W)
    input_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=60)
    input_text_area.grid(row=2, column=0, padx=10, pady=(0,10), sticky=(tk.W, tk.E, tk.N, tk.S))

    # --- Filter Button ---
    filter_button = ttk.Button(root, text="Filter Lines", command=process_filter)
    filter_button.grid(row=3, column=0, padx=10, pady=5)

    # --- Output Text Area ---
    ttk.Label(root, text="Filtered Lines:").grid(row=4, column=0, padx=10, pady=(5,0), sticky=tk.W)
    output_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=60, state=tk.DISABLED) # Start disabled
    output_text_area.grid(row=5, column=0, padx=10, pady=(0,10), sticky=(tk.W, tk.E, tk.N, tk.S))


    # Focus on the keyword entry initially
    keyword_entry.focus()

    # Start the GUI event loop
    root.mainloop()


def filter_lines_with_keyword(keyword: str = "", lines: list[str] = []):
    """
    Keeps only lines that contain the specified keyword.
    If 'lines' is None or empty, the script opens a Tkinter GUI to take input from user and also handles output (no additional action is required).

    Args:
        keyword (str): The keyword to search for. Lines without this keyword will be removed.
        lines (list[str], optional): The list of lines to filter.
                                     If None or empty, a GUI will be launched. Defaults to None.

    Returns:
        str: A single string containing the filtered lines, joined by newlines.
             Returns only status message if the GUI is launched (as the GUI handles the output).
    Raises:
        ValueError: If 'keyword' is empty and lines are provided.
    """
    if not keyword:
         if  not lines or len(lines) == 0:
             return {
                 "status": "error",
                 "message": "Keyword cannot be empty!",
             }

    if  not lines or len(lines) == 0:
        print("Input lines not provided, launching GUI...")
        show_filter_gui(keyword)
        return {"status": "success", "message": None}
    else:
        filtered_lines = [line for line in lines if keyword in line]
        filtered_lines = '\n'.join(filtered_lines)
        return {"status": "success", "message": filtered_lines}