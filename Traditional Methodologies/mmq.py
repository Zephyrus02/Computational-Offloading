import random
import time
import queue
from threading import Thread, Lock

# Constants
NUM_MOBILE_DEVICES = 5
SERVER_CAPACITY = 3
LATENCY = 1  # seconds
THRESHOLD_COMPLEXITY = 5  # Task complexity threshold for offloading
DATA_GENERATION_INTERVAL = 2  # Interval to generate new data (in seconds)

class Task:
    def __init__(self, task_id, complexity, resources_needed):
        self.task_id = task_id
        self.complexity = complexity
        self.resources_needed = resources_needed
        self.state = "Pending"

class Server:
    def __init__(self):
        self.available_resources = 10  # Total resources the server has
        self.current_tasks = queue.Queue(maxsize=SERVER_CAPACITY)
        self.lock = Lock()

    def process_task(self, task):
        """Simulate task processing."""
        time.sleep(LATENCY + task.complexity * 0.5)  # Simulate processing time
        task.state = "Completed"
        print(f"Task {task.task_id} processed on server.")

    def offload_task(self, task):
        with self.lock:
            if self.current_tasks.full():
                print(f"Server is busy, cannot offload Task {task.task_id}.")
                return False
            self.current_tasks.put(task)
            self.process_task(task)
            return True

class MobileDevice(Thread):
    def __init__(self, device_id, server):
        super().__init__()
        self.device_id = device_id
        self.server = server

    def run(self):
        while True:
            # Generate a task based on real-time data (simulated here)
            complexity = random.randint(1, 10)  # Random complexity
            resources_needed = random.randint(1, 3)  # Random resources needed
            task_id = int(time.time())  # Use current time as a unique task ID
            task = Task(task_id, complexity, resources_needed)
            
            # Decide whether to process locally or offload
            if task.complexity > THRESHOLD_COMPLEXITY and self.server.available_resources >= resources_needed:
                print(f"Device {self.device_id}: Offloading Task {task.task_id} to server.")
                success = self.server.offload_task(task)
                if not success:
                    print(f"Device {self.device_id}: Processing Task {task.task_id} locally due to server being busy.")
                    self.process_task_locally(task)
            else:
                print(f"Device {self.device_id}: Processing Task {task.task_id} locally.")
                self.process_task_locally(task)

            time.sleep(DATA_GENERATION_INTERVAL)  # Wait for the next data generation

    def process_task_locally(self, task):
        """Simulate local task processing."""
        time.sleep(LATENCY + task.complexity * 0.2)  # Simulate local processing time
        task.state = "Completed"
        print(f"Device {self.device_id}: Task {task.task_id} processed locally.")

def main():
    server = Server()
    devices = [MobileDevice(device_id=i, server=server) for i in range(NUM_MOBILE_DEVICES)]

    # Start all mobile devices
    for device in devices:
        device.start()

    # Let the devices run for a certain time and then terminate
    time.sleep(30)  # Run for 30 seconds for example
    print("Terminating all devices.")
    
    # Since the devices are in an infinite loop, we may want to handle termination gracefully
    for device in devices:
        device.join(timeout=1)

if __name__ == "__main__":
    main()