def quickSelect(lst, k):
    if len(lst) != 0:
        pivot = lst[(len(lst)) // 2]
        smallerList = []
        for i in lst:
            if i < pivot:
                smallerList.append(i)
        largerList = []
        for i in lst:
            if i > pivot:
                largerList.append(i)
        count = len(lst) - len(smallerList) - len(largerList)
        m = len(smallerList)
        if k >= m and k < m + count:
            return pivot
            print(pivot)
        elif m > k:
            return quickSelect(smallerList, k)
        else:
            return quickSelect(largerList, k-m-count)

lst = [70, 120, 200, 5]
n = len(lst)
if n%2==1:
    print(quickSelect(lst, n/2))
else:
    print((quickSelect(lst, n/2-1) + quickSelect(lst, n/2))/2)

