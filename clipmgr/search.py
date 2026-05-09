def fuzzy_match(query, text, threshold=0.6):
    """Simple fuzzy matching based on longest common subsequence."""
    if not query or not text:
        return 0.0
    m, n = len(query), len(text)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if query[i-1].lower() == text[j-1].lower():
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    score = dp[m][n] / m
    return score

def search_history(history, query, top_k=10):
    """Search clipboard history with fuzzy matching."""
    scored = []
    for item in history:
        score = fuzzy_match(query, item['text'])
        if score > 0.4:
            scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored[:top_k]]
