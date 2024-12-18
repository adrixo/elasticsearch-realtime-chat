import time
import curses
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch

USERNAME = "elastic"
PASSWORD = "changeme"

es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=(USERNAME, PASSWORD),
    verify_certs=False
)
index_name = "character_index"
field_name = "Description"

def query_elasticsearch_autocomplete(partial_input):
    start_time = time.time()
    query = {
        "query": {
            "match_phrase_prefix": {
                field_name: {
                    "query": partial_input
                }
            }
        }
    }
    response = es.search(index=index_name, body=query)
    elapsed_time = time.time() - start_time
    return response, elapsed_time

def real_time_autocomplete(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Color for autocomplete

    stdscr.clear()
    stdscr.addstr(0, 0, "Start typing your sentence: ")
    input_text = ""
    suggestion = ""

    while True:
        key = stdscr.getch()

        if key == 27:  # Escape key to exit
            break
        elif key == 127 or key == curses.KEY_BACKSPACE:  # Backspace
            input_text = input_text[:-1]
        else:
            input_text += chr(key)

        stdscr.clear()
        stdscr.addstr(0, 0, "Start typing your sentence: ")
        stdscr.addstr(1, 0, input_text)

        if input_text.strip():
            response, elapsed_time = query_elasticsearch_autocomplete(input_text.strip())
            results = response.get("hits", {}).get("hits", [])

            # Extract the first suggestion, if available
            if results:
                suggestion = results[0]["_source"].get(field_name, "").lower()
                if suggestion.lower().startswith(input_text.lower()):
                    autocomplete_part = suggestion[len(input_text):]
                else:
                    autocomplete_part = ""
            else:
                autocomplete_part = ""

            stdscr.addstr(2, 0, f"Search time: {elapsed_time:.2f} seconds")

            if autocomplete_part:
                stdscr.addstr(1, len(input_text), autocomplete_part, curses.color_pair(1))

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(real_time_autocomplete)
