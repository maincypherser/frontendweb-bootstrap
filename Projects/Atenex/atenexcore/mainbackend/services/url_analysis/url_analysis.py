# mainbackend/services/url_analysis.py

def analyze_url(log_data, policy):
    """
    Analyze a URL based on the given log data and user's policy.
    This is a simple implementation that returns different results based on the policy.
    """
    # Example logic based on policy
    if policy.id == 1:
        return {"status": "blocked", "reason": "Policy ID 1 blocks this URL"}
    elif policy.id == 2:
        return {"status": "allowed", "reason": "Policy ID 2 allows this URL"}
    else:
        return {"status": "allowed", "reason": "Default policy allows this URL"}
