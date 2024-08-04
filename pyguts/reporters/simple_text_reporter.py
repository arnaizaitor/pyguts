import os
from pyguts.reporters.base_reporter import BaseReporter


class SimpleTextReporter(BaseReporter):
    """Generates a simple text report from the messages stored in the MessageStore."""

    output_file = "guts_report.txt"

    def write_report(self, messages_by_location):
        """Write the report to a file."""
        with open(os.path.join(self.output_dir, self.output_file), "w") as file:
            for location, messages in messages_by_location.items():
                file.write(
                    f"\n********************* {location} *********************\n"
                )
                if (
                    location.lower() == "general"
                ):  # Using .lower() for case-insensitive comparison
                    for message in messages:
                        file.write(
                            f"{message.msg_id}:{message.symbol} - {message.msg}\n"
                        )
                else:
                    for message in messages:
                        file.write(
                            f"{message.msg_id}:{message.symbol} - {message.line}:{message.column}: {message.msg}\n"
                        )

    def report(self):
        """Generate a simple text report from the messages stored in the MessageStore"""
        messages = self._message_store.get_messages()
        messages_by_location = {}
        for message in messages:
            if not message.module:
                messages_by_location.setdefault("General", []).append(message)
            else:
                messages_by_location.setdefault(f"{message.module}", []).append(message)

        self.write_report(messages_by_location)
