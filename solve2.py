def replace_duplicate_chars(string, k):
    # 创建一个字典，用于存储每个字符最后一次出现的位置
    last_occurrence = {}
    result = ''
    
    for i, char in enumerate(string):
        # 如果字符在字典中，并且当前位置与上一次出现的位置的差值小于等于k
        if char in last_occurrence and i - last_occurrence[char] <= k:
            result += '-'
        else:
            result += char
        last_occurrence[char] = i
    
    return result

if __name__ == "__main__":
    string = input("Enter a string: ")
    k = int(input("Enter k: "))
    print(replace_duplicate_chars(string, k))