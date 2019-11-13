from dotenv import load_dotenv
import os

# # OR, the same with increased verbosity:
dotenvpath = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path= dotenvpath, verbose=True)
