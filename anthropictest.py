import anthropic

client = anthropic.Anthropic()  # This initializes the client
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # Model specificaion (May need ot change if using pdf input)
    max_tokens=1000,  # Can use to truncate response
    system="You are a world-class poet. Respond only with short poems.",  # System prompt
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "Why is the ocean salty?"}],
        }
    ],
)
print(message.content)  # Output form model
