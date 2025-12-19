from dataclasses import dataclass


@dataclass(repr=False)
class InputSpecs:
    type: str
    title: str | None
    options: str | None
    matchValue: str | None
    focus: bool
    required: bool

    def __repr__(self):
        focus = "@" if self.focus else ""
        required = "*" if self.required else ""
        return f"i({self.type}; {self.title or ''}; {self.options or ''}; {self.matchValue or ''}){focus}{required}"
