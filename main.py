from database.db import (
    add_article,
    fetch_articles,
    fetch_all_articles,
    initialize_database,
    get_all_sessions,
    retrieve_memory,
    store_memory,
)
from utils.search import semantic_search
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the search tool
def search_tool_function(query):
    articles = fetch_articles(query)

    if not articles:
        return "No matching articles found."

    # Perform semantic search
    semantic_results = semantic_search(articles, query)

    # Display semantic search results
    response = "\nSemantic Search Results:\n"
    for result in semantic_results:
        response += f"- {result['page_content']} (Source: {result['source']})\n"

    return response

# Convert the search function into a tool
search_tool = Tool(
    name="Semantic Search",
    func=search_tool_function,
    description="Use this tool to search for articles related to specific topics or queries.",
)

# Initialize the ChatGPT model for the agent
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Create the agent with the tool
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
)

# Main program function
def start_agent():
    initialize_database()  # Ensure tables are created

    print("Welcome to the Semantic Search Application!")

    while True:
        print("\nOptions:")
        print("1. Add a new article")
        print("2. Search articles")
        print("3. Fetch all articles")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            # Add a new article
            page_content = input("Enter the article content: ")
            source = input("Enter the article source: ")
            add_article(page_content, source)
            print("Article added successfully.")

        elif choice == "2":
            # Search articles
            available_sessions = get_all_sessions()

            if available_sessions:
                print("\nAvailable sessions:")
                for i, session in enumerate(available_sessions, start=1):
                    print(f"{i}. {session}")

                session_choice = input(
                    "\nDo you want to continue a previous session or start a new one? (Type 'new' or the session number): "
                )
                if session_choice.lower() == "new":
                    session_id = f"session_{len(available_sessions) + 1}"  # New session ID
                    print("\nStarting a new session...")
                else:
                    try:
                        session_id = available_sessions[int(session_choice) - 1]
                        print(f"\nContinuing session: {session_id}")

                        # Retrieve memory for the current session
                        past_memory = retrieve_memory(session_id)
                        if past_memory:
                            print("\nPrevious Interactions:")
                            for item in past_memory:
                                print(f"User: {item['query']}")
                                print(f"Agent: {item['response']}")

                    except (IndexError, ValueError):
                        print("\nInvalid session choice. Starting a new session.")
                        session_id = f"session_{len(available_sessions) + 1}"
            else:
                session_id = "session_1"  # Default session for the first time
                print("\nNo previous sessions found. Starting a new session...")

            # Search articles using the agent
            user_query = input("\nEnter the article to Search: ")
            response = agent.invoke(user_query)

            # Store memory for the current session
            store_memory(session_id, user_query, response["output"])

            print(f"\n{response['output']}")

        elif choice == "3":
            # Fetch all articles
            articles = fetch_all_articles()

            if not articles:
                print("No articles found.")
                continue

            print("\nAll Articles:")
            for article in articles:
                print(f"- {article['page_content']} (Source: {article['source']})")

        elif choice == "4":
            print("\nThank you for using the Semantic Search Application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    start_agent()
