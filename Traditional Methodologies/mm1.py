class MM1Queue:
    def __init__(self, arrival_rate, service_rate):
        """
        Initialize the M/M/1 queue with arrival and service rates.
        
        :param arrival_rate: Lambda (λ) - Average number of arrivals per time unit
        :param service_rate: Mu (μ) - Average number of services completed per time unit
        """
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate

        if arrival_rate >= service_rate:
            raise ValueError("System is unstable. Arrival rate must be less than service rate.")

    def utilization(self):
        """
        Calculate the server utilization (ρ).
        Utilization is the fraction of time the server is busy.
        
        :return: Utilization (ρ)
        """
        return self.arrival_rate / self.service_rate

    def average_number_in_system(self):
        """
        Calculate the average number of customers in the system (L).
        
        :return: Average number in system (L)
        """
        return self.utilization() / (1 - self.utilization())

    def average_time_in_system(self):
        """
        Calculate the average time a customer spends in the system (W).
        
        :return: Average time in system (W)
        """
        return 1 / (self.service_rate - self.arrival_rate)

    def average_number_in_queue(self):
        """
        Calculate the average number of customers in the queue (Lq).
        
        :return: Average number in queue (Lq)
        """
        return (self.arrival_rate ** 2) / (self.service_rate * (self.service_rate - self.arrival_rate))

    def average_time_in_queue(self):
        """
        Calculate the average time a customer spends waiting in the queue (Wq).
        
        :return: Average time in queue (Wq)
        """
        return self.arrival_rate / (self.service_rate * (self.service_rate - self.arrival_rate))

# Taking user input
arrival_rate = float(input("Enter the arrival rate (λ): "))
service_rate = float(input("Enter the service rate (μ): "))

# Create an instance of MM1Queue
try:
    queue = MM1Queue(arrival_rate, service_rate)

    # Output results
    print(f"\nServer Utilization (ρ): {queue.utilization():.2f}")
    print(f"Average Number in System (L): {queue.average_number_in_system():.2f}")
    print(f"Average Time in System (W): {queue.average_time_in_system():.2f} time units")
    print(f"Average Number in Queue (Lq): {queue.average_number_in_queue():.2f}")
    print(f"Average Time in Queue (Wq): {queue.average_time_in_queue():.2f} time units")
except ValueError as e:
    print(e)