# CreateNU Test Case

## Structure

```
├── app.py                                main file
├── requirements.txt
├── rule_sets                             ruleset module
│   ├── __init__.py
│   ├── board_member_rule_set.py
│   ├── rule_set_factory.py               ruleset factory
│   └── survival_rate_age_rule_set.py
└── ui.py                                 command-line user interface
```

## Ruleset

By considering the rules and the structure of the input and output data, I decided to start from creating a place to have my rules classified and easy to access.  
To have the two rulesets with the same encapsulated properties but in a dynamic way, designing an interface came to my mind. I started with factory design pattern and it was the best choice. 

In the ruleset module, Both Survival Rate/Age and Board Member rulsets are inheriting from the factory ruleset class and the `annotage` function is to produce the annotations from the rules one by one.

## UI
To print the data, I implemented a user interface that can handle the data shown to the user, the table, colors and styles.

## CLI

Install the requirements:

```sh
pip3 install -r requirements.txt
```

Run the program:

```sh
python app.py
```

### Arguments

- `--verbose`(`-v`) verbose/debug mode
- `--input-data`(`-i`) input file path
