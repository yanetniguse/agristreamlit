import scraper
import pdf_extractor
import database
import chatbot

def main():
    print("🚀 Running Smart Agriculture Chatbot System")

    print("\n📥 Downloading latest farming PDFs...")
    scraper.download_pdfs()

    print("\n📄 Extracting text from PDFs...")
    data = pdf_extractor.extract_text_from_pdfs()

    print("\n🗄️ Storing extracted data in database...")
    database.init_db()
    database.store_in_db(data)

    print("\n🤖 Starting the chatbot...")
    chatbot.chatbot()

    # Test with different farming queries
    test_queries = [
        "How can I grow maize?",
        "Best time to plant maize?",
        "How to control pests in maize?"
    ]

    for query in test_queries:
        response = database.search_farming_info(query)
        print(f"\n✅ Answer: {response}\n")

if __name__ == "__main__":
    main()
