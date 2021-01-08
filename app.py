import json
import click
import os
from rule_sets import SurvivalRateAgeRuleSet
from rule_sets import BoradMemberRuleSet
from ui import UI

def parser(input_data):
    try:
        with open(input_data, 'r') as f:
            data = json.load(f)
        f.close()
        return data

    except Exception as err:
        # TODO catch error
        print(str(err))

def annotage(data, verbose):
    header = ["status", "annotation"]   
    if verbose:
        header.extend(['category', 'rule'])
    result = []
    result.append(SurvivalRateAgeRuleSet(data, verbose).annotage())
    result.extend(BoradMemberRuleSet(data, verbose).annotage())
    return (header, result)

@click.command()
@click.option('--input-data', '-i', help='data', prompt='input data .json')
@click.option('--verbose', '-v', help='-v for verbose mode', type=bool, is_flag=True)
def main(input_data, verbose):
    data = parser(input_data)
    (header, items) = annotage(data, verbose)
    UI.print_table(header, items)


if __name__=='__main__':
    main()