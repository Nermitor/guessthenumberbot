import os
from dataclasses import dataclass
import dotenv


@dataclass  # Позволяет не писать инициализатор
class TGBot:
    token: str


dotenv.load_dotenv()

config = TGBot(token=os.getenv('BOT_TOKEN'))