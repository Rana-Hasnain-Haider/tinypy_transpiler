def sum_upto(n):
    sum = 0
    for i in range(1, n):
        sum = sum + i
    return sum
def main():
    num = None
    print("Enter a number:")
    num = int(input())
    result = sum_upto(num)
    print("Sum from 1 to", num, "is", result)
    return 0

if __name__ == "__main__":
    main()