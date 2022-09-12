""" Content Service Entry Point """

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# load locally defined environmental variables
load_dotenv(dotenv_path="env/.env.offline")  # take environment variables from .env.

from rowantree.common.sdk import demand_env_var
from rowantree.service.sdk import RowanTreeService

from .common.global_personality import GlobalPersonality
from .common.global_storyteller import GlobalStoryTeller

if __name__ == "__main__":
    # Setup logging
    Path(demand_env_var(name="LOGS_DIR")).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
        filemode="w",
        filename=f"{demand_env_var(name='LOGS_DIR')}/{os.uname()[1]}.therowantree.content.service.log",
    )

    logging.debug("Starting server")

    rowantree_service: RowanTreeService = RowanTreeService()
    loremaster_service: GlobalStoryTeller = GlobalStoryTeller()
    personality: GlobalPersonality = GlobalPersonality(
        rowantree_service=rowantree_service, loremaster_service=loremaster_service
    )

    logging.debug("Starting contemplation loop")
    while True:
        personality.contemplate()
