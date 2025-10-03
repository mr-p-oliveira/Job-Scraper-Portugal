import sys
import net_empregos
import sapo
import os

SCRAPERS = {
    "netempregos": net_empregos.run_scraper,
    "sapo": sapo.run_scraper,
}

def load_keywords(file_path):
    if not file_path.lower().endswith(".txt"):
        print(f"❌ The file '{file_path}' is not a .txt file. Please provide text file.")
        sys.exit(1)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()]

    if not keywords:
        print(f" The file '{file_path}' is empty. Add at least one keyword.")
        sys.exit(1)
    return keywords

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_scraper.py [netempregos|sapo] [keywords.txt]")
        sys.exit(1)

    site = sys.argv[1].lower()
    if site not in SCRAPERS:
        print(f"Unknown scraper '{site}'. Options: {list(SCRAPERS.keys())}")
        sys.exit(1)

    if len(sys.argv) == 3:
        keywords = load_keywords(sys.argv[2])
        for kw in keywords:
            print(f"\n Running {site} scraper for: {kw}")
            SCRAPERS[site](search_term=kw)
    else:
        SCRAPERS[site]()
