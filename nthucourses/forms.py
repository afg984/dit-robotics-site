from django import forms


from . import data


class CourseFilterForm(forms.Form):
    OPERATIONS = (
        ('except', '搜尋選取時段以外的課'),
        ('within', '搜尋選取時段以內的課'),
    )
    operation = forms.ChoiceField(
        choices=OPERATIONS,
        initial='except',
        widget=forms.RadioSelect,
    )
    times = forms.MultipleChoiceField(
        choices=zip(*[data.times]*2),
        widget=forms.CheckboxSelectMultiple,
    )
    department = forms.MultipleChoiceField(
        label='搜尋開課系所',
        choices=zip(*[data.departments]*2),
        widget=forms.CheckboxSelectMultiple,
    )


    @property
    def timetable(self):
        return [
            [
                self['times'][x * len(data.classsects) + y]
                for x in range(len(data.weekdays))
            ]
            for y in range(len(data.classsects))
        ]

    @property
    def selected_times(self):
        return self.cleaned_data.get('times', [])
