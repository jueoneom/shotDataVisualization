# data[10] = [0]
# prev[10] = [-1]
# next[10] = [-1]
unused = 1
cur = 0


def insert(addr, dat):
    data[unused] = dat
    prev[unused] = addr
    next[unused] = next[addr]
    next[addr] = unused
    prev[addr] = unused
    unused += 1


def erase(addr):
    next[prev[addr]] = next[addr]
    if (next[addr] != -1):
        prev[next[addr]] = prev[addr]


if __name__ == "__main__":
    strs = input()
    arr=[]
    for i in strs:
        arr.append(i)
        cur=len(arr)-1

    num = input()
    for i in range(int(num)):
        order = input().split(" ")
        if order[0] == 'L':
            if cur>=0:
                cur = cur-1
        elif order[0]=='D':
            if cur < len(arr):
                cur=cur+1
        elif order[0]=='B' and cur != -1:
            del arr[cur]
            cur=cur-1
        elif oårder[0]=='P':
            arr.insert(cur+1, order[1])
            cur=cur+1

    for i in arr:
        print(i, end="")
        

                

            





 
