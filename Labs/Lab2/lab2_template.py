
if __name__ == "__main__":

    # Q1: Take the following list and multiply all items together
    lst1 = [1,2,4,8,16,32,64,128,256,512,1024]
    result1 = 1

    ### Add your code here
    from functools import reduce
    result1 = reduce(lambda m,n: m*n, lst1)
        
    ###

    print(f"Results of Q1:")
    print(f"result1 = {result1}")

    # Q2: Take the following list and all all the items together
    lst2 = [-1, 23, 483, 8573, -1384, -381569, 1652337, 718522177]
    result2 = 0

    ### Add your code here
    resutl2 = reduce(lambda x,y: x+y)
    ###

    print(f"Results of Q2:")
    print(f"result2 = {result2}")

    # Q3: Take the following list and and only add the items that are even
    lst3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21]
    result3 = 0

    ### Add your code here

    ###

    print(f"Results of Q3:")
    print(f"result3 = {result3}")