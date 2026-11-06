class _Slot:
    __slots__ = ("key", "value", "deleted")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.deleted = False


class HashTable:
    def __init__(self, capacity=101, max_load_factor=0.7):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._table = [None] * capacity
        self._size = 0
        self.last_probes = 0

    # ------------------------------------------------------------------ #
    # Hashing helpers
    # ------------------------------------------------------------------ #
    def _hash(self, key):
        if isinstance(key, int):
            return key % self._capacity
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def _probe(self, key):
        start = self._hash(key)
        for i in range(self._capacity):
            yield (start + i) % self._capacity

    # ------------------------------------------------------------------ #
    # Public operations
    # ------------------------------------------------------------------ #
    def put(self, key, value):
        if (self._size + 1) / self._capacity > self._max_load_factor:
            self._resize(self._capacity * 2 + 1)

        first_tombstone = None
        probes = 0
        for index in self._probe(key):
            probes += 1
            slot = self._table[index]
            if slot is None:
                target = first_tombstone if first_tombstone is not None else index
                self._table[target] = _Slot(key, value)
                self._size += 1
                self.last_probes = probes
                return target
            if slot.deleted:
                if first_tombstone is None:
                    first_tombstone = index
            elif slot.key == key:
                slot.value = value
                self.last_probes = probes
                return index

        if first_tombstone is not None:
            self._table[first_tombstone] = _Slot(key, value)
            self._size += 1
            self.last_probes = probes
            return first_tombstone
        raise OverflowError("hash table is full")

    def get(self, key):
        index = self._find_index(key)
        return None if index is None else self._table[index].value

    def slot_of(self, key):
        return self._find_index(key)

    def remove(self, key):
        index = self._find_index(key)
        if index is None:
            return False
        self._table[index].deleted = True
        self._table[index].value = None
        self._size -= 1
        return True

    def _find_index(self, key):
        probes = 0
        for index in self._probe(key):
            probes += 1
            slot = self._table[index]
            if slot is None:
                self.last_probes = probes
                return None
            if not slot.deleted and slot.key == key:
                self.last_probes = probes
                return index
        self.last_probes = probes
        return None

    def _resize(self, new_capacity):
        old = self._table
        self._capacity = new_capacity
        self._table = [None] * new_capacity
        self._size = 0
        for slot in old:
            if slot is not None and not slot.deleted:
                self.put(slot.key, slot.value)

    # ------------------------------------------------------------------ #
    # Utilities
    # ------------------------------------------------------------------ #
    def items(self):
        for i, slot in enumerate(self._table):
            if slot is not None and not slot.deleted:
                yield i, slot.key, slot.value

    @property
    def capacity(self):
        return self._capacity

    @property
    def load_factor(self):
        return self._size / self._capacity

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self._find_index(key) is not None
