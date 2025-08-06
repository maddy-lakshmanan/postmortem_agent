incident_data = {
    "incident_id": "INC-2025-081",
    "title": "Service Outage on US-West API Cluster",
    "start_time": "2025-08-01T14:10:00Z",
    "end_time": "2025-08-01T14:42:00Z",
    "impact": "API requests to US-West cluster failed for 32 minutes, affecting ~22% of users. Mobile apps showed 503 errors.",
    "detection": "Detected via Datadog alert and user reports in Slack.",
    "resolution": "Rollback to stable deployment. Restarted kube pods and drained node with failing istio sidecar.",
    "root_cause": "Bad configuration pushed to production without staging verification. Istio config caused TLS negotiation failure.",
    "slack_summary": """
14:10 PDT - Alert triggered on API latency
14:15 PDT - Oncall joined, validated alert
14:18 PDT - Confirmed it's limited to US-West
14:24 PDT - Found Istio config change in last deploy
14:30 PDT - Rolled back and restarted pods
14:42 PDT - Services recovered
""",
    "owner": "Lakshmanan Maddy",
}