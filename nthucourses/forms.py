from django import forms

from nthucourses import models


class CourseFilterForm(forms.Form):
    OPERATIONS = (
        ('except', '搜尋選取時段以外的課'),
        ('within', '搜尋選取時段以內的課'),
    )
    operation = forms.ChoiceField(
        label='時段選項',
        choices=OPERATIONS,
        initial='except',
        widget=forms.RadioSelect,
    )
    time = forms.MultipleChoiceField(
        choices=zip(*[models.Time.objects.all()]*2),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    department = forms.ChoiceField(
        label='開課單位',
        choices=[
            (
                department.abbr,
                department.abbr + ' ' + department.name_zh
            )
            for department in models.Department.objects.all()
        ],
        # widget=forms.CheckboxSelectMultiple,
    )


    @property
    def timetable(self):
        return [
            [
                self['time'][x * len(models.Time.hours) + y]
                for x in range(len(models.Time.weekdays))
            ]
            for y in range(len(models.Time.hours))
        ]

    @property
    def selected_time(self):
        return self.cleaned_data.get('time', [])
