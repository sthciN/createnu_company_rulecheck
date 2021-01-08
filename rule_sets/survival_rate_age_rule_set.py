from datetime import datetime as dt, date
from copy import copy
from .rule_set_factory import RuleSetFactory



class SurvivalRateAgeRuleSet(RuleSetFactory):
    _max_lifetime = 10
    diff_days = None

    def __init__(self, data, verbose):
        super().__init__(data)
        self._verbose = verbose
        self._category = self.categories[0]
        self._annotation_list = [
            [self.status[0], 'Company is a young company that only has been operating {} month[s]', self._category, 'If company life_time<12 months THEN'],
            [self.status[0], 'Company is a young company that only has been operating {} years', self._category, 'If company life_time is between 1-2 year THEN'],
            [self.status[0], 'Company is a young company that only has been operating {} years', self._category, 'If company life_time is between 2-3 years THEN'],
            [self.status[0], 'Company is a young company that only has been operating {} years', self._category, 'If company life_time is between 3-4 years THEN'],
            [self.status[0], 'Company is a young company that only has been operating {} years', self._category, 'If company life_time is between 4-5 years THEN'],
            [self.status[1], 'Company has been operating for {} years; longevity is TBD', self._category, 'If company life_time is between 5-6 years THEN'],
            [self.status[1], 'Company has been operating for {} years; longevity is TBD', self._category, 'If company life_time is between 6-7 years THEN'],
            [self.status[1], 'Company has been operating for {} years; longevity is TBD', self._category, 'If company life_time is between 7-8 years THEN'],
            [self.status[2], 'Company has been operating for {} years, which shows longevity', self._category, 'If company life_time is between 8-9 years THEN'],
            [self.status[2], 'Company has been operating for {} years, which shows longevity', self._category, 'If company life_time is between 9-10 years THEN']
        ]

    def _rule_check(self, min, max):
        self.diff_days = (date.today() - date.fromisoformat(self.data['profile']['established_date'])).days
        return min * 365 <= self.diff_days < max * 365

    def _annotation_match(self, index):
        annotation_item = copy(self._annotation_list[index])
        annotation_item = annotation_item[:2] if not self._verbose else annotation_item
        if not index:
            # less than a year
            annotation_item[1] = annotation_item[1].format(str(int(self.diff_days/30)))
        else:
            annotation_item[1] = annotation_item[1].format(str(index))
        return annotation_item
    
    def annotage(self):
        for i in range(self._max_lifetime):
            if self._rule_check(i, i+1):
                annotation = self._annotation_match(i)
                return annotation
        return self.empty_annotation_info()
