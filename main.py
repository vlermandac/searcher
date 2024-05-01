import os
import sys
pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, './src'))

import config  # noqa: E402
import data_loading  # noqa: E402
from clients import Clients  # noqa: E402
from utils import Arguments  # noqa: E402


parse_args = Arguments() | "--process_data" | "--RAG" | "--KG"
selected_arg = parse_args()

cfg_vars = config.ConfigVariables(root='./')
clients = Clients(**cfg_vars.env_vars("ELASTIC_PASSWORD", "ELASTIC_URL",
                                      "CA_CERT", "OPENAI_API_KEY"))

if selected_arg == "--process_data":

    data_loading.run(clients, cfg_vars('processed-files', 'chunk-size',
                                       'overlap', 'openai-model', 'dims'))
    os.system(
     f"mv {cfg_vars('unprocessed-files')}/*.pdf {cfg_vars('processed-files')}"
    )

if selected_arg == "--RAG":
    print("RAG processing not implemented.")
    pass

if selected_arg == "--KG":
    print("KG processing not implemented.")
    pass
