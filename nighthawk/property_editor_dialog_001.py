import tkinter as tk

from nighthawk.centered_dialog_mixin import CenteredDialogMixin
from nighthawk.property_editor import CheckboxPropertyEditor, DirectoryPropertyEditor, FilenamePropertyEditor, RadioSelectPropertyEditor, StringPropertyEditor

class PropertyEditorDialog(tk.Toplevel, CenteredDialogMixin):
    def __init__(self, root, properties, config):        
        super().__init__(root)
        self.transient(root)
        self.title('Property Editor')
        self.config = config
        self.properties = properties
        self.editors = []


         # Create main frame with grid layout
        main_frame = tk.Frame(self, bg="white")
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create canvas with scrollbar
        self.canvas = tk.Canvas(main_frame, bg="grey", highlightthickness=0)
        #self.canvas.create_window((0, 0), window=canvas_frame, anchor="nw", tags="canvas_frame")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.grid_columnconfigure(0, weight=1)  # Add this line
        
        v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set)
        
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.grid(row=0, column=0, sticky='nswe')

        # Configure row and column weights of main_frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Create a frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.scrollable_frame, anchor='nw')


        for index, prop in enumerate(self.properties):

            panel = tk.Frame(self.scrollable_frame, borderwidth=1, relief=tk.SUNKEN)
            panel.grid(row=index, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)            
            
            label = tk.Label(panel, text=prop['prompt'])
            label.grid(row=0, column=0, sticky='en', padx=5, pady=5)

            prop_editor = None
            if prop['property_type'] == 'string':
                prop_editor = StringPropertyEditor(panel, prop, index)
                
            elif prop['property_type'] == 'directory':
                prop_editor = DirectoryPropertyEditor(panel, prop, index)

            elif prop['property_type'] == 'filename':
                prop_editor = FilenamePropertyEditor(panel, prop, index)

            elif prop['property_type'] == 'checkbox':
                prop_editor = CheckboxPropertyEditor(panel, prop, index)

            elif prop['property_type'] == 'radio':
                prop_editor = RadioSelectPropertyEditor(panel, prop, index)

            # ChoicePropertyEditor

            # TextPropertyEditor

            # AgreementPropertyEditor

            # NumberPropertyEditor


            if not prop_editor:
                raise Exception(f'Unknown property type: {prop["property_type"]}')        
            else:
                self.editors.append(prop_editor)
                prop['prop_editor'] = prop_editor  # Store the PropertyEditor instance in the prop dictionary
                #prop_editor.grid(row=0, column=1, sticky='ew', padx=5, pady=5)  # Modify the sticky option


        # Bind the function to update the scrollregion
        self.scrollable_frame.bind("<Configure>", self.update_scrollregion)


        # Add button container below the canvas
        button_container = tk.Frame(main_frame)
        button_container.grid(row=1, column=0, columnspan=2)

        save_button = tk.Button(button_container, text='Save', command=self.save)
        save_button.grid(row=0, column=0, pady=10)

        cancel_button = tk.Button(button_container, text='Cancel', command=self.cancel)
        cancel_button.grid(row=0, column=1, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set()
        self.center_over_master()
        self.wait_window(self)

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save(self):
        for prop in self.properties:
            if prop.get('property_type') not in ['label', 'separator']:
                prop['value'] = prop['prop_editor'].get_value()
                section = prop['section']
                key = prop['key']
                value = prop['value']
                self.config.set(section, key, value)

        self.config.save()
        self.close()

    def cancel(self):
        self.master.focus_set()
        self.close()

    def close(self):
        self.destroy()