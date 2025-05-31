class OrderedSet:
    """
    A class that implements an ordered set, which maintains the order of elements
    while ensuring uniqueness.
    """

    def __init__(self):
        self._item_set = {}
        self._items = []

    def add(self, item):
        """Add an item to the ordered set."""
        if item not in self._item_set:
            self._item_set[item] = None
            self._items.append(item)

    def remove(self, item):
        """Remove an item from the ordered set."""
        if item in self._item_set:
            del self._item_set[item]
            self._items.remove(item)

    def __contains__(self, item):
        """Check if an item is in the ordered set."""
        return item in self._item_set

    def __iter__(self):
        """Return an iterator over the ordered set."""
        return iter(self._items)

    def __len__(self):
        """Return the number of items in the ordered set."""
        return len(self._item_set)

    def __repr__(self):
        """Return a string representation of the ordered set."""
        return "OrderedSet(" + repr(self._items) + ")"
