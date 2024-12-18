import time
import curses
from elasticsearch import Elasticsearch

USERNAME = "elastic"
PASSWORD = "changeme"

es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False  # Allow self-signed certificates
)
index_name = "character_index"
field_name = "Description"

def query_elasticsearch(partial_input):
    start_time = time.time()
    query_sensitive = {
        "query": {
            "match_phrase_prefix": {
                field_name: {
                    "query": partial_input
                }
            }
        }

    }
    response = es.search(index=index_name, body=query_sensitive)
    elapsed_time = time.time() - start_time
    return response, elapsed_time

def real_time_search(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr(0, 0, "Start typing your sentence: ")
    input_text = ""

    while True:
        key = stdscr.getch()

        if key == 27:  # Escape key to exit
            break
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Backspace
            input_text = input_text[:-1]
        elif key == 10:  # Enter key (not needed for real-time search)
            continue
        else:
            input_text += chr(key)

        stdscr.clear()
        stdscr.addstr(0, 0, f"Start typing your sentence: {input_text}")

        if input_text.strip():
            response, elapsed_time = query_elasticsearch(input_text.strip())
            stdscr.addstr(2, 0, f"Search time: {elapsed_time:.2f} seconds")

            results = response.get("hits", {}).get("hits", [])
            for idx, hit in enumerate(results[:10], start=3):
                stdscr.addstr(idx, 0, hit["_source"].get(field_name, "No Description"))

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(real_time_search)