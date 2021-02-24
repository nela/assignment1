import random
import matplotlib.pyplot as plt


def peak_sides(price: float, pre: bool):
    arr = []
    count = range(1, 3) if pre else range(7, 0, -1)

    for i in count:
        rate_of_change = random.uniform(0.1, 0.2)
        # r = random.getrandbits(0)
        # if r == 0:
        #     rate_of_change = 0.10
        # elif r == 1:
        #     rate_of_change = 0.15
        # else:
        #     rate_of_change = 0.20

        p = random.uniform(price * rate_of_change * i,
                price * ((rate_of_change * i) + rate_of_change))

        arr.append(p)

    return arr


def daily_price(pr_min: float, pr_max: float):
    peak_morning = random.uniform((pr_max * 0.55), (pr_max * 0.9))
    peak_evening = random.uniform((pr_max * 0.65), pr_max)
    morning_pre = peak_sides(peak_morning, True)
    morning_post = peak_sides(peak_morning, False)
    evening_pre = peak_sides(peak_evening, True)
    evening_post = peak_sides(peak_evening, False)

    nightly_prices = [random.uniform(pr_min, morning_pre[0])] * 4

    prices = nightly_prices + morning_pre
    prices.append(peak_morning)
    prices = prices + morning_post + evening_pre
    prices.append(peak_evening)
    prices = prices + evening_post
    return prices


def plot_prices(prs: list):
    hours = []
    for i in range(24):
        hours.append(i)

    plt.step(hours, prices, where='mid')
    plt.xticks(hours)
    plt.show()

# price_max = 2.0
# price_min = 0.1
# prices = daily_price(price_max, price_min)
#
# plot_prices(prices)
