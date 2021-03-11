import random
import matplotlib.pyplot as plt




def peak_sides(price: float, pr_min: float, pre: bool):
    arr = []
    count = range(1, 3) if pre else range(7, 0, -1)
    #count = random.randint(3,5) if pre else random.randint(5,9)
    #print(count)
    #it = range(1, count) if pre else range(count, 0, -1)
    prev_min = pr_min if pre else price
    diff = price - pr_min
    step = diff / len(count)
    for i in count:
        rate_of_change = random.uniform(0.1, 0.15)
        # r = random.getrandbits(0)
        # if r == 0:
        #     rate_of_change = 0.10
        # elif r == 1:
        #     rate_of_change = 0.15
        # else:
        #     rate_of_change = 0.20

        # tmp_rate = rate_of_change * i
        # print(f'tmp_rate {tmp_rate}')
        # old2= price * tmp_rate + rate_of_change

        # val1 = prev_min + prev_min * tmp_rate
        # val2 = price * tmp_rate + rate_of_change
        # diff = price - prev_min
        # new = prev_min + (prev_min * rate_of_change)
        # print(f'prev_min {prev_min} bew {new}')
        # p = random.uniform(prev_min, new)
        # print(p)
        # arr.append(p)
        # prev_min = p
        # a = prev_min
        # b = prev_min + step
        # if pre:
        #     p = random.uniform(prev_min, prev_min + step)
        # else:
        #     p = random.uniform(prev_min - step, prev_min -step)
        # arr.append(p)
        # prev_min = p
        p = random.uniform(price * rate_of_change * i,
                price * ((rate_of_change * i) + rate_of_change))
        arr.append(p)

#    if max(arr) > price * 0.9 || min(arr) < pr_min * 1.1:

    print(arr)
    return arr

def compress_sequence(l: list, lt, ht):
    avg = sum(l) / len(l)
    threshold_avg_low = lt + ((ht-lt)/4)
    thresh_avg_high = lt + ((ht-lt)*0.75)
    print(f'avg {avg} threshold_avg {threshold_avg_low} thresh_avg_high {thresh_avg_high}')
    new = []
    for i in l:
        print(i)
        print(i/avg)
        v = i/avg
        r1 = v * threshold_avg_low if i < avg else thresh_avg_high
        new.append(r1)

    print(new)

price_max = 1.0
price_min = 0.5

peak_morning = random.uniform((price_max * 0.55), (price_max * 0.9))
print(f'peak monring {peak_morning}')
morning_pre = peak_sides(peak_morning, price_min, False)

compress_sequence(morning_pre, price_min, peak_morning)

def daily_price(pr_min: float, pr_max: float):
    peak_morning = random.uniform((pr_max * 0.55), (pr_max * 0.9))
    print(peak_morning)
    peak_evening = random.uniform((pr_max * 0.65), pr_max)
    print(peak_evening)
    morning_pre = peak_sides(peak_morning, pr_min, True)
    morning_post = peak_sides(peak_morning,pr_min,  False)
    evening_pre = peak_sides(peak_evening,pr_min,  True)
    evening_post = peak_sides(peak_evening,pr_min,  False)

    nightly_prices = [random.uniform(pr_min, morning_pre[0])] * 4

    prices = nightly_prices + morning_pre
    prices.append(peak_morning)
    prices = prices + morning_post + evening_pre
    prices.append(peak_evening)
    prices = prices + evening_post
    return prices


def plot_prices(prices: list):
    hours = []
    for i in range(24):
        hours.append(i)

    plt.step(hours, prices, where='mid')
    plt.xticks(hours)
    plt.show()

# price_max = 1.0
# price_min = 0.5
# prices = daily_price(price_min, price_max)
# print(prices)
# print(len(prices))
# #
# plot_prices(prices)
# def chunks(l, n):
#     for i in xrange(0, len(l), n):
#         yield l[i:i+n]
#
# l = [1, 2, 3, 4, 5]
# print(chunks(l, 5))
# x = np.linspace(0.5, 1, 3)
# print(x)
#
# def resample(arr, newLength):
#     chunkSize = len(arr)/newLength
#     return [np.mean(chunk) for chunk in chunks(arr, chunkSize)]
#
# y = resample(x, 3)
# print(y)
