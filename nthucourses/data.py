import os
import json
import itertools
import collections


weekdays = 'MTWRFS'
classsects = '1234n56789abc'
times = tuple(''.join(p) for p in itertools.product(weekdays, classsects))
times_as_table = tuple(tuple(w + s for s in classsects) for w in weekdays)


class CourseDataSet(collections.OrderedDict):
    def filter(self, function):
        return type(self)(filter(lambda grp: function(grp[1]), self.items()))


    def within_times(self, times):
        return self.filter(
            lambda ins: all(time in times for time in ins['time'])
        )


    def except_times(self, times):
        return self.filter(
            lambda ins: not any(time in times for time in ins['time'])
        )


    def within_departments(self, departments):
        return self.filter(
            lambda ins: ins['id'].startswith(departments)
        )


with open(os.path.join(os.path.dirname(__file__), 'courses.json')) as file:
    data = CourseDataSet(sorted(json.load(file).items(), key=lambda x: x[0]))
