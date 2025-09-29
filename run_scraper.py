import sys
import net_empregos
import sapo

SCRAPERS = {
    "netempregos": net_empregos.run_scraper,
    "sapo": sapo.run_scraper,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_scraper.py [netempregos|sapo]")
        sys.exit(1)

    site = sys.argv[1].lower()
    if site not in SCRAPERS:
        print(f"Unknown scraper '{site}'. Options: {list(SCRAPERS.keys())}")
        sys.exit(1)

    SCRAPERS[site]()
