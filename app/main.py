from app.rag import LocalRAG


class CustomerSupportSystem:
    def __init__(self):
        self.rag = LocalRAG()

    def ask(self, query: str) -> str:
        return self.rag.ask(query)


if __name__ == "__main__":
    system = CustomerSupportSystem()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Assistant: Goodbye.")
            break

        response = system.ask(user_input)
        print("Assistant:", response)