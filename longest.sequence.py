# Longest Common Subsequence using Dynamic Programming

def lcs(seq1, seq2):
    m = len(seq1)
    n = len(seq2)

    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1

            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1]
                )

    # Reconstruct the LCS
    i = m
    j = n
    result = []

    while i > 0 and j > 0:

        if seq1[i - 1] == seq2[j - 1]:
            result.append(seq1[i - 1])
            i -= 1
            j -= 1

        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1

        else:
            j -= 1

    # Reverse because we built it backwards
    result.reverse()

    return result, dp[m][n]


# -------------------------------
# Main Program
# -------------------------------

seq1 = input("Enter first sequence: ")
seq2 = input("Enter second sequence: ")

subsequence, length = lcs(seq1, seq2)

print("\nLongest Common Subsequence:", "".join(subsequence))
print("Length of LCS:", length)