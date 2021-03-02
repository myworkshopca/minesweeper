def addup(total, index, max):

    total = total + index
    index = index + 1
    if index > max:
        return total
    else:
        return addup(total, index, max)

print(addup(0, 1, 500))
