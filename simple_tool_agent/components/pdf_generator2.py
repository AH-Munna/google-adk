# Import necessary libraries
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER # Import TA_CENTER
import math
import os
import re # For filename sanitization

def sanitize_filename(filename_base: str) -> str:
    """Sanitizes a string to be used as a safe filename."""
    s = filename_base.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s) # Remove non-alphanumeric, non-whitespace, non-hyphen
    s = re.sub(r'[-\s]+', '_', s) # Replace hyphens and spaces with underscores
    return s if s else "untitled_document"

def generate_pdf(title: str, items: list[str]) -> dict:
    """
    Generate a PDF with a title and a list of items formatted as a checklist.
    Long items will wrap to the next line.
    Parameters:
    title (str): The title of the document.
    items (list): A list of strings to be displayed as checklist items.
    """
    output_filename = f"{title.lower().replace(' ', '_')}.pdf"
    # Set up the canvas
    c = canvas.Canvas(output_filename, pagesize=letter)
    safe_title_base = sanitize_filename(title)
    output_filename = f"{safe_title_base}.pdf"
    width, height = letter

    # Set up styles and sizes
    styles = getSampleStyleSheet()
    # Using 'Normal' style as a base for items
    item_style = styles['Normal']
    # Keep item font size consistent
    item_style.fontSize = 12
    # Adjust leading (space between lines)
    item_style.leading = 14
    title_font_size = 20
    checkbox_size = 10
    # Vertical gap between items
    item_gap = 8
    # Top and side padding
    padding = 50

    # --- Draw Title ---
    title_style = styles['h1']
    title_style.fontSize = title_font_size
    title_style.alignment = TA_CENTER

    title_p = Paragraph(title, title_style)
    # Calculate width/height needed for title, allowing wrap
    # Note: c (canvas) is passed to wrapOn for font metrics, not for drawing here.
    title_w, title_h = title_p.wrapOn(c, width - 2 * padding, height)

    # Calculate title y position
    title_y = height - padding - title_h
    # Draw title centered
    title_p.drawOn(c, padding, title_y)

    # Starting y position for the first checklist item
    # Adjusted to account for actual title height
    current_y = title_y - item_gap * 2
    warnings = []

    # --- Draw Checklist Items ---
    # Determine if two columns are needed (heuristic based on item count)
    use_two_columns = len(items) > 8 # Adjust this threshold as needed

    if use_two_columns:
        col_width = (width - 3 * padding) / 2
        # Width available for text next to checkbox
        item_available_width = col_width - checkbox_size - 5
        items_per_column = math.ceil(len(items) / 2)
        col1_y = current_y
        col2_y = current_y
        col1_x = padding
        col2_x = padding + col_width + padding

        for i, item_text in enumerate(items):
            # Create Paragraph object for the item
            p = Paragraph(item_text, item_style)

            if i < items_per_column:
                # Column 1
                item_x = col1_x
                # Calculate required paragraph height based on available width
                w, h = p.wrapOn(c, item_available_width, height) # Height limit is less critical here
                # Check if item fits vertically in the column
                if col1_y - h < padding:
                    warnings.append(f"Content might exceed page height in column 1 for item: '{item_text[:30]}...'. Item and subsequent items in this column might be truncated.")
                    # Basic overflow handling: stop adding items (or add page break logic)
                    break
                 # Adjust y position for drawing: draw from bottom-left
                draw_y = col1_y - h
                # Draw checkbox (aligned slightly below the top of the paragraph)
                c.rect(item_x, draw_y + h - item_style.fontSize + 2, checkbox_size, checkbox_size)
                # Draw paragraph text
                p.drawOn(c, item_x + checkbox_size + 5, draw_y)
                # Update y position for the next item in this column
                col1_y -= (h + item_gap)
            else:
                # Column 2
                item_x = col2_x
                # Calculate required paragraph height
                w, h = p.wrapOn(c, item_available_width, height)
                # Check if item fits vertically
                if col2_y - h < padding:
                    warnings.append(f"Content might exceed page height in column 2 for item: '{item_text[:30]}...'. Item and subsequent items in this column might be truncated.")
                    break
                # Adjust y position for drawing
                draw_y = col2_y - h
                # Draw checkbox
                c.rect(item_x, draw_y + h - item_style.fontSize + 2, checkbox_size, checkbox_size)
                # Draw paragraph text
                p.drawOn(c, item_x + checkbox_size + 5, draw_y)
                # Update y position for next item
                col2_y -= (h + item_gap)

    else:
        # Single column layout
        # Width available for text
        item_available_width = width - 2 * padding - checkbox_size - 5
        item_x = padding

        for item_text in items:
            # Create Paragraph object
            p = Paragraph(item_text, item_style)
            # Calculate required height
            w, h = p.wrapOn(c, item_available_width, height)
             # Check if item fits vertically on page
            if current_y - h < padding:
                warnings.append(f"Content might exceed page height for item: '{item_text[:30]}...'. Item and subsequent items might be truncated.")
                break # Basic overflow handling
            # Adjust y position for drawing
            draw_y = current_y - h
            # Draw checkbox
            c.rect(item_x, draw_y + h - item_style.fontSize + 2, checkbox_size, checkbox_size)
            # Draw paragraph text
            p.drawOn(c, item_x + checkbox_size + 5, draw_y)
            # Update y position for next item
            current_y -= (h + item_gap)

    c.save()
    abs_path = os.path.abspath(output_filename)
    
    result = {
        "status": "success" if not warnings else "warning_content_truncated",
        "report": f"PDF created at {abs_path}",
    }
    if warnings:
        result["warnings"] = warnings
    
    return result