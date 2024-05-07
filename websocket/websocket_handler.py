import websockets
import RPi.GPIO as GPIO

class RaspberryPiApp:
    def __init__(self):
        self.is_running = True

    def connect_to_server(self,message):
        uri = "ws://192.168.0.28:8080"

        with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket server at {uri}")

            while True:
                if message.lower() == 'exit':
                    break

                try:
                    websocket.send(message)

                    # Receive and print the response from the server
                    response = websocket.recv()
                    print(f"Received from server: {response}")
                    print(response)
                    break
                
                except websockets.exceptions.ConnectionClosedOK:
                    print("Server connection closed. Stopping the application...")
                self.stop()
                break


    def main_loop(self):
        while self.is_running:
            # Your asynchronous main application logic goes here
            print("Running the main loop asynchronously...")

        # checking for changes in gpio
        gpio_status_check(16)
            


        self.connect_to_server('test from application')

    def start(self):
        print("Raspberry Pi Async Application started.")
        try:
         self.main_loop()
            
        except KeyboardInterrupt:
         self.stop()

    def stop(self):
        self.is_running = False
        print("\nStopping the Raspberry Pi Async Application. Goodbye!")

if __name__ == "__main__":
    app = RaspberryPiApp()
    run(app.start())
