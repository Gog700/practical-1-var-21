"""XML logger for shell emulator events."""

import getpass
import os
import xml.etree.ElementTree as et
from datetime import datetime


class XMLLogger:
    """Writes command events to an XML log file."""

    def __init__(self, path: str) -> None:
        """Load existing log or create a new one."""
        self.path = path
        self.user = getpass.getuser()
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if os.path.exists(path):
            self.tree = et.parse(path)
            self.root = self.tree.getroot()
        else:
            self.root = et.Element("log")
            self.tree = et.ElementTree(self.root)

    def log(self, command: str, args: list, error: str = "") -> None:
        """Append one event to the XML log."""
        event = et.SubElement(self.root, "event")
        et.SubElement(event, "timestamp").text = (
            datetime.now().isoformat()
        )
        et.SubElement(event, "user").text = self.user
        et.SubElement(event, "command").text = command
        et.SubElement(event, "args").text = " ".join(args)
        et.SubElement(event, "error").text = error
        et.indent(self.tree, space="  ")
        self.tree.write(
            self.path, encoding="utf-8", xml_declaration=True
        )