import pyautogui
import keyboard
import time
import logging
import sys
from PIL import ImageGrab
import pytesseract
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler('assistant.log'), logging.StreamHandler(sys.stdout)])

class SafariAutomatedAssistant:
    def __init__(self):
        self.running = False
        self.setup_browser()
        
    def setup_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.webkit.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("https://claude.ai")
        print("Please log in to Claude.ai...")
        input("Press Enter once logged in...")

    def start(self):
        if not self.running:
            self.running = True
            print("Assistant started - Press Ctrl+C to stop")
            self.monitor_loop()

    def stop(self):
        self.running = False
        self.context.close()
        self.browser.close()
        self.playwright.stop()
        print("Assistant stopped")

    def get_screen_text(self):
        screenshot = ImageGrab.grab()
        return pytesseract.image_to_string(screenshot)

    def ask_claude(self, prompt):
        try:
            input_field = self.page.locator("[placeholder='Message Claude...']")
            input_field.clear()
            input_field.fill(prompt)
            input_field.press("Enter")
            
            response = self.page.locator(".claude-response").last
            response.wait_for(state="visible", timeout=30000)
            return response.text_content()

        except Exception as e:
            print(f"Error communicating with Claude: {str(e)}")
            return None

    def execute_action(self, action_text):
        try:
            if "MOUSE_MOVE:" in action_text:
                coords = action_text.split("MOUSE_MOVE:")[1].strip().split(",")
                pyautogui.moveTo(int(coords[0]), int(coords[1]))
            elif "MOUSE_CLICK" in action_text:
                pyautogui.click()
            elif "TYPE:" in action_text:
                text = action_text.split("TYPE:")[1].strip()
                pyautogui.write(text)
            elif "HOTKEY:" in action_text:
                keys = action_text.split("HOTKEY:")[1].strip().split("+")
                pyautogui.hotkey(*keys)
                
            print(f"Executed action: {action_text}")
            
        except Exception as e:
            print(f"Error executing action: {str(e)}")

    def monitor_loop(self):
        try:
            while self.running:
                if keyboard.is_pressed('ctrl+shift+a'):
                    screen_text = self.get_screen_text()
                    prompt = f"""
                    Current screen content:
                    {screen_text}
                    
                    What action should be taken? Respond with one of:
                    MOUSE_MOVE:x,y
                    MOUSE_CLICK
                    TYPE:text
                    HOTKEY:key1+key2
                    """
                    
                    response = self.ask_claude(prompt)
                    if response:
                        self.execute_action(response)
                    
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

if __name__ == "__main__":
    assistant = SafariAutomatedAssistant()
    assistant.start()