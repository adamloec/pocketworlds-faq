import requests
import time

def test_chatbot_api():
    # API endpoints
    BASE_URL = "http://127.0.0.1:8080"
    INIT_URL = f"{BASE_URL}/api/initialize"
    CHAT_URL = f"{BASE_URL}/api/chat"
    FEEDBACK_URL = f"{BASE_URL}/api/feedback"

    # Initialize chatbot
    print("Initializing chatbot...")
    init_response = requests.post(INIT_URL)
    if init_response.status_code != 200:
        print(f"Failed to initialize chatbot: {init_response.status_code}")
        return
    
    print("Chatbot initialized successfully!")
    time.sleep(2)  # Give the system time to initialize

    # Test messages
    test_messages = [
        "Hello!",
        "How do I earn gold?",
        "What was the 2nd thing you said about earning gold?",
        "Thank you, goodbye!"
    ]

    # Process each message
    for message in test_messages:
        print(f"\nSending message: {message}")
        
        response = requests.post(
            CHAT_URL,
            json={"user_message": message}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Chatbot response: {result['system_response']}")
            
            if result['supporting_urls']:
                print("Supporting URLs:")
                for url in result['supporting_urls']:
                    print(f"- {url}")
            
            # Test feedback (for the first successful message only)
            if message == test_messages[1]:
                print("\nTesting feedback system...")
                feedback_response = requests.post(f"{FEEDBACK_URL}/liked")
                if feedback_response.status_code == 200:
                    print("Feedback recorded successfully!")
                else:
                    print(f"Failed to record feedback: {feedback_response.status_code}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        
        time.sleep(1)  # Pause between messages

if __name__ == "__main__":
    test_chatbot_api()