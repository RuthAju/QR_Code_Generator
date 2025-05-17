# # Import necessary libraries
# import qrcode
# from PIL import Image

# # Load the logo image
# logo = Image.open(r"C:\Users\USER\Desktop\Data Engineering\calc_image\LF3.png")  # Load the logo image

# # Create a QR code with high error correction level
# qr_code = qrcode.QRCode(
#     error_correction=qrcode.constants.ERROR_CORRECT_H  # Allows up to 30% damage tolerance
# )

# # Add the data (URL) to the QR code
# qr_code.add_data("www.linkedin.com/in/ruthaju")  # Embed the URL
# qr_code.make()  # Generate the QR code

# # Customize the QR code colors and convert to RGBA format
# img_qr_code = qr_code.make_image(fill_color="purple", back_color="white").convert('RGBA')

# # Calculate the position to center the logo
# logo_pos = (
#     (img_qr_code.size[0] - logo.size[0]) // 2,  # Horizontal centering
#     (img_qr_code.size[1] - logo.size[1]) // 2   # Vertical centering
# )

# # Paste the logo onto the QR code
# img_qr_code.paste(logo, logo_pos)

# # Save the final QR code with logo as an image file
# img_qr_code.save(r"C:\Users\USER\Desktop\Data Engineering\QR_code\Qr_code.png")  # Save the image



import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom QR Code Generator")
        self.root.geometry("450x550")

        self.logo_path = None
        self.fill_color = "#000000"  # Default black
        self.bg_color = "#FFFFFF"    # Default white
        self.save_path = ""          # Output file path

        # Input: Data to encode
        tk.Label(root, text="Data to encode (URL, text, etc):").pack()
        self.data_entry = tk.Entry(root, width=50)
        self.data_entry.pack(pady=5)

        # Logo Upload
        tk.Button(root, text="Upload Logo", command=self.upload_logo).pack(pady=5)

        # Color Pickers
        tk.Button(root, text="Choose Fill Color", command=self.pick_fill_color).pack(pady=5)
        tk.Button(root, text="Choose Background Color", command=self.pick_bg_color).pack(pady=5)

        # Save Location
        tk.Label(root, text="Select Save Location:").pack()
        self.save_path_entry = tk.Entry(root, width=40)
        self.save_path_entry.pack(pady=5)
        tk.Button(root, text="Browse Save Location", command=self.choose_save_path).pack(pady=5)

        # Generate Button
        tk.Button(root, text="Generate QR Code", command=self.generate_qr).pack(pady=10)

        # Display Area
        self.qr_label = tk.Label(root)
        self.qr_label.pack(pady=10)

    def upload_logo(self):
        self.logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.logo_path:
            messagebox.showinfo("Logo Selected", f"Logo loaded:\n{self.logo_path}")

    def pick_fill_color(self):
        color_code = colorchooser.askcolor(title="Choose QR Fill Color")
        if color_code[1]:
            self.fill_color = color_code[1]

    def pick_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose QR Background Color")
        if color_code[1]:
            self.bg_color = color_code[1]

    def choose_save_path(self):
        self.save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            title="Save QR Code"
        )
        if self.save_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, self.save_path)

    def generate_qr(self):
        data = self.data_entry.get()
        save_path = self.save_path_entry.get()

        if not data:
            messagebox.showerror("Error", "Please enter data to encode.")
            return
        if not save_path:
            messagebox.showerror("Error", "Please choose a save location.")
            return

        # Create QR code
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(data)
        qr.make()
        img_qr = qr.make_image(fill_color=self.fill_color, back_color=self.bg_color).convert('RGBA')

        # Add logo if provided
        if self.logo_path:
            logo = Image.open(self.logo_path)
            logo = logo.resize((50, 50), Image.LANCZOS)
            pos = (
                (img_qr.size[0] - logo.size[0]) // 2,
                (img_qr.size[1] - logo.size[1]) // 2
            )
            img_qr.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

        # Save and show
        try:
            img_qr.save(save_path)
            img_qr.thumbnail((200, 200))
            img_display = ImageTk.PhotoImage(img_qr)
            self.qr_label.config(image=img_display)
            self.qr_label.image = img_display
            messagebox.showinfo("Success", f"QR Code saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Failed to save QR Code.\n{str(e)}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
