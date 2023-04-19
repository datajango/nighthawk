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

        for index, prop in enumerate(self.properties):

            panel = tk.Frame(self, borderwidth=1, relief=tk.SUNKEN)
            panel.grid(row=index, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

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



        save_button = tk.Button(self, text='Save', command=self.save)
        save_button.grid(row=index+1, column=0, columnspan=2, pady=10)

        cancel_button = tk.Button(self, text='Cancel', command=self.cancel)
        cancel_button.grid(row=index+1, column=1, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set()
        self.center_over_master()
        self.wait_window(self)


    def save(self):
        # for prop in self.properties:
        #     # prop['value'] = prop['widget'].get()

        #     # # Convert non-string values to strings
        #     # if prop['property_type'] in ['integer', 'float', 'boolean', 'list']:
        #     #     prop['value'] = str(prop['value'])

        #     prop_editor = prop.get('property_editor')
        #     if prop_editor:
        #         prop['value'] = prop_editor.get_value()
        #     else:
        #         prop['value'] = prop['widget'].get()
        #     self.config.set(prop['section'], prop['key'], prop['value'])

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