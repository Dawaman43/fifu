import random

class JokeService:
    """Service to provide random tech and programming jokes."""
    
    JOKES = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "There are 10 types of people in the world: those who understand binary, and those who don't.",
        "A SQL query walks into a bar, walks up to two tables, and asks, 'Can I join you?'",
        "Why was the JavaScript developer sad? Because they didn't know how to 'null' their feelings.",
        "Why did the developer go broke? Because they used up all their cache.",
        "I'd tell you a joke about UDP, but you might not get it.",
        "What is a programmer's favorite hangout place? The Foo Bar.",
        "Real programmers count from 0.",
        "Why do Java developers wear glasses? Because they can't C#.",
        "A programmer had a problem. He thought, 'I know, I'll use floating point numbers!' Now he has 1.0000000000000002 problems.",
        "Knock knock. Who's there? (long pause) Java.",
        "Programming is 10% writing code and 90% understanding why it's not working.",
        "Hardware is the part of a computer that you can kick; software is the part you can only curse at.",
        "To understand what recursion is, you must first understand what recursion is.",
        "An optimist says: 'The glass is half full.' A pessimist says: 'The glass is half empty.' A programmer says: 'The glass is twice as large as it needs to be.'",
        "My code doesn't always work, but when it does, I don't know why."
    ]

    @classmethod
    def get_random_joke(cls) -> str:
        """Get a random joke from the collection."""
        return random.choice(cls.JOKES)
