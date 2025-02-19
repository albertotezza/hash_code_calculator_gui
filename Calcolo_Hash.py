import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from os import chdir
from os.path import realpath
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import messagebox
import pyperclip


class MainPage(TkinterDnD.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gui_dir = Path(realpath(__file__)).parent
        chdir(gui_dir)

        # GUI title
        self.title("Calcolo Hash Code - Embedded FCU")
        self.iconbitmap("hash_icon.ico")

        self.Tab_CRC16 = [0x0000, 0xc0c1, 0xc181, 0x0140, 0xc301, 0x03c0, 0x0280, 0xc241, 0xc601, 0x06c0, 0x0780, 0xc741, 0x0500, 0xc5c1, 0xc481, 0x0440,
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
                        0x4400, 0x84c1, 0x8581, 0x4540, 0x8701, 0x47c0, 0x4680, 0x8641, 0x8201, 0x42c0, 0x4380, 0x8341, 0x4100, 0x81c1, 0x8081, 0x4040 ]
        
        self.HASH_CODE = []


        # MAIN FRAME -------------------------------------------------------------------------------------------------------------------------------------
        
        # INPUT ------------------------------------------------------------------------------------------------------------------------------------------
        main_frame = tk.Frame()
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        # Label
        self.input_label = tk.Label(main_frame, text="BLUETOOTH MAC ADDRESS:", font=("Arial", 10, "bold"))
        self.input_label.grid(row=0, column=0, columnspan=10, padx=5, pady=[15,0], sticky="w")

        # MAC Address entries
        # Ciclo per creare variabili e Entry widgets
        for i in range(1, 7):
            
            # Crea Label
            self.pos_label = tk.Label(main_frame, text=f'{i}:')
            self.pos_label.grid(row=1, column=i, padx=5, pady=[10,0], sticky="w")

            # Crea una variabile StringVar dinamica
            setattr(self, f'MAC{i}_str', tk.StringVar())
            # Crea un widget Entry per ogni MAC
            entry_widget = tk.Entry(main_frame, textvariable=getattr(self, f'MAC{i}_str'), justify="center", width=5)
            # Posiziona il widget nella griglia
            entry_widget.grid(row=2, column=i, padx=5, pady=[0,10], sticky="w")


        # Pulsante Calcola
        self.calc_button = tk.Button(main_frame, text="Calcola", command=self.check_entries)
        self.calc_button.grid(row=1, column=11, rowspan=2, padx=15, pady=10, sticky="s")

        # Reset button to select the directory
        self.reset_button = tk.Button(main_frame, text="Reset",command=self.reset_entries)
        self.reset_button.grid(row=2, column=11, rowspan=2, padx=10, pady=10, sticky="s")
        
        # ------------------------------------------------------------------------------------------------------------------------------------------------


        # OUTOUT # ---------------------------------------------------------------------------------------------------------------------------------------
        # Label
        self.output_label = tk.Label(main_frame, text="HASH CODE:", font=("Arial", 10, "bold"))
        self.output_label.grid(row=3, column=0, columnspan=10, padx=5, pady=[15,0], sticky="w")

        # HASH Address entries
        # Ciclo per creare variabili e Entry widgets
        for i in range(1, 11):
            # Crea una variabile StringVar dinamica
            setattr(self, f'HASH{i}_str', tk.StringVar())

            # Crea un widget Entry per ogni MAC
            entry_widget = tk.Entry(main_frame, textvariable=getattr(self, f'HASH{i}_str'), justify="center", state="readonly", width=5)

            # Crea Label
            self.pos_label = tk.Label(main_frame, text=f'{i}:')
            self.pos_label.grid(row=4, column=i, padx=5, pady=[10,0], sticky="w")

            # Posiziona il widget nella griglia
            entry_widget.grid(row=5, column=i, padx=5, pady=[0,10], sticky="w")

        # Copy button
        self.copy_button = tk.Button(main_frame, text="Copy",command=self.copy_entries)
        self.copy_button.grid(row=4, column=11, rowspan=2, padx=10, pady=10, sticky="s")
        
        # ------------------------------------------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------------------------------------


        # SECOND FRAME (Screenshot) ----------------------------------------------------------------------------------------------------------------------
        second_frame = tk.Frame()
        second_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

        img = Image.open(gui_dir.joinpath("Screenshot_20250203_090509_ST25.png"))
        width, height = img.size  # Ottieni le dimensioni dell'immagine
        img = img.resize((int(width*0.45), int(height*0.45)))  # Ridimensiona l'immagine

        # Converte l'immagine in un formato che Tkinter può usare
        img_tk = ImageTk.PhotoImage(img)

        # Crea un widget Label per visualizzare l'immagine
        label = tk.Label(second_frame, image=img_tk)
        label.img = img_tk  # This line holds the reference (evito "garbage collected")
        label.grid(row=0, column=20, columnspan=10, padx=15, pady=15, sticky="w")
        # ------------------------------------------------------------------------------------------------------------------------------------------------


    # Funzione calcolo CRC-16
    def crc16_modbus(self, data: bytes):
        
        crc=0xFFFF
        
        # data = [int(n,16) for n in data]

        for byte in data:
            crc = self.Tab_CRC16[(crc ^ byte ) & 0x0ff] ^ (crc >> 8)
        
        return crc & 0xFFFF  # Ensure the CRC is limited to 16 bits


    # Check sui valori inseriti prima di lanciare il calcolo dell'HASH Code
    def check_entries(self):
        # Controlla che ogni Entry abbia esattamente 2 caratteri
        for i in range(1,7):
            mac_value = getattr(self, f'MAC{i}_str').get()
            if len(mac_value) != 2:
                # Se uno dei valori non è esattamente di 2 caratteri, mostra un messaggio di errore
                messagebox.showerror("Errore", f"Completa ogni casella con 2 caratteri")
                return  # Interrompe la funzione se c'è un errore

        # Se tutti i valori sono corretti, esegui i calcoli (qui un esempio di calcolo)
        self.calcola_hash_code()


    # MAIN FUNCTION:
    def calcola_hash_code(self):

        # BT_MAC = [0xdc, 0xda, 0x0c, 0x88, 0xbe, 0xce]
        BT_MAC = []
        for i in range(1,7):
            try:
                el = int(getattr(self, f'MAC{i}_str').get(), 16)
                BT_MAC .append(el)
            except Exception as e:
                messagebox.showerror("Errore", e)
                return

        # print(BT_MAC)
        
        BT_HASH = []
        for HashIndex in range(5):
            Buff = []
            for i in range(6):
                Buff.append(BT_MAC[(i+HashIndex) % 6])

            BT_HASH.append(self.crc16_modbus(Buff))

        BT_HASH = [hex(num) for num in BT_HASH]

        # print(BT_HASH)

        normalized = []
        for hex_value in BT_HASH:
            # Rimuovere il prefisso '0x'
            hex_value = hex_value[2:]

            # Aggiungere zeri a sinistra fino a che la lunghezza non diventa 4
            hex_value = hex_value.zfill(4)
            normalized.append(hex_value)

        # print(normalized)

        # Creare una lista di coppie di caratteri
        splitted = []
        for el in normalized:
            # Splittiamo ogni stringa in coppie di 2 caratteri
            for i in range(0, len(el), 2):
                splitted.append(el[i:i+2])

        # Imposta valori nella GUI
        for i, el in enumerate(splitted):
            getattr(self, f'HASH{i+1}_str').set(el)  # Imposta il valore
        print(splitted)


    # Reset Mac Address inputs
    def reset_entries(self):
        # Resetta tutte le Entry
        for i in range(1,7):
            getattr(self, f'MAC{i}_str').set("")  # Imposta la StringVar a una stringa vuota


    # Copia Hash Code calcolato
    def copy_entries(self):
        self.HASH_CODE = []
        # Copia tutte le Entry
        for i in range(1,11):
            self.HASH_CODE.append(getattr(self, f'HASH{i}_str').get())  # Imposta la StringVar a una stringa vuota

        hex_string = ''.join(self.HASH_CODE)
        pyperclip.copy(hex_string) # Copia la stringa negli appunti



if __name__ == '__main__':
    app = MainPage()
    app.mainloop()
