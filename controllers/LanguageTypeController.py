class LanguageTypeController:
    def __init__(self,view):
        self.view = view
        
    def determine_language_type(self):
        input_text = self.view.entry.get()
        print(f"Texto ingresado: {input_text}")

        
        