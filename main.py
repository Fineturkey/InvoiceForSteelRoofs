import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas as pdf_canvas

# Initialize the main window
root = tk.Tk()
root.title("PDF Drawing Application with Invoice")
root.geometry("800x800")

# Canvas for displaying and drawing on the PDF
draw_canvas = tk.Canvas(root, bg="white", width=600, height=600)
draw_canvas.pack(pady=20)

# Variables to store drawing and PDF state
start_x, start_y = None, None
end_x, end_y = None, None
drawn_shapes = []  # Store (start_x, start_y, end_x, end_y) tuples
pdf_path = None
pdf_image = None

# Function to load PDF and set it as background
def load_pdf():
    global pdf_path, pdf_image
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    if pdf_path:
        doc = fitz.open(pdf_path)
        page = doc[0]  # Load the first page for simplicity
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pdf_image = ImageTk.PhotoImage(img)
        
        draw_canvas.create_image(0, 0, anchor="nw", image=pdf_image)
        draw_canvas.config(scrollregion=draw_canvas.bbox("all"))
        doc.close()

# Function to start drawing
def start_draw(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

# Function to finalize and draw a straight line
def draw(event):
    global start_x, start_y, end_x, end_y
    end_x, end_y = event.x, event.y
    
    # Remove existing temporary line
    draw_canvas.delete("temp_line")
    
    if start_x and start_y:
        # Draw temporary line
        draw_canvas.create_line(start_x, start_y, end_x, end_y, fill="black", width=2, tags="temp_line")

# Function to reset start position and store line
def reset_draw(event):
    global start_x, start_y, end_x, end_y
    if start_x and start_y and end_x and end_y:
        # Draw final line
        line = draw_canvas.create_line(start_x, start_y, end_x, end_y, fill="black", width=2)
        drawn_shapes.append((start_x, start_y, end_x, end_y))  # Store line coordinates
    
    # Reset positions
    start_x, start_y, end_x, end_y = None, None, None, None

# Function to generate an invoice PDF
def generate_invoice():
    if not drawn_shapes:
        messagebox.showwarning("No Drawings", "There are no drawings to invoice.")
        return
    
    save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    
    if save_path:
        c = pdf_canvas.Canvas(save_path)
        c.drawString(100, 750, "Invoice for Drawn Annotations")
        
        item_count = len(drawn_shapes)
        total_cost = item_count * 5  # Example cost of $5 per item
        c.drawString(100, 730, f"Items drawn: {item_count}")
        c.drawString(100, 710, f"Total cost: ${total_cost}")
        
        # List of items on the invoice
        for i, (sx, sy, ex, ey) in enumerate(drawn_shapes, start=1):
            c.drawString(100, 710 - i * 20, f"Item {i}: Line from ({sx}, {sy}) to ({ex}, {ey})")
        
        c.save()
        messagebox.showinfo("Invoice Saved", f"Invoice saved to {save_path}")

#def generatePDF():
#    pdf_image

# Bind mouse events to canvas for drawing
draw_canvas.bind("<Button-1>", start_draw)  # Left click to start drawing
draw_canvas.bind("<B1-Motion>", draw)       # Move mouse while holding left button
draw_canvas.bind("<ButtonRelease-1>", reset_draw)  # Release left button to finalize

# Buttons for loading PDF and generating invoice
load_pdf_button = tk.Button(root, text="Load PDF", command=load_pdf)
load_pdf_button.pack(pady=10)
#load_pdf_button = tk.Button(root, text="Generate PDF", command=generatePDF)
invoice_button = tk.Button(root, text="Generate Invoice", command=generate_invoice)
invoice_button.pack(pady=10)

# Start the main loop
root.mainloop()

