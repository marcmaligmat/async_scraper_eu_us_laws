from scrapers_shared.shared_settings import SharedSettings

class Settings(SharedSettings):
    page_size: int = 64
    output_file: str = "./output.jsonl"
    last_cursor_file: str = "./last_cursor.json"
