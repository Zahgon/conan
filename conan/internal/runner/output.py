from conan.api.output import Color, ConanOutput


class RunnerOutput(ConanOutput):
    def __init__(self, runner_info: str):
        super().__init__()
        self.set_warnings_as_errors(True) # Make log errors blocker
        self._prefix = f"{runner_info} | "

    def _write_message(self, msg, fg=None, bg=None, newline=True):
        pass
