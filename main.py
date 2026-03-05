"""
Main entry point for Country Information AI Agent.
Implements an interactive loop for querying country information.
"""

from agent import CountryInformationAgent
from config import Config


def main():
    """Main function to run the Country Information AI Agent."""
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return
    
    print("Country Information AI Agent")
    print("===================================================")
    print("Ask me questions about countries!")
    print("Type 'quit' or 'exit' to stop the agent.")
    print("===================================================")
    print()
    
    agent = CountryInformationAgent()
    
    while True:
        try:
            user_input = input("Your question: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit"]:
                print("Thank you for using Country Information AI Agent. Goodbye!")
                break
            
            print("\nProcessing your query...")
            answer = agent.query(user_input)
            print(f"\nAnswer: {answer}\n")
            print("===================================================")
            print()
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")
            print("===================================================")
            print()


if __name__ == "__main__":
    main()
