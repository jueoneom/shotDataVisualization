
import sys    
data=[]
if __name__=="__main__":  
    num=list(map(int, sys.stdin.readline().split()))

    for i in range(num[0]):
        strs=list(sys.stdin.readline().split())
        if (strs[0]=="push") and (len(strs)>1):
            data.append(strs[1])
        elif strs[0]=="pop":
            if not data:
                print("-1")
            else:
                print(data.pop())
        elif strs[0]=="size":
            print(len(data))
        elif strs[0]=="empty":
            if not data: print("1")
            else: print("0")
        elif strs[0]=="top":
            if not data: print("-1")
            else: print(data[0])
 


                

            





 
