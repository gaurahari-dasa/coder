from dataclasses import dataclass


@dataclass(repr=False)
class OutputSpecs:
    name: str
    type: str
    title: str | None
    index: int
    searchable: bool
    sortable: bool
    sortOrdinal: str

    def __repr__(self):
        search_part = "?" if self.searchable else ""
        sort_part = (
            f"^{self.sortOrdinal if self.sortOrdinal else ''}" if self.sortable else ""
        )
        return f"#{self.index}({self.type or ''}; {self.title or ''}){search_part}{sort_part}"
