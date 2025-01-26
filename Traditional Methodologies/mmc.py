import math

class MMCQueue:
    def __init__(self, arrival_rate, service_rate, servers):
        """
        Initialize the M/M/c queue with arrival rate, service rate, and the number of servers.
        
        :param arrival_rate: Lambda (λ) - Average number of arrivals per time unit
        :param service_rate: Mu (μ) - Average number of services completed per time unit per server
        :param servers: c - Number of servers
        """
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.servers = servers

        if arrival_rate >= servers * service_rate:
            raise ValueError("System is unstable. Arrival rate must be less than c * service rate.")

    def utilization(self):
        """
        Calculate the server utilization (ρ).
        Utilization is the fraction of time each server is busy.
        
        :return: Utilization (ρ)
        """
        return self.arrival_rate / (self.servers * self.service_rate)

    def probability_zero_customers(self):
        """
        Calculate the probability that there are zero customers in the system (P0).
        
        :return: Probability of zero customers in the system (P0)
        """
        sum_terms = sum((self.arrival_rate / self.service_rate) ** n / math.factorial(n) for n in range(self.servers))
        last_term = ((self.arrival_rate / self.service_rate) ** self.servers) / (math.factorial(self.servers) * (1 - self.utilization()))
        return 1 / (sum_terms + last_term)

    def average_number_in_queue(self):
        """
        Calculate the average number of customers in the queue (Lq).
        
        :return: Average number in queue (Lq)
        """
        P0 = self.probability_zero_customers()
        Lq = (P0 * ((self.arrival_rate / self.service_rate) ** self.servers) * self.utilization()) / \
             (math.factorial(self.servers) * (1 - self.utilization()) ** 2)
        return Lq

    def average_time_in_queue(self):
        """
        Calculate the average time a customer spends waiting in the queue (Wq).
        
        :return: Average time in queue (Wq)
        """
        return self.average_number_in_queue() / self.arrival_rate

    def average_number_in_system(self):
        """
        Calculate the average number of customers in the system (L).
        
        :return: Average number in system (L)
        """
        return self.average_number_in_queue() + self.arrival_rate / self.service_rate

    def average_time_in_system(self):
        """
        Calculate the average time a customer spends in the system (W).
        
        :return: Average time in system (W)
        """
        return self.average_time_in_queue() + 1 / self.service_rate

# Taking user input
arrival_rate = float(input("Enter the arrival rate (λ): "))
service_rate = float(input("Enter the service rate (μ): "))
servers = int(input("Enter the number of servers (c): "))

# Create an instance of MMCQueue
try:
    queue = MMCQueue(arrival_rate, service_rate, servers)

    # Output results
    print(f"\nServer Utilization (ρ): {queue.utilization():.2f}")
    print(f"Probability of 0 customers (P0): {queue.probability_zero_customers():.2f}")
    print(f"Average Number in Queue (Lq): {queue.average_number_in_queue():.2f}")
    print(f"Average Time in Queue (Wq): {queue.average_time_in_queue():.2f} time units")
    print(f"Average Number in System (L): {queue.average_number_in_system():.2f}")
    print(f"Average Time in System (W): {queue.average_time_in_system():.2f} time units")
except ValueError as e:
    print(e)