from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from pyproj import Transformer

class ConversorUTM(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text="WGS84 -> UTM SAD69", font_size='22sp', bold=True))
        
        self.lat_input = TextInput(multiline=False, hint_text="Latitude (ex: -25.102)")
        layout.add_widget(self.lat_input)
        
        self.lon_input = TextInput(multiline=False, hint_text="Longitude (ex: -50.640)")
        layout.add_widget(self.lon_input)
        
        btn = Button(text="CONVERTER", background_color=(0, 0.6, 1, 1), bold=True)
        btn.bind(on_press=self.calcular)
        layout.add_widget(btn)
        
        self.result_label = Label(text="Resultado aparecerá aqui", color=(1, 1, 0, 1))
        layout.add_widget(self.result_label)
        return layout

    def calcular(self, instance):
        try:
            lat = float(self.lat_input.text.replace(",", "."))
            lon = float(self.lon_input.text.replace(",", "."))
            
            fuso = int((lon + 180) / 6) + 1
            # Dicionário para SAD69 no Brasil (SUL)
            epsg_dict = {21: "EPSG:29191", 22: "EPSG:29192", 23: "EPSG:29193"}
            epsg = epsg_dict.get(fuso)
            
            if not epsg:
                self.result_label.text = "Fuso fora de alcance (21-23S)"
                return
                
            transformer = Transformer.from_crs("EPSG:4326", epsg, always_xy=True)
            x, y = transformer.transform(lon, lat)
            self.result_label.text = f"Fuso: {fuso}S\nX: {x:.3f}\nY: {y:.3f}"
        except Exception:
            self.result_label.text = "Erro: Verifique os dados."

if __name__ == '__main__':
    ConversorUTM().run()
