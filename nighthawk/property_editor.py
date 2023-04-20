import os
import tkinter as tk
from tkinter import filedialog

class PropertyEditor():

    def __init__(self, panel, prop, index):
        self.panel = panel
        self.prop = prop
        self.index = index

        self.container = tk.Frame(panel)
        self.container.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        self.container.grid_columnconfigure(0, weight=1)  # Add this line
    
        self.create_ui()

    def create_ui(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_value(self):
        raise NotImplementedError("Subclasses must implement the 'get_value' method")

class StringPropertyEditor(PropertyEditor):
    def __init__(self, panel, prop, index):
        super().__init__(panel, prop, index)

    def create_ui(self):
        value = self.prop.get('value', '')
        self.var = tk.StringVar(value=value)
        self.entry = tk.Entry(self.container, textvariable=self.var, width=1)
        self.entry.pack(fill='both', expand=True)
        
        #self.entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)  # Modify the sticky option
        #self.panel.grid_columnconfigure(1, weight=1)  # Add this line

    def get_value(self):
        return self.var.get()

    # def create_ui(self):
    #     entry = tk.Entry(self.panel)
    #     entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)        
    #     self.panel.grid_columnconfigure(1, weight=1)  # Add this line
        
    #     value = self.prop.get('value', self.prop['default_value'])
    #     if value:
    #         entry.insert(0, value)
    #     self.prop['widget'] = entry

    # def get_value(self):
    #     return self.prop['widget'].get()

class DirectoryPropertyEditor(PropertyEditor):

    def __init__(self, panel, prop, index):
        super().__init__(panel, prop, index)

    def create_ui(self):

        entry = tk.Entry(self.container)
        entry.pack(side=tk.LEFT)
        value = self.prop.get('value', self.prop['default_value'])
        if value:
            entry.insert(0, value)
        self.prop['widget'] = entry

        button = tk.Button(self.container, text='...', command=self.browse_directory)
        button.pack(side=tk.LEFT, padx=(5, 0))

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.prop['widget'].delete(0, tk.END)
            self.prop['widget'].insert(0, directory)

    def get_value(self):
        return self.prop['widget'].get()
    
class FilenamePropertyEditor(PropertyEditor):

    def __init__(self, panel, prop, index):
        super().__init__(panel, prop, index)

    def create_ui(self):

        entry = tk.Entry(self.container)
        entry.pack(side=tk.LEFT)
        value = self.prop.get('value', self.prop['default_value'])
        if value:
            entry.insert(0, value)
        self.prop['widget'] = entry

        button = tk.Button(self.container, text='...', command=self.browse_file)
        button.pack(side=tk.LEFT, padx=(5, 0))

    def browse_file(self):
        filetypes = self.prop.get('filetypes', [('All Files', '*.*')])
        initialdir = self.prop.get('initialdir', os.path.expanduser("~"))
        filename = filedialog.askopenfilename(initialdir=initialdir, filetypes=filetypes)
        if filename:
            self.prop['widget'].delete(0, tk.END)
            self.prop['widget'].insert(0, filename)    

    def get_value(self):
        return self.prop['widget'].get()
    
class CheckboxPropertyEditor(PropertyEditor):

    def __init__(self, panel, prop, index):
        super().__init__(panel, prop, index)

    def create_ui(self):
                        
        value = self.prop.get('value', self.prop['default_value'])
        self.var = tk.BooleanVar()

        if value is not None:
            self.var.set(value)
        else:
            self.var.set(False)

        checkbox = tk.Checkbutton(self.container, variable=self.var, text=self.prop['prompt'])
        checkbox.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        self.prop['widget'] = checkbox

    def get_value(self):
        return self.var.get()

class RadioSelectPropertyEditor(PropertyEditor):

    def __init__(self, panel, prop, index):
        super().__init__(panel, prop, index)

    def create_ui(self):
        options = self.prop['options']
        var = tk.StringVar()
        var.set(self.prop.get('value', self.prop['default_value']))

        for index, option in enumerate(options):
            radio = tk.Radiobutton(self.container, text=option, variable=var, value=option)
            radio.grid(row=0, column=1 + index, sticky='w', padx=(5 if index == 0 else 0), pady=5)

        self.prop['widget'] = var
    
    def get_value(self):
        return self.prop['widget'].get()