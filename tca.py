import numpy as np
import matplotlib.pyplot as plt

# Functions phi1 and phi2
def phi1(x):
    return x / (1 + x)  # Example function for phi1

def phi2(x):
    return x / (1 + x)  # Example function for phi2

# Function to compute sigma and rho
def compute_sigma_rho(Spread, q, q0, Size, V, alpha, A1, B1, C1, A2, B2, C2):
    phi1_value = phi1(q / q0)
    phi2_value = phi2(q / q0)
    
    sigma = Spread * (A1 * (1 - phi1_value) + B1 * phi2_value * (Size / V)**alpha + C1)
    rho = Spread * (A2 * (1 - phi1_value) + B2 * phi2_value * (Size / V)**alpha + C2)
    
    return sigma, rho

# Function to compute the weighting factor h
def compute_h(sigma, rho):
    return sigma / (sigma + rho * np.sqrt(2 / np.pi))


# Custom trade cost distribution function
def trade_cost_distribution(x, mu, sigma, rho, h):
    if x < mu:
        return (2 * h / np.sqrt(2 * np.pi * sigma**2)) * np.exp(- (x - mu)**2 / (2 * sigma**2))
    else:
        return ((1 - h) / rho) * np.exp(- (x - mu) / rho)

if __name__ == "__main__":
    # Example parameters
    Spread = 0.03  # CBBT Bid/Ask spread
    q = 120  # Order size
    q0 = 100  # Scale parameter characterizing sensitivity of trade cost for odd lots
    Size = 100000  # Trade size in units
    V = 0.01 * 10000000  # 1% of the amount outstanding (10,000,000 in this example)
    alpha = 0.4  # Empirical value found to be sublinear, e.g., 0.4

    # Coefficients (example values)
    A1, A2 = 0.1, 0.1
    B1, B2 = 0.2, 0.2
    C1, C2 = 0.3, 0.3   
    
    # Compute sigma and rho
    sigma, rho = compute_sigma_rho(Spread, q, q0, Size, V, alpha, A1, B1, C1, A2, B2, C2)
    
    # Example mode (mu)
    mu = 0

    # Compute the weighting factor h
    h = compute_h(sigma, rho)

    # Generate sample data and plot
    x_values_left = np.linspace(mu - 3 * sigma, mu, 500)
    x_values_right = np.linspace(mu, mu + 3 * rho, 500)
    y_values_left = [trade_cost_distribution(x, mu, sigma, rho, h) for x in x_values_left]
    y_values_right = [trade_cost_distribution(x, mu, sigma, rho, h) for x in x_values_right]

    # Plot the distributions
    plt.plot(x_values_left, y_values_left, label='Half-Normal (Left Tail)')
    plt.plot(x_values_right, y_values_right, label='Half-Laplace (Right Tail)')
    plt.axvline(mu, color='gray', linestyle='--', label='Mean (μ)', alpha=0.3)
    plt.xlabel('Trade Cost')
    plt.ylabel('Probability Density')
    plt.title('Custom Trade Cost Distribution')
    plt.legend()

    # Display the results
    print(f"Computed sigma: {sigma}")
    print(f"Computed rho: {rho}")
    print(f"Computed h: {h}")

    plt.show()
