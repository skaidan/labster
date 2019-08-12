from collections import OrderedDict

SEPARATOR = ','

class Restaurant():
    WEEKDAYS = [
        'Sun',
        'Mon',
        'Tue',
        'Wed',
        'Thu',
        'Fri',
        'Sat',
    ]
    


    def __init__(self, *opening_hours):

        # group day with the opening hours
        # [('Mon', '9-17'), ('Tue', '10-15'), ...]
        self.opening_hours = zip(
            self.WEEKDAYS,
            [opening_hour.to_string() for opening_hour in opening_hours]
        )

    def get_opening_hours(self):

        group_days = self._group_days_with_same_opened_hours()
        timetable = self._build_timetable(group_days)
        return timetable

    def _split_group_days_by_consecutive_days(self, seq, sep):
        group = []
        for el in seq:
            if el == sep:
                yield group
                group = []
            group.append(el)
        yield group
    
    def _group_days_with_same_opened_hours(self):
        group_days = OrderedDict()
        last_day = ''
        for opening_hour in self.opening_hours:
            if opening_hour[1] not in group_days.keys():
                group_days[opening_hour[1]] = (opening_hour[0],)
            else:
                if last_day not in group_days[opening_hour[1]]:
                    group_days[opening_hour[1]] = group_days[opening_hour[1]] + (SEPARATOR,)
                group_days[opening_hour[1]] = group_days[opening_hour[1]] + (opening_hour[0],)
            last_day = opening_hour[0]
        return group_days
    
    def _build_timetable(self, group_days):
        timetable = ''
        for opening_hour, group_day in group_days.iteritems():
            if len(group_day) > 1:
                if SEPARATOR in group_day:
                    splitted_group_day = self._split_group_days_by_consecutive_days(group_day, SEPARATOR)
                    for split in splitted_group_day:
                        if len(split) > 2:
                            timetable = timetable + split[1] + ' - ' + split[len(split) - 1] + ', '
                        else:
                            if SEPARATOR in split:
                                split.remove(',')
                            timetable = timetable + split[0] + ', '
                    timetable = timetable[:-2]
                    timetable = timetable + ': ' + opening_hour + ', '
                else:
                    timetable = timetable + group_day[0] + ' - ' + group_day[
                        len(group_day) - 1] + ': ' + opening_hour + ', '
            else:
                timetable = timetable + group_day[0] + ': ' + opening_hour + ', '

        if timetable:
            timetable = timetable[:-2]
        return timetable


class OpeningHour():

    def __init__(self, opening_hour, closing_hour):
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour

    def to_string(self):
        return "{}-{}".format(self.opening_hour, self.closing_hour)
