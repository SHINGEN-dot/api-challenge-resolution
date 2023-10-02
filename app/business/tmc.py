from tools import decorator
from tools import static
from tools import common
from scipy.optimize import linprog

@decorator.catch_exceptions
def extract_data(json_body):
    result = dict()
    original_load = json_body['load']
    target_load = json_body['load']
    if original_load > 0:
        fuels = json_body['fuels']
        c = []
        c_name = []
        bounds = []
        a = []
        wind = []
        for json_entry in json_body['powerplants']:
            if json_entry['type'] == static.PowerPlant.GAS:
                c_name.append(json_entry['name'])
                c.append(fuels[static.FuelPrice.GAS])
                bounds.append((json_entry['pmin'], json_entry['pmax']))
                a.append(json_entry['efficiency']*(-1))
            elif json_entry['type'] == static.PowerPlant.KEROSENE:
                c_name.append(json_entry['name'])
                c.append(fuels[static.FuelPrice.KEROSENE])
                bounds.append((json_entry['pmin'], json_entry['pmax']))
                a.append(json_entry['efficiency']*(-1))
            elif json_entry['type'] == static.PowerPlant.WIND:
                available_load = (fuels[static.WindPercentageAvailable.PERCENTAGE])/100 * json_entry['pmax']
                load = min(available_load, target_load)
                target_load -= load
                wind.append({'name': json_entry['name'], 'load': load})
        result = {'a': a, 'c': c, 'c_name': c_name, 'load': original_load, 'bounds': bounds, 'target_load': target_load, 'wind': wind}
    return result


@decorator.catch_exceptions
def calculate_max_load(parameters):
    result = 0
    for efficiency, bound in zip(parameters['a'], parameters['bounds']):
        result += common.round_float(float_number=(efficiency * bound[1] * (-1)), digit=1)
    for json_entry in parameters['wind']:
        result += json_entry['load']
    return result


@decorator.catch_exceptions
def found_optimal(parameters):
    result = dict()
    res = linprog(c=parameters['c'], A_ub=[parameters['a']], b_ub=[parameters['target_load'] * (-1)], bounds=parameters['bounds'], integrality=[2, 2, 2, 2])
    if res.success:
        result['success'] = True
        result['solution'] = []
        solution = list(res.x)
        for name, load in zip(parameters['c_name'], solution):
            result['solution'].append({'name': name, 'p': common.round_float(float_number=load, digit=1)})
        for json_entry in parameters['wind']:
            result['solution'].append({'name': json_entry['name'], 'p': common.round_float(float_number=json_entry['load'], digit=1)})
    else:
        result['success'] = False
        result['max_load'] = calculate_max_load(parameters=parameters)
    return result
