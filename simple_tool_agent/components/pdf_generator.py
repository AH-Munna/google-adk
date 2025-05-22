from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import math
import os

def generate_pdf(title, items, output_filename="output.pdf"):
    """
    Generate a PDF with a title and a list of items formatted as a checklist.
    
    Parameters:
    title (str): The title of the document (approximately 60 characters)
    items (list): A list of strings to be displayed as checklist items
    output_filename (str): The name of the PDF file to create
    """
    # Set up the canvas
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    
    # Set up font and sizes
    title_font_size = 20
    default_item_font_size = 12
    min_font_size = 8  # Minimum font size we'll allow
    checkbox_size = 10
    line_height = default_item_font_size * 1.5
    padding = 50
    
    # Calculate title position and draw it
    c.setFont("Helvetica-Bold", title_font_size)
    
    # If title is long, we'll split it into two lines
    # Approximate 60-70 chars per line depending on font
    if len(title) > 40:
        # Find suitable midpoint for splitting
        mid_point = len(title) // 2
        # Look for space near the midpoint
        while mid_point < len(title) and mid_point > 0:
            if title[mid_point] == ' ':
                break
            mid_point += 1
        
        if mid_point == len(title) or mid_point == 0:
            # If no space found, just split at midpoint
            mid_point = len(title) // 2
        
        title_line1 = title[:mid_point]
        title_line2 = title[mid_point:].strip()
        
        # Calculate text width for centering
        title_width1 = c.stringWidth(title_line1, "Helvetica-Bold", title_font_size)
        title_width2 = c.stringWidth(title_line2, "Helvetica-Bold", title_font_size)
        
        # Draw title lines centered
        c.drawString((width - title_width1) / 2, height - 50, title_line1)
        c.drawString((width - title_width2) / 2, height - 50 - title_font_size * 1.2, title_line2)
        
        # Move current position down for the items
        y_position = height - 50 - title_font_size * 2.5
    else:
        # Calculate text width for centering
        title_width = c.stringWidth(title, "Helvetica-Bold", title_font_size)
        
        # Draw title centered
        c.drawString((width - title_width) / 2, height - 50, title)
        
        # Move current position down for the items
        y_position = height - 50 - title_font_size * 1.5
    
    # Function to determine appropriate font size for an item
    def get_font_size_for_item(item_text, max_width, start_size=default_item_font_size):
        """
        Calculate the appropriate font size to ensure text fits in one line.
        
        Args:
            item_text: The text to display
            max_width: Maximum width available
            start_size: Starting font size
            
        Returns:
            Appropriate font size
        """
        font_size = start_size
        # Account for checkbox and padding
        available_width = max_width - checkbox_size - 5
        
        # Check if text fits at current font size
        text_width = c.stringWidth(item_text, "Helvetica", font_size)
        
        # If text is too wide, reduce font size until it fits
        while text_width > available_width and font_size > min_font_size:
            font_size -= 0.5
            text_width = c.stringWidth(item_text, "Helvetica", font_size)
            
        return font_size
    
    # Determine if we need two columns
    if len(items) > 10:
        # Calculate column width
        col_width = (width - 3 * padding) / 2
        
        # Calculate items per column
        items_per_column = math.ceil(len(items) / 2)
        
        # We need to calculate dynamic line heights based on actual font sizes
        # For simplicity, we'll use a consistent line height for layout calculation
        # The actual text rendering will use different font sizes
        total_checklist_height = max(items_per_column, len(items) - items_per_column) * line_height
        
        # Calculate start y position to vertically center the checklist
        # We take into account the title space at the top
        title_space = 100  # Approximate space for title
        available_height = height - title_space
        start_y_position = (available_height / 2) + (total_checklist_height / 2)
        
        # Draw items in two columns
        for i, item in enumerate(items):
            # Determine which column this item belongs to
            if i < items_per_column:
                # First column
                x_position = padding
                # Calculate y position based on position within the column
                y_pos = start_y_position - (i * line_height)
            else:
                # Second column
                x_position = padding + col_width + padding
                # Calculate y position based on position within the column
                y_pos = start_y_position - ((i - items_per_column) * line_height)
            
            # Calculate available width for this column
            available_column_width = col_width - padding
            
            # Get appropriate font size for this item
            item_font_size = get_font_size_for_item(item, available_column_width)
            
            # Set font with calculated size
            c.setFont("Helvetica", item_font_size)
            
            # Draw checkbox
            c.rect(x_position, y_pos, checkbox_size, checkbox_size)
            
            # Draw item text
            c.drawString(x_position + checkbox_size + 5, y_pos + 2, item)
    else:
        # Single column for 10 or fewer items
        
        # Calculate total height of checklist
        total_checklist_height = len(items) * line_height
        
        # Calculate start y position to vertically center the checklist
        # We take into account the title space at the top
        title_space = 100  # Approximate space for title
        available_height = height - title_space
        start_y_position = (available_height / 2) + (total_checklist_height / 2)
        
        for i, item in enumerate(items):
            y_pos = start_y_position - (i * line_height)
            
            # Calculate available width for single column
            available_column_width = width - (2 * padding)
            
            # Get appropriate font size for this item
            item_font_size = get_font_size_for_item(item, available_column_width)
            
            # Set font with calculated size
            c.setFont("Helvetica", item_font_size)
            
            # Draw checkbox
            c.rect(padding, y_pos, checkbox_size, checkbox_size)
            
            # Draw item text
            c.drawString(padding + checkbox_size + 5, y_pos + 2, item)
    
    # Save the PDF
    c.save()
    
    # Get the absolute path to the created file
    abs_path = os.path.abspath(output_filename)
    return abs_path

# Example usage
if __name__ == "__main__":
    title = "Sample Task List for the Project - This is a longer title that should span two lines"
    
    # Sample list of items
    sample_items = [
        "Complete the project requirements document",
        "Set up the development environment",
        "Create the initial database schema",
        "Design the user interface mockups",
        "Implement user authentication system Create documentation for API endpoints",
        "Develop",
        "Write unit tests for all components Create documentation for API endpoints Create documentation for API endpoints Create documentation for API endpoints",
        "Perform initial security review",
        "Create documentation for API endpoints",
        "Schedule team",
        "Deploy to staging environment",
        "Conduct user acceptance testing",
    ]
    
    # Generate the PDF
    pdf_path = generate_pdf(title, sample_items)
    print(f"PDF created successfully at: {pdf_path}")