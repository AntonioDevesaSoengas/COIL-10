from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Crear el cuadro de texto
        self.text_input = TextInput(hint_text='Escribe aquí...')
        layout.add_widget(self.text_input)

        # Crear un botón que muestra el mensaje
        button = Button(text="Mostrar Mensaje")
        button.bind(on_press=self.show_message)
        layout.add_widget(button)

        # Etiqueta para mostrar el mensaje
        self.label = Label(text="")
        layout.add_widget(self.label)

        return layout

    # Función para mostrar el mensaje
    def show_message(self, instance):
        message = self.text_input.text  # Obtiene el texto del cuadro de texto
        self.label.text = f"Has escrito: {message}"  # Actualiza la etiqueta con el mensaje

if __name__ == '__main__':
    MyApp().run()
