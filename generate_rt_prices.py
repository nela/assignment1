import random
import matplotlib.pyplot as plt


def peak_sides(pr_max: float, pr_min: float, pre: bool):
    arr = []
    count, prev, it = None, None, None
    if pre:
        count = random.randint(2,5)
        it = range(1, count)
        prev = pr_min
    else:
        count = random.randint(4,8)
        it = range(count, 0, -1)
        prev = pr_max

    step = (pr_max - pr_min) / count
    for i in it:
        if pre:
            up = prev + (step * random.uniform(1.1, 1.75))
            if up > pr_max:
                up = up - (step * random.uniform(0.5, 1.5))
                if up > pr_max:
                    up = pr_max

            p = random.uniform(prev, up)
        else:
            down = prev - (step * 1.5)
            if down < pr_min:
                down = down + (step * 0.75)
                if down < pr_min:
                    down = pr_min

            p = random.uniform(down, prev)
        arr.append(p)
        prev = p

    return arr


def daily_price(pr_min: float, pr_max: float):
    peak_morning = random.uniform((pr_max * 0.55), (pr_max * 0.9))
    peak_evening = random.uniform((pr_max * 0.65), pr_max)
    morning_pre = peak_sides(peak_morning, pr_min, True)
    morning_post = peak_sides(peak_morning,pr_min,  False)
    evening_pre = peak_sides(peak_evening,pr_min,  True)
    evening_post = peak_sides(peak_evening,pr_min,  False)

    prices = morning_pre
    prices.append(peak_morning)
    prices = prices + morning_post

    add_mpost = 9 - (len(morning_post) + len(evening_pre))
    if add_mpost > 0:
        post_morning_post = [random.uniform(pr_min,
            pr_min + (pr_min * random.uniform(0.45, .67))) for i in range(add_mpost)]
        print(post_morning_post)
        prices = prices + post_morning_post

    prices = prices + evening_pre
    prices.append(peak_evening)
    prices = prices + evening_post

    nightly_count = 24 - len(prices)
    if nightly_count > 0:
        nightly = [random.uniform(pr_min,
            pr_min + (pr_min * random.uniform(0.1, 0.25))) for i in range(nightly_count)]
        print(nightly)
        prices = nightly + prices

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
#
# plot_prices(prices)
