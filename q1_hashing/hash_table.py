"""
hash_table.py
A generic Hash Table that uses Open Addressing with Linear Probing.

The table knows nothing about pharmacy products - any hashable key and any
value object can be stored, so it can be reused in other projects.
"""


class _Slot:
    """One slot (bucket) of the hash table.

    A slot holds exactly one key/value pair (open addressing stores every
    record directly inside the array, there are no linked lists).
    The `deleted` flag marks a "tombstone": a slot whose record was removed.
    A tombstone must not stop a search, otherwise records that were pushed
    further along the probe sequence would become unreachable.
    """
    __slots__ = ("key", "value", "deleted")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.deleted = False


class HashTable:
    """Hash table using open addressing + linear probing."""

    def __init__(self, capacity=101, max_load_factor=0.7):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._table = [None] * capacity   # None = empty, never used slot
        self._size = 0                    # number of live records
        self.last_probes = 0              # probes used by the last operation

    # ------------------------------------------------------------------ #
    # Hashing helpers
    # ------------------------------------------------------------------ #
    def _hash(self, key):
        """Map a key to its home slot index."""
        if isinstance(key, int):
            return key % self._capacity
        # Polynomial rolling hash for strings / other keys (deterministic,
        # unlike Python's randomised built-in str hash).
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def _probe(self, key):
        """Yield slot indices following the linear probing sequence."""
        start = self._hash(key)
        for i in range(self._capacity):
            yield (start + i) % self._capacity

    # ------------------------------------------------------------------ #
    # Public operations
    # ------------------------------------------------------------------ #
    def put(self, key, value):
        """Insert or update a record. Returns the slot index used."""
        if (self._size + 1) / self._capacity > self._max_load_factor:
            self._resize(self._capacity * 2 + 1)

        first_tombstone = None
        probes = 0
        for index in self._probe(key):
            probes += 1
            slot = self._table[index]
            if slot is None:                                   # empty slot
                target = first_tombstone if first_tombstone is not None else index
                self._table[target] = _Slot(key, value)
                self._size += 1
                self.last_probes = probes
                return target
            if slot.deleted:                                   # reuse later
                if first_tombstone is None:
                    first_tombstone = index
            elif slot.key == key:                              # update
                slot.value = value
                self.last_probes = probes
                return index

        if first_tombstone is not None:                        # table full of tombstones
            self._table[first_tombstone] = _Slot(key, value)
            self._size += 1
            self.last_probes = probes
            return first_tombstone
        raise OverflowError("hash table is full")

    def get(self, key):
        """Return the value stored for key, or None if absent."""
        index = self._find_index(key)
        return None if index is None else self._table[index].value

    def slot_of(self, key):
        """Return the slot index where key is stored, or None."""
        return self._find_index(key)

    def remove(self, key):
        """Delete a record (marks a tombstone). Returns True if removed."""
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
            if slot is None:              # truly empty -> key cannot be further on
                self.last_probes = probes
                return None
            if not slot.deleted and slot.key == key:
                self.last_probes = probes
                return index
        self.last_probes = probes
        return None

    def _resize(self, new_capacity):
        """Rehash every live record into a bigger table."""
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
        """Yield (slot_index, key, value) for every live record."""
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
