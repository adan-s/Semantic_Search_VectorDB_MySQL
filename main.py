from database.db import add_article, fetch_articles, fetch_all_articles
from utils.search import semantic_search
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
import os
import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Please enter your OpenAI API key: ")

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
        response += f"- {result.page_content}\n"

    return response

# Convert the search function into a tool
search_tool = Tool(
    name="Semantic Search",
    func=search_tool_function,
    description="Use this tool to search for articles related to specific topics or queries."
)

# Initialize the ChatGPT model for the agent
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Create the agent with the tool
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent_type="zero-shot-react-description",
)

# Main program function
def main():
    print("Welcome to the Semantic Search Application!")
    while True:
        print("\nOptions:")
        print("1. Add a new article")
        print("2. Search articles")
        print("3. Fetch all articles")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            # Add new article
            page_content = input("Enter the article content: ")
            source = input("Enter the article source: ")
            add_article(page_content, source)

        elif choice == "2":
            # Search articles using the agent and search tool
            query = input("Enter your search query: ")

            # Pass the query to the agent
            response = agent.invoke(query)
            print(f"\n{response['output']}")

        elif choice == "3":
            # Fetch all articles
            articles = fetch_all_articles()

            if not articles:
                print("No articles found.")
                continue

            print("\nAll Articles:")
            for article in articles:
                print(f"- {article[1]} (Source: {article[2]})")  # article[1] = page_content, article[2] = source

        elif choice == "4":
            print("\nThank you for using the search agent. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    main()
