import tkinter as tk
from tkinter import filedialog

class PropertyEditor(tk.Toplevel):
    def __init__(self, root, properties, config):
        super().__init__(root)
        self.title('Property Editor')
        self.config = config
        self.properties = properties

        for index, prop in enumerate(self.properties):
            label = tk.Label(self, text=prop['prompt'])
            label.grid(row=index, column=0, sticky='e', padx=5, pady=5)

            if prop['property_type'] == 'string':
                entry = tk.Entry(self)
                entry.grid(row=index, column=1, sticky='w', padx=5, pady=5)
                value = prop.get('value', prop['default_value'])
                if value:
                    entry.insert(0, value)
                prop['widget'] = entry

            elif prop['property_type'] == 'directory':
                frame = tk.Frame(self)
                frame.grid(row=index, column=1, sticky='w', padx=5, pady=5)

                entry = tk.Entry(frame)
                entry.pack(side=tk.LEFT)
                value = prop.get('value', prop['default_value'])
                if value:
                    entry.insert(0, value)
                prop['widget'] = entry

                button = tk.Button(frame, text='...', command=lambda p=prop: self.browse_directory(p))
                button.pack(side=tk.LEFT, padx=(5, 0))

        save_button = tk.Button(self, text='Save', command=self.save)
        save_button.grid(row=index+1, column=0, columnspan=2, pady=10)


        # Get main window's geometry
        main_x = root.winfo_x()
        main_y = root.winfo_y()
        main_width = root.winfo_width()
        main_height = root.winfo_height()

        # Wait for the dialog to get its dimensions
        self.update_idletasks()

        # Calculate the position to center the About dialog over the main window
        about_width = self.winfo_width()
        about_height = self.winfo_height()
        pos_x = main_x + (main_width // 2) - (about_width // 2)
        pos_y = main_y + (main_height // 2) - (about_height // 2)

        # Set the About dialog's position
        self.geometry(f"+{pos_x}+{pos_y}")


    def browse_directory(self, prop):
        directory = filedialog.askdirectory()
        if directory:
            prop['widget'].delete(0, tk.END)
            prop['widget'].insert(0, directory)

    def save(self):
        for prop in self.properties:
            prop['value'] = prop['widget'].get()

        self.config.save()

        self.destroy()
