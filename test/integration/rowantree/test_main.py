""" Content Service Entry Point """

import logging
import os
import unittest
from pathlib import Path

from rowantree.common.sdk import demand_env_var
from rowantree.service.sdk import RowanTreeService
from src.rowantree.server.common.personality import Personality


class TestMain(unittest.TestCase):
    def test_main(self):
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

        me: Personality = Personality(rowantree_service=RowanTreeService())

        logging.debug("Starting contemplation loop")
        while True:
            me.contemplate()


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(TestMain())
