import datetime
import pytest


class LRUCache(object):

    def __init__(self, capacity):
        # Initialize class variables
        self.max = capacity      # the max size of the LRU cache
        self.cache = {}          # the LRU cache.  The value in the cache includes the timestamp of most recent use.
        self.times_list = []     # an ordered list of the timestamps of cache use (set and get)
        self.times = {}          # a mapping of the timestamp to the item (key) that was used
        self.min_time = None     # the smallest timestamp (the oldest cache use)

    def get(self, key):
        # Retrieve item from provided key. Return -1 if nonexistent. 
        if key in self.cache.keys():
            now = datetime.datetime.now()
            # old_time is the previous time this item was used
            old_time = self.cache[key]["time"]
            # update the most recent time for this item
            self.cache[key]["time"] = now
            # Add the new time to our use tracking
            self.times_list.append({"time": now, "key": key})
            self.times[now] = key
            # Remove old_time from the times dict
            self.times.pop(old_time)
            # If old_time was the minimum, it's not anymore.
            if self.min_time == old_time:
                self.times_list.pop(0)
                self.min_time = self.times_list[0]["time"]
            return self.cache[key]["value"]
        else:
            return -1

    def set(self, key, value):
        # If the item is already set, don't do anything. Only set if it's new to the LRU cache.
        if key not in self.cache.keys():
            # If the cache is at capacity remove the oldest item.
            if len(self.cache.keys()) == self.max:
                print("at capacity")
                # Who's at the min time
                min_item = self.times[self.min_time]
                print("  min_item is ", min_item)
                # remove that one from the cache
                self.cache.pop(min_item)
                old_time = self.times_list.pop(0)["time"]
                self.times.pop(old_time)
                # who's the new minimum
                self.min_time = self.times_list[0]["time"]
            # Set the item in the cache
            self.cache[key] = {}
            self.cache[key]["value"] = value
            now = datetime.datetime.now()
            self.cache[key]["time"] = now
            # Add the new timestamp to our use tracking
            self.times_list.append({"time": now, "key": key})
            self.times[now] = key
            if self.min_time is None:
                self.min_time = now

    def __str__(self):
        ret_str = ""
        ret_str += "cache: \n"
        for key, value in self.cache.items():
            ret_str += ("  " + str(key) + "," + str(value) + "\n")
        ret_str += "times_list: \n"
        ret_str += ("  " + str(self.times_list) + "\n")
        ret_str += "times: \n"
        for key, value in self.times.items():
            ret_str += ("  " + str(key) + "," + str(value) + "\n")
        ret_str += ("min_time: " + str(self.min_time) + "\n")
        return ret_str

    def get_current_queue(self):
        # PROBLEM here:  the values happen to come back in the correct order.  In what case would they not, though?
        ret = self.times.values()
        return list(ret)


our_cache = LRUCache(5)

our_cache.set(1, 1)
our_cache.set(2, 2)
our_cache.set(3, 3)
our_cache.set(4, 4)
assert (our_cache.get(1) == 1)  # returns 1
assert (our_cache.get(2) == 2)  # returns 2
assert (our_cache.get(9) == -1)  # returns -1 because 9 is not present in the cache
our_cache.set(5, 5)
our_cache.set(6, 6)
assert (our_cache.get(3) == -1)  # returns -1 because the cache reached its capacity and 3 was the LRU item

"""
Add your own test cases: include at least three test cases, and two of them must include edge cases, such as null, 
empty or very large values
"""


def fill_a_cache(capacity, use_ind, use_val):
    cache = LRUCache(capacity)
    for i in range(0, len(use_ind)):
        if use_ind[i] == "s":
            cache.set(use_val[i], use_val[i])
        elif use_ind[i] == "g":
            cache.get(use_val[i])
    return cache


# Test Case 1
print("TEST 1:")
test_1_cache = fill_a_cache(5, ["s", "s", "g", "s", "s", "s", "g"], [1, 2, 1, 3, 4, 5, 4])
assert (test_1_cache.get_current_queue() == [2, 1, 3, 5, 4])
print(test_1_cache)

# Test Case 2
print("TEST 2:")
test_2_cache = fill_a_cache(5, ["s", "s", "g", "g", "g"], [1, 2, 1, 1, 1])
assert (test_2_cache.get_current_queue() == [2, 1])
print(test_2_cache)
assert (test_2_cache.get(2) == 2)
# 1 is now the LRU
assert (test_2_cache.get_current_queue() == [1, 2])
print(test_2_cache)

# Test Case 3: just keep adding new things, while max cache size is 2
print("TEST 3:")
test_3_cache = fill_a_cache(2, ["s", "s", "s", "s", "s"], [1, 2, 3, 4, 5])
print(test_3_cache)
assert (test_3_cache.get(1) == -1)
assert (test_3_cache.get(2) == -1)
assert (test_3_cache.get(3) == -1)
print(test_3_cache)

# Test Case 4: try to get something before setting anything
print("TEST 4:")
test_4_cache = fill_a_cache(5, [], [])
print(test_4_cache)
assert (test_4_cache.get(100) == -1)

# Test Case 5: try to get something before setting anything
print("TEST 5:")
test_5_cache = fill_a_cache(5, ["g"], [100])
print(test_5_cache)
assert (test_5_cache.get(100) == -1)
assert (test_5_cache.get("abc") == -1)

# Test Case 6a: try to get a middle value (meaning not the first value we set)
print("TEST 6a:")
test_6a_cache = fill_a_cache(5, ["s", "s", "s", "g"], [1, 2, 3, 2])
assert (test_6a_cache.get_current_queue() == [1, 3, 2])
print(test_6a_cache)

# Test Case 6b: try to get a middle value, again
print("TEST 6b:")
test_6b_cache = fill_a_cache(5, ["s", "s", "s", "g", "g"], [1, 2, 3, 2, 1])
assert (test_6b_cache.get_current_queue() == [3, 2, 1])
print(test_6b_cache)

# Test Case 7: set and get immediately
print("TEST 7:")
test_7_cache = fill_a_cache(5, ["s", "g"], [1, 1])
assert (test_7_cache.get_current_queue() == [1])
print(test_7_cache)

# Test Case 8: set and get, then get again later
print("TEST 8:")
test_8_cache = fill_a_cache(5, ["s", "g", "s", "g"], [1, 1, 2, 1])
assert (test_8_cache.get_current_queue() == [2, 1])
print(test_8_cache)
assert (test_8_cache.get(1) == 1)
assert (test_8_cache.get(2) == 2)

