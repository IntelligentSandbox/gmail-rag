import time

timestamp = int(time.time())

# DISCLAIMER: This was generated using ChatGPT.
emails = [
    {
        "id": f"demo_{timestamp}_1",
        "sender": "sarah@company.com",
        "recipient": "me@company.com", 
        "subject": "Q4 Budget Review",
        "body": "Hi team, I've completed the Q4 budget analysis. We need to reduce marketing spend by 15% and increase R&D investment. The board meeting is scheduled for next Tuesday.",
        "date": "2024-11-15",
        "thread_id": f"thread_{timestamp}_1",
        "content": "Hi team, I've completed the Q4 budget analysis. We need to reduce marketing spend by 15% and increase R&D investment. The board meeting is scheduled for next Tuesday."
    },
    {
        "id": f"demo_{timestamp}_2", 
        "sender": "dev@company.com",
        "recipient": "me@company.com",
        "subject": "API Integration Progress",
        "body": "The API integration with Stripe is 80% complete. We've implemented payment processing and subscription management. Still need to work on webhook handling and error reporting.",
        "date": "2024-11-14",
        "thread_id": f"thread_{timestamp}_2", 
        "content": "The API integration with Stripe is 80% complete. We've implemented payment processing and subscription management. Still need to work on webhook handling and error reporting."
    },
    {
        "id": f"demo_{timestamp}_3",
        "sender": "marketing@company.com",
        "recipient": "team@company.com",
        "subject": "Campaign Launch Next Monday",
        "body": "Our winter campaign launches next Monday. All assets are ready and social media schedule is set. Expected reach: 500K users.",
        "date": "2024-11-13",
        "thread_id": f"thread_{timestamp}_3",
        "content": "Our winter campaign launches next Monday. All assets are ready and social media schedule is set. Expected reach: 500K users."
    }
]

questions = [
    "What did Sarah say about the Q4 budget?",
    "Show me emails discussing the API integration project", 
    "When did I last hear from the marketing team?",
    "Summarize all conversations about the product launch"
]