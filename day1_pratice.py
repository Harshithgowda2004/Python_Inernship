# Find the largest number in the list
numbers = [10, 45, 99, 3, 20, 60]

largest = numbers[0]

for i in range(len(numbers)):
    if numbers[i] > largest:
        largest = numbers[i]

print("Largest number is:", largest)


# Remove duplicates from a list without using sets
numbers = [10, 45, 99, 3, 20, 60, 45, 10, 99]

unique_numbers = []

for num in numbers:
    if num not in unique_numbers:
        unique_numbers.append(num)

print("Unique numbers:", unique_numbers)


# Move all zeros to the end of the list
numbers = [0, 1, 0, 3, 0, 12]

result = []

for num in numbers:
    if num != 0:
        result.append(num)

zeros_count = len(numbers) - len(result)

result.extend([0] * zeros_count)

print("After moving zeros:", result)
