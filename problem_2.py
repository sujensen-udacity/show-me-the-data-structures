import os


def find_files_rec(suffix, path):
    ret = []
    if not os.path.isdir(path):
        return "Error: path argument must be a directory!"
    path_list = os.listdir(path)
    for i in path_list:
        if os.path.isdir(path + "/" + i):
            new_path = path + "/" + i
            ret.extend(find_files_rec(suffix, new_path))
        else:
            if i.endswith(suffix):
                ret.append(path + "/" + i)
    return ret


def find_files(suffix, path):
    """
    Find all files beneath path with file name suffix.

    Note that a path may contain further subdirectories
    and those subdirectories may also contain further subdirectories.

    There are no limit to the depth of the subdirectories can be.

    Args:
      suffix(str): suffix if the file name to be found
      path(str): path of the file system

    Returns:
       a list of paths
    """
    return find_files_rec(suffix, path)


# Add your own test cases: include at least three test cases
# and two of them must include edge cases, such as null, empty or very large values

# Test Case 1
print("TEST 1")
test_1_files = find_files(".c", "testdir")
test_1_files.sort()
assert (test_1_files == ['testdir/subdir1/a.c', 'testdir/subdir3/subsubdir1/b.c', 'testdir/subdir5/a.c',
                         'testdir/t1.c'])

# Test Case 2
print("TEST 2")
test_2_files = find_files(".xml", "testdir")
assert (test_2_files == [])

# Test Case 3
print("TEST 3")
test_3_files = find_files(".h", "testdir/subdir5")
assert (test_3_files == ["testdir/subdir5/a.h"])

# Test Case 4
print("TEST 4")
test_4_files = find_files(".c", "foobarDoesNotExist")
assert (test_4_files == "Error: path argument must be a directory!")
