import tkinter as tk
from pathlib import Path
from os import chdir
from PIL import Image, ImageTk
from tkinter import messagebox
import pyperclip
import sys


class HashCalculatorApp(tk.Tk):
    """Main application class for Hash Calculator"""

    # CRC-16 MODBUS lookup table (truncated for brevity)
    CRC16_TABLE = [
        0x0000, 0xc0c1, 0xc181, 0x0140, 0xc301, 0x03c0, 0x0280, 0xc241, 0xc601, 0x06c0, 0x0780, 0xc741, 0x0500, 0xc5c1, 0xc481, 0x0440,
        0xcc01, 0x0cc0, 0x0d80, 0xcd41, 0x0f00, 0xcfc1, 0xce81, 0x0e40, 0x0a00, 0xcac1, 0xcb81, 0x0b40, 0xc901, 0x09c0, 0x0880, 0xc841,
        0xd801, 0x18c0, 0x1980, 0xd941, 0x1b00, 0xdbc1, 0xda81, 0x1a40, 0x1e00, 0xdec1, 0xdf81, 0x1f40, 0xdd01, 0x1dc0, 0x1c80, 0xdc41,
        0x1400, 0xd4c1, 0xd581, 0x1540, 0xd701, 0x17c0, 0x1680, 0xd641, 0xd201, 0x12c0, 0x1380, 0xd341, 0x1100, 0xd1c1, 0xd081, 0x1040,
        0xf001, 0x30c0, 0x3180, 0xf141, 0x3300, 0xf3c1, 0xf281, 0x3240, 0x3600, 0xf6c1, 0xf781, 0x3740, 0xf501, 0x35c0, 0x3480, 0xf441,
        0x3c00, 0xfcc1, 0xfd81, 0x3d40, 0xff01, 0x3fc0, 0x3e80, 0xfe41, 0xfa01, 0x3ac0, 0x3b80, 0xfb41, 0x3900, 0xf9c1, 0xf881, 0x3840,
        0x2800, 0xe8c1, 0xe981, 0x2940, 0xeb01, 0x2bc0, 0x2a80, 0xea41, 0xee01, 0x2ec0, 0x2f80, 0xef41, 0x2d00, 0xedc1, 0xec81, 0x2c40,
        0xe401, 0x24c0, 0x2580, 0xe541, 0x2700, 0xe7c1, 0xe681, 0x2640, 0x2200, 0xe2c1, 0xe381, 0x2340, 0xe101, 0x21c0, 0x2080, 0xe041,
        0xa001, 0x60c0, 0x6180, 0xa141, 0x6300, 0xa3c1, 0xa281, 0x6240, 0x6600, 0xa6c1, 0xa781, 0x6740, 0xa501, 0x65c0, 0x6480, 0xa441,
        0x6c00, 0xacc1, 0xad81, 0x6d40, 0xaf01, 0x6fc0, 0x6e80, 0xae41, 0xaa01, 0x6ac0, 0x6b80, 0xab41, 0x6900, 0xa9c1, 0xa881, 0x6840,
        0x7800, 0xb8c1, 0xb981, 0x7940, 0xbb01, 0x7bc0, 0x7a80, 0xba41, 0xbe01, 0x7ec0, 0x7f80, 0xbf41, 0x7d00, 0xbdc1, 0xbc81, 0x7c40,
        0xb401, 0x74c0, 0x7580, 0xb541, 0x7700, 0xb7c1, 0xb681, 0x7640, 0x7200, 0xb2c1, 0xb381, 0x7340, 0xb101, 0x71c0, 0x7080, 0xb041,
        0x5000, 0x90c1, 0x9181, 0x5140, 0x9301, 0x53c0, 0x5280, 0x9241, 0x9601, 0x56c0, 0x5780, 0x9741, 0x5500, 0x95c1, 0x9481, 0x5440,
        0x9c01, 0x5cc0, 0x5d80, 0x9d41, 0x5f00, 0x9fc1, 0x9e81, 0x5e40, 0x5a00, 0x9ac1, 0x9b81, 0x5b40, 0x9901, 0x59c0, 0x5880, 0x9841,
        0x8801, 0x48c0, 0x4980, 0x8941, 0x4b00, 0x8bc1, 0x8a81, 0x4a40, 0x4e00, 0x8ec1, 0x8f81, 0x4f40, 0x8d01, 0x4dc0, 0x4c80, 0x8c41,
        0x4400, 0x84c1, 0x8581, 0x4540, 0x8701, 0x47c0, 0x4680, 0x8641, 0x8201, 0x42c0, 0x4380, 0x8341, 0x4100, 0x81c1, 0x8081, 0x4040 
    ]

    def __init__(self):
        """Initialize the application window and components"""
        super().__init__()

        # Configure application directory and set it
        self.app_dir = Path(__file__).parent
        chdir(self.app_dir)

        self.title("Calcolo Hash Code - Embedded FCU")
        self.iconbitmap(self.app_dir.joinpath("..","resources","icons","hash_icon.ico"))

        # Shared attributes
        self.mac_vars = [tk.StringVar() for _ in range(6)]
        self.hash_vars = [tk.StringVar() for _ in range(10)]
        self.image_reference = None

        # Initialize GUI components
        self._create_frames()
        self._load_image()
        self._layout_organizer()

    # ----------------------------------------------------------------------------------------------------------------------------------

    def _create_frames(self):
        """Creates containers frame"""
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.image_frame = tk.Frame(self)
        self.image_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")


    def _load_image(self):
        """Load and prepare the image to be displayed"""
        image_path = self.app_dir.joinpath("..","resources","images","Screenshot_20250203_090509_ST25.png")
        if image_path.exists():
            try:
                original_image = Image.open(image_path)
                # Resize image
                new_size = (int(original_image.width * 0.45), 
                            int(original_image.height * 0.45))
                resized_image = original_image.resize(new_size)
                self.image_reference = ImageTk.PhotoImage(resized_image)
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            print(f"Image file not found: {image_path}")


    def _layout_organizer(self):
        """Arranges components in the window"""
        # Main frame layout
        self._create_input_section()
        self._create_output_section()

        # Image frame layout
        label = tk.Label(self.image_frame, image=self.image_reference)
        label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        label.img = self.image_reference


    def _create_input_section(self):
        """Create MAC address input section"""
        tk.Label(self.main_frame, text="BLUETOOTH MAC ADDRESS:", font=("Arial", 10, "bold"))\
            .grid(row=0, column=0, columnspan=10, padx=5, pady=(15, 0), sticky="w")

        # Create MAC Address input fields
        for i in range(6):
            col = i + 1
            tk.Label(self.main_frame, text=f"{col}:")\
                .grid(row=1, column=col, padx=5, pady=(10, 0), sticky="w")
            tk.Entry(self.main_frame, textvariable=self.mac_vars[i], justify="center", width=5)\
                .grid(row=2, column=col, padx=5, pady=(0, 10), sticky="w")

        # Position buttons
        self.calc_button = tk.Button(self.main_frame, text="Calcola", command=self.validate_entries)
        self.calc_button.grid(row=1, column=11, rowspan=2, padx=15, pady=10, sticky="s")
        self.reset_button = tk.Button(self.main_frame, text="Reset", command=self.reset_entries)
        self.reset_button.grid(row=2, column=11, rowspan=2, padx=10, pady=10, sticky="s")


    def _create_output_section(self):
        """Create Hash Code output section"""
        tk.Label(self.main_frame, text="HASH CODE:", font=("Arial", 10, "bold")).\
            grid(row=3, column=0, columnspan=10, padx=5, pady=(15, 0), sticky="w")

        # Create HASH Code output fields
        for i in range(10):
            col = i + 1
            tk.Label(self.main_frame, text=f"{col}:")\
                .grid(row=4, column=col, padx=5, pady=(10, 0), sticky="w")
            tk.Entry(self.main_frame, textvariable=self.hash_vars[i], state="readonly", justify="center", width=5)\
                .grid(row=5, column=col, padx=5, pady=(0, 10), sticky="w")

        self.copy_button = tk.Button(self.main_frame, text="Copy", command=self.copy_hash)
        self.copy_button.grid(row=4, column=11, rowspan=2, padx=10, pady=10, sticky="s")

    # ----------------------------------------------------------------------------------------------------------------------------------

    def calculate_crc16(self, data: bytes) -> int:
        """Calculate CRC-16 MODBUS checksum for given data"""
        crc = 0xFFFF
        for byte in data:
            crc = self.CRC16_TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
        return crc & 0xFFFF


    def validate_entries(self):
        """Validate MAC address input fields"""
        if all(len(var.get()) == 2 for var in self.mac_vars):
            self.calculate_hash()
        else:
            messagebox.showerror("Errore", "Completa ogni casella con 2 caratteri")


    def calculate_hash(self):
        """Main hash calculation routine"""
        try:
            mac_bytes = [int(var.get(), 16) for var in self.mac_vars]
        except ValueError as e:
            messagebox.showerror("Errore", f"Verranno ammesse solamente cifre esadecimali (0-9, A-F): \n{e}")
            return

        hash_values = []
        for index in range(5):
            buffer = [mac_bytes[(i + index) % 6] for i in range(6)]
            crc = self.calculate_crc16(bytes(buffer))
            hash_values.append(f"{crc:04x}")  # Format as 4-digit hex

        # Split into byte pairs and update UI
        byte_pairs = [pair  for value in hash_values  for pair in (value[:2], value[2:])]
        for var, pair in zip(self.hash_vars, byte_pairs):
            var.set(pair)


    def reset_entries(self):
        """Clear all input fields"""
        for var in self.mac_vars:
            var.set("")


    def copy_hash(self):
        """Copy hash code to clipboard"""
        hex_string = "".join(var.get() for var in self.hash_vars)
        pyperclip.copy(hex_string)


if __name__ == "__main__":
    app = HashCalculatorApp()
    app.mainloop()