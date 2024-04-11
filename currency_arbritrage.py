import requests
import math

def fetch_exchange_rates(api_key, base_currency):
    print(f"Fetching exchange rates for {base_currency}...")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if data['result'] == 'success':
        print("Exchange rates fetched successfully.")
        return data['conversion_rates']
    else:
        raise Exception("Failed to fetch exchange rates")

def calculate_profit(edges, path, exchange_rates):
    print("Calculating profit for the arbitrage path...")
    amount = 1  # Start with 1 unit of base currency
    for i in range(len(path)-1):
        from_currency = path[i]
        to_currency = path[i+1]
        # Adjust for direct use of exchange rates
        rate = exchange_rates[to_currency] / exchange_rates[from_currency] if from_currency != 'USD' else exchange_rates[to_currency]
        print(f"Converting {from_currency} to {to_currency} at rate {rate}")
        amount *= rate
    profit_percentage = (amount - 1) * 100
    return profit_percentage

def bellman_ford(currencies, edges, source, exchange_rates):
    print(f"Running Bellman-Ford algorithm from {source}...")
    distance = {currency: float('inf') for currency in currencies}
    predecessor = {currency: None for currency in currencies}
    distance[source] = 0

    for _ in range(len(currencies) - 1):
        for u, v, weight in edges:
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u

    for u, v, weight in edges:
        if distance[u] != float('inf') and distance[u] + weight < distance[v]:
            arbitrage_path = [v]
            while True:
                v = predecessor[v]
                if v not in arbitrage_path or len(arbitrage_path) > len(currencies):
                    arbitrage_path.append(v)
                else:
                    arbitrage_path.append(v)
                    arbitrage_path = arbitrage_path[arbitrage_path.index(v):]
                    break
            arbitrage_path.reverse()

            print(f"Arbitrage opportunity detected! Path: {' -> '.join(arbitrage_path)}")
            profit_percentage = calculate_profit(edges, arbitrage_path, exchange_rates)
            print(f"Profit percentage for the cycle: {profit_percentage:.2f}%")

            investment = 1000000
            profit = investment * (profit_percentage / 100)
            print(f"Return on a $1,000,000 investment: ${profit:.2f}")

            print("No minimum investment required due to absence of transaction fees.")
            return True

    return False

def main(api_key, base_currency):
    exchange_rates = fetch_exchange_rates(api_key, base_currency)

    # Use all currencies returned by the API
    currencies = list(exchange_rates.keys())
    edges = []

    for from_currency in currencies:
        for to_currency in currencies:
            if from_currency != to_currency:
                rate = exchange_rates[to_currency]
                # Construct edges with actual exchange rates
                edges.append((from_currency, to_currency, -math.log(rate)))

    print("Checking for arbitrage opportunities among all currencies...")
    for currency in currencies:
        if bellman_ford(currencies, edges, currency, exchange_rates):
            break
    else:
        print("No arbitrage opportunity found among all currencies.")

if __name__ == "__main__":
    api_key = 'your_api_key_here'
    base_currency = 'USD'
    main(api_key, base_currency)
