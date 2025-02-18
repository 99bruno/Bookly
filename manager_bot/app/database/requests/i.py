def solution(buckets):
    # Implement your solution here

    k = 0  # Bumber of balls
    len_bucket = 0

    for element in buckets:
        if element == "B":
            k += 1
        len_bucket += 1

    return len_bucket