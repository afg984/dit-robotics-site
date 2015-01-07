import os
import json
import itertools
import collections


weekdays = 'MTWRFS'
classsects = '1234n56789abc'
times = tuple(''.join(p) for p in itertools.product(weekdays, classsects))
times_as_table = tuple(tuple(w + s for s in classsects) for w in weekdays)


class CourseDataSet(collections.OrderedDict):
    def __init__(self, dict_, department_index=None):
        super().__init__(dict_)
        if department_index is None:
            department_index = dict_.department_index
        self.department_index = department_index


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
        result = type(self)({}, self.department_index)
        for department in departments:
            for no in department['curriclum']:
                result[no] = self[no]
        return result


with open(os.path.join(os.path.dirname(__file__), 'courses.json')) as file:
    data = json.load(file)
departments = data['departments']
courses = CourseDataSet(data['courses'], department_index=departments)
