def count_divisors(num):
    divisors = set()
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            divisors.add(i)
            divisors.add(num // i)
        if len(divisors) > 8:
            return 0
    return len(divisors)

count = 0
for i in range(32000, 43001):
    if count_divisors(i) == 8:
        count += 1

print(count)
