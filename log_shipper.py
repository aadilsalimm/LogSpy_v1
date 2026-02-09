import subprocess
import json
import sys
import select

class LogShipper:
    def __init__(self, buffer_size=10):
        self.buffer_size = buffer_size
        self.buffer = []
        self.process = None

    def start(self):
        """Starts the journalctl subprocess."""
        try:
            # -f: follow
            # -o json: output as json
            self.process = subprocess.Popen(
                ['journalctl', '-f', '-o', 'json', '-n', '0'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, # Decode bytes to string
                bufsize=1  # Line buffered
            )
            print(f"Log shipper started with buffer size {self.buffer_size}")
            self.capture_loop()
        except FileNotFoundError:
            print("Error: journalctl command not found from log_shipper.py in start method.")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting log shipper: {e}")
            sys.exit(1)

    def capture_loop(self):
        """Continuously reads from the subprocess stdout."""
        if not self.process:
            return

        try:
            while True:
                # Read a line from stdout
                line = self.process.stdout.readline()
                if not line:
                    # Process ended or stream closed
                    break
                
                self.add_to_buffer(line.strip())
                
        except KeyboardInterrupt:
            print("\nStopping log shipper...")
            self.flush_buffer() # Flush remaining logs before exit
            self.process.terminate()
        except Exception as e:
            print(f"Error in capture loop: {e}")
        finally:
            if self.process:
                self.process.kill()

    def add_to_buffer(self, log_entry):
        """Adds a log entry to the buffer and checks if flush is needed."""
        if not log_entry:
            return

        self.buffer.append(log_entry)
        
        if len(self.buffer) >= self.buffer_size:
            self.flush_buffer()

    def flush_buffer(self):
        """Outputs the buffered logs and clears the buffer."""
        if not self.buffer:
            return

        print(f"--- Flushing {len(self.buffer)} logs ---")
        for log in self.buffer:
            # We can parse json here if we want to pretty print or filter,
            # but for now we just dump the raw line as requested/implied.
            # Use json.loads(log) if we need to process the object.
            print(log) 
        print("----------------------------")
        
        self.buffer.clear()

if __name__ == "__main__":
    # Default buffer size is 10, can be changed here or via args if expanded
    shipper = LogShipper(buffer_size=10)
    shipper.start()
