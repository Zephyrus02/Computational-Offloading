import random
import time
import queue
from threading import Thread, Lock

# Constants
NUM_MOBILE_DEVICES = 5
NUM_SERVERS = 2
SERVER_CAPACITY = 3
LATENCY = 1  # seconds
THRESHOLD_COMPLEXITY = 5  # Task complexity threshold for offloading
DATA_GENERATION_INTERVAL = 2  # Interval to generate new data (in seconds)
SERVER_POWER_CONSUMPTION = 150  # Power consumption in watts
DEVICE_POWER_CONSUMPTION_WATTS = 10  # Power consumption in watts

class Task:
    def __init__(self, task_id, complexity, resources_needed):
        self.task_id = task_id
        self.complexity = complexity
        self.resources_needed = resources_needed
        self.state = "Pending"

class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.available_resources = 10  # Total resources the server has
        self.current_tasks = queue.Queue(maxsize=SERVER_CAPACITY)
        self.lock = Lock()
        self.energy_consumed = 0

    def process_task(self, task):
        """Simulate task processing."""
        processing_time = LATENCY + task.complexity * 0.5
        time.sleep(processing_time)
        self.energy_consumed += calculate_energy_consumed(SERVER_POWER_CONSUMPTION, processing_time)
        task.state = "Completed"
        print(f"Task {task.task_id} processed on server {self.server_id}. Energy consumed: {self.energy_consumed:.2f} watt-hours.")

    def offload_task(self, task):
        with self.lock:
            if self.current_tasks.full():
                print(f"Server {self.server_id} is busy, cannot offload Task {task.task_id}.")
                return False
            
            self.current_tasks.put(task)
            print(f"Task {task.task_id} added to server {self.server_id}'s queue.")

            # Only process if it's the only task in the queue (FIFO handling)
            if self.current_tasks.qsize() == 1:
                self.process_tasks_in_queue()
                
            return True

    def process_tasks_in_queue(self):
        while not self.current_tasks.empty():
            task = self.current_tasks.get()
            self.process_task(task)

def calculate_energy_consumed(power, processing_time):
    """Calculate energy consumed based on power (in watts) and processing time (in seconds)."""
    time_in_hours = processing_time / 3600
    return power * time_in_hours

class MobileDevice(Thread):
    def __init__(self, device_id, servers):
        super().__init__()
        self.device_id = device_id
        self.servers = servers
        self.energy_consumed = 0

    def run(self):
        global quit_flag
        while not quit_flag:
            complexity = random.randint(1, 10)
            resources_needed = random.randint(1, 3)
            task_id = int(time.time())
            task = Task(task_id, complexity, resources_needed)
            
            if task.complexity > THRESHOLD_COMPLEXITY:
                server = self.select_server(task)
                if server:
                    print(f"Device {self.device_id}: Offloading Task {task.task_id} to server {server.server_id}.")
                    success = server.offload_task(task)
                    if not success:
                        print(f"Device {self.device_id}: Processing Task {task.task_id} locally due to server being busy.")
                        self.process_task_locally(task)
                else:
                    print(f"Device {self.device_id}: Processing Task {task.task_id} locally (no available servers).")
                    self.process_task_locally(task)
            else:
                print(f"Device {self.device_id}: Processing Task {task.task_id} locally.")
                self.process_task_locally(task)

            time.sleep(DATA_GENERATION_INTERVAL)

    def select_server(self, task):
        available_servers = [server for server in self.servers if server.available_resources >= task.resources_needed]
        if available_servers:
            return available_servers[0]  # Select the first available server (FIFO principle)
        return None

    def process_task_locally(self, task):
        """Simulate local task processing."""
        processing_time = LATENCY + task.complexity * 0.2
        time.sleep(processing_time)
        self.energy_consumed += calculate_energy_consumed(DEVICE_POWER_CONSUMPTION_WATTS, processing_time)
        task.state = "Completed"
        print(f"Device {self.device_id}: Task {task.task_id} processed locally. Energy consumed: {self.energy_consumed:.2f} watt-hours.")

def main():
    global quit_flag
    quit_flag = False
    servers = [Server(server_id=i) for i in range(NUM_SERVERS)]
    devices = [MobileDevice(device_id=i, servers=servers) for i in range(NUM_MOBILE_DEVICES)]

    # Start all mobile devices
    for device in devices:
        device.start()

    # Let the devices run for a certain time and then terminate
    time.sleep(30)  # Run for 30 seconds for example
    quit_flag = True
    print("Terminating all devices.")

    # Since the devices are in an infinite loop, we may want to handle termination gracefully
    for device in devices:
        device.join(timeout=1)

if __name__ == "__main__":
    main()
