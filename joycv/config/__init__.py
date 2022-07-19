import tempfile
from pathlib import Path

temp_path= tempfile.gettempdir() +'/joycv_tmp/'
Path(temp_path).mkdir(parents=True, exist_ok=True)
