def main():
    listA = [1, 2, 3, 4, 5]
    print(listA.pop())
    print(listA.pop())
    print(listA.pop())
    print(listA.pop())
    print(listA.pop())
    if len(listA):
        print("Not Empty")
    else:
        print("Empty")
if __name__ == "__main__":
    main()