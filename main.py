from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests
import re
from urllib.parse import urlparse, parse_qs
from kivy.utils import platform
from kivy.core.clipboard import Clipboard


class SoundCloudLinkConverter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10)

        # Input field for shared text
        self.input_label = Label(text="Paste SoundCloud shared text:", size_hint=(1, 0.1))
        self.input_text = TextInput(multiline=True, size_hint=(1, 0.4))
        self.add_widget(self.input_label)
        self.add_widget(self.input_text)

        # Convert button
        self.convert_button = Button(text="Convert Link", size_hint=(1, 0.1))
        self.convert_button.bind(on_press=self.convert_link)
        self.add_widget(self.convert_button)

        # Output field for full URL
        self.output_label = Label(text="Full SoundCloud URL:", size_hint=(1, 0.1))
        self.output_text = TextInput(readonly=True, multiline=False, size_hint=(1, 0.2))
        self.add_widget(self.output_label)
        self.add_widget(self.output_text)

        # Copy to clipboard button
        self.copy_button = Button(text="Copy to Clipboard", size_hint=(1, 0.1))
        self.copy_button.bind(on_press=self.copy_to_clipboard)
        self.add_widget(self.copy_button)

    def convert_link(self, instance):
        shared_text = self.input_text.text.strip()

        # Extract the shortened URL from the shared text
        url_pattern = r'https://on\.soundcloud\.com/[^\s]+'
        match = re.search(url_pattern, shared_text)
        if not match:
            self.output_text.text = "No valid SoundCloud URL found."
            return

        shortened_url = match.group(0)

        try:
            # Follow the redirect to get the full URL
            response = requests.head(shortened_url, allow_redirects=True)
            full_url = response.url

            # Clean the URL by removing query parameters after the main path
            parsed_url = urlparse(full_url)
            clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            self.output_text.text = clean_url
        except requests.RequestException:
            self.output_text.text = "Error resolving URL. Please check your input or internet connection."

    def copy_to_clipboard(self, instance):
        if self.output_text.text and "Error" not in self.output_text.text:
            Clipboard.copy(self.output_text.text)


class SoundCloudApp(App):
    def build(self):
        return SoundCloudLinkConverter()


if __name__ == '__main__':
    SoundCloudApp().run()