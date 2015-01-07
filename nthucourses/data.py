import os
import json
import itertools
import collections


weekdays = 'MTWRFS'
classsects = '1234n56789abc'
times = tuple(''.join(p) for p in itertools.product(weekdays, classsects))
times_as_table = tuple(tuple(w + s for s in classsects) for w in weekdays)


class CourseDataSet(collections.OrderedDict):
    def __init__(self, arg, department_index, **kw):
        super().__init__(arg, **kw)
        self.department_index = department_index


    def filter(self, function):
        return type(self)(
            filter(lambda grp: function(grp[1]), self.items()), self.department_index
        )


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
departments = collections.OrderedDict(sorted(data['departments'].items()))
courses = CourseDataSet(data['courses'], department_index=departments)
