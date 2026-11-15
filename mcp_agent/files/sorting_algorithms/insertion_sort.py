def insertion_sort(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

if __name__ == "__main__":
    test_list = [12, 11, 13, 5, 6]
    print(f"Original list: {test_list}")
    sorted_list = insertion_sort(test_list)
    print(f"Sorted list (Insertion Sort): {sorted_list}")
