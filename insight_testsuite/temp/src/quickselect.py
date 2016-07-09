def nth(arr, n):
    pivot = arr[0]
    below = [x for x in arr if x < pivot]
    above = [x for x in arr if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if n < num_less:
        return nth(below, n)
    elif n >= num_lessoreq:
        return nth(above, n-num_lessoreq)
    else:
        return pivot

lst = [1,2,3,4,5,5,5,5]
n = len(lst)
if n % 2 == 1:
    med = float(nth(lst, n/2))
else:
    med = float(nth(lst, n/2-1) + float(nth(lst, n/2)))/2
print(med)

