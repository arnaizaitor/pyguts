import os
import json
from pyguts.reporters.base_reporter import BaseReporter
from pyguts.message.message import Message
from pyguts.interfaces import Confidence


class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            # Here, you use the asdict() if Message is a dataclass or manually define it.
            return (
                obj.__dict__
            )  # This assumes all attributes of Message are JSON serializable
        elif isinstance(obj, Confidence):
            # Serialize Confidence as a simple dictionary or just use its name.
            return {"name": obj.name, "description": obj.description}
        return json.JSONEncoder.default(self, obj)


class JsonReporter(BaseReporter):

    output_file = "guts_report.json"

    def report(self):
        messages = self._message_store.get_messages()
        messages_by_location = {}
        for message in messages:
            if not message.module:
                messages_by_location.setdefault("General", []).append(message)
            else:
                messages_by_location.setdefault(f"{message.module}", []).append(message)

        with open(os.path.join(self.output_dir, self.output_file), "w") as file:
            json.dump(messages_by_location, file, cls=MessageEncoder, indent=4)
