def inplace_reverse(str):
    if str:
        # Convert the String to a list since strings are immutable in Python
        lst = list(str)

        # Initialize two pointers at the start and end of the list
        start = 0
        end = len(lst) - 1

        # Reverse the list in place
        while start < end:
            # XOR_SWAP equivalent in Python
            lst[start], lst[end] = lst[end], lst[start]

            # Move the pointers towards the center of the list
            start += 1
            end -= 1

        # Convert the list back into a string
        return ''.join(lst)
    return str
