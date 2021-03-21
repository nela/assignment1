from classes import ElAppliance, ElType

def get_optimal_hours_for_continuous(appliance: ElAppliance, hourly_prices):
    cost = []
    for h in range(appliance.timeMin, appliance.timeMax-appliance.duration):
        cost.append((sum(hourly_prices[h:(h+appliance.duration)]), h))

    sorted_cost = sorted(cost, key=lambda x: (x[0], x[1]))

    return sorted_cost[0]


def sort_appliances(appliances: list):
    shiftable_continuous = []
    shiftable_non_continuous = []
    non_shiftable = []
    for a in appliances:
        if a.elType == ElType.shiftable:
            shiftable_continuous.append(a)
        elif a.elType == ElType.shiftable_non_continuous:
            shiftable_non_continuous.append(a)
        elif a.elType == ElType.non_shiftable:
            non_shiftable.append(a)

    return shiftable_continuous, shiftable_non_continuous, non_shiftable


def updated_hours_continuous(appliances: list, hourly_prices):
    substitutions = []
    for a in appliances:
        optimal_hour = get_optimal_hours_for_continuous(a, hourly_prices)
        optimal_hour = optimal_hour[1]
        substitutions.append(ElAppliance(a.name, a.dailyUsageMin, a.dailyUsageMax,
            a.maxHourConsumption, a.duration, a.elType, optimal_hour, optimal_hour+a.duration, a.actual_consumption))

    return substitutions
