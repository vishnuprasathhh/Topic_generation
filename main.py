from topic_extractor.extractor import TopicExtractor

if __name__ == "__main__":
    print("\n📄 SAMKHYA TOPIC GENERATOR")
    filepath = input("Enter the path to your DOCX file: ").strip()
    try:
        num_topics = int(input("How many topics do you want to extract (e.g., 10, 50, 100)? "))
    except ValueError:
        print(" Invalid input. Defaulting to 10 topics.")
        num_topics = 10

    extractor = TopicExtractor(filepath, num_topics)
    extractor.load_text()
    extractor.preprocess()
    extractor.vectorize()
    extractor.cluster_and_extract()

    print("\n🧠 Extracted Topics:")
    for i, topic in enumerate(extractor.get_topics(), 1):
        print(f"{i}) {topic}")
