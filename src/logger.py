"""XML logger for shell emulator events."""

import getpass
import os
import xml.etree.ElementTree as ET
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
            self.tree = ET.parse(path)
            self.root = self.tree.getroot()
        else:
            self.root = ET.Element("log")
            self.tree = ET.ElementTree(self.root)

    def log(self, command: str, args: list, error: str = "") -> None:
        """Append one event to the XML log."""
        event = ET.SubElement(self.root, "event")
        ET.SubElement(event, "timestamp").text = (
            datetime.now().isoformat()
        )
        ET.SubElement(event, "user").text = self.user
        ET.SubElement(event, "command").text = command
        ET.SubElement(event, "args").text = " ".join(args)
        ET.SubElement(event, "error").text = error
        self.tree.write(
            self.path, encoding="utf-8", xml_declaration=True
        )