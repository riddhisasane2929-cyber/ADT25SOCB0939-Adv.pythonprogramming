# Fibonacci using Memoization and Tabulation


# -------------------------------
# 1. Memoization (Top-Down)
# -------------------------------

def fibonacci_memo(n, memo=None):

    if memo is None:
        memo = {}

    # Base cases
    if n == 0:
        return 0

    if n == 1:
        return 1

    # Check if already calculated
    if n in memo:
        return memo[n]

    # Calculate and store result
    memo[n] = (
        fibonacci_memo(n - 1, memo)
        + fibonacci_memo(n - 2, memo)
    )

    return memo[n]


# -------------------------------
# 2. Tabulation (Bottom-Up)
# -------------------------------

def fibonacci_tabulation(n):

    if n == 0:
        return 0

    if n == 1:
        return 1

    # DP table
    dp = [0] * (n + 1)

    dp[0] = 0
    dp[1] = 1

    # Fill the table
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


# -------------------------------
# Main Program
# -------------------------------

n = int(input("Enter the value of n: "))

print("\nMemoization:")
print("Fibonacci number =", fibonacci_memo(n))

print("\nTabulation:")
print("Fibonacci number =", fibonacci_tabulation(n))