def fuzzy_match(query, text):
    if not query or not text:
        return 0.0
    m, n = len(query), len(text)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if query[i-1].lower() == text[j-1].lower():
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n] / m

def search_history(history, query, top_k=10):
    scored = [(fuzzy_match(query, it['text']), it) for it in history]
    scored.sort(key=lambda x: -x[0])
    return [it for s, it in scored[:top_k] if s > 0.4]
