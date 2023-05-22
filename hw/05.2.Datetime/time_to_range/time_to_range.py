import datetime
import enum
import typing as tp  # noqa


class GranularityEnum(enum.Enum):
    """
    Enum for describing granularity
    """
    DAY = datetime.timedelta(days=1)
    TWELVE_HOURS = datetime.timedelta(hours=12)
    HOUR = datetime.timedelta(hours=1)
    THIRTY_MIN = datetime.timedelta(minutes=30)
    FIVE_MIN = datetime.timedelta(minutes=5)


def truncate_to_granularity(dt: datetime.datetime, gtd: GranularityEnum) -> datetime.datetime:
    """
    :param dt: datetime to truncate
    :param gtd: granularity
    :return: resulted datetime
    """
    if gtd == GranularityEnum.FIVE_MIN:
        dt -= datetime.timedelta(minutes=dt.minute % 5, seconds=dt.second, microseconds=dt.microsecond)
    elif gtd == GranularityEnum.THIRTY_MIN:
        dt -= datetime.timedelta(minutes=dt.minute % 30, seconds=dt.second, microseconds=dt.microsecond)
    elif gtd == GranularityEnum.HOUR:
        dt -= datetime.timedelta(minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
    elif gtd == GranularityEnum.TWELVE_HOURS:
        dt -= datetime.timedelta(hours=dt.hour % 12, minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
    else:
        dt -= datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second, microseconds=dt.microsecond)
    return dt


class DtRange:
    def __init__(
            self,
            before: int,
            after: int,
            shift: int,
            gtd: GranularityEnum
    ) -> None:
        """
        :param before: number of datetimes should take before `given datetime`
        :param after: number of datetimes should take after `given datetime`
        :param shift: shift of `given datetime`
        :param gtd: granularity
        """
        self._before = before
        self._after = after
        self._shift = shift
        self._gtd = gtd

    def __call__(self, dt: datetime.datetime) -> list[datetime.datetime]:
        """
        :param dt: given datetime
        :return: list of datetimes in range
        """
        dt = truncate_to_granularity(dt, self._gtd)
        if self._gtd == GranularityEnum.FIVE_MIN:
            dt2 = dt + datetime.timedelta(minutes=self._shift * 5, seconds=dt.second)
            if self._before == 0:
                dt1: tp.Any = []
            else:
                dt1 = dt2 - datetime.timedelta(minutes=self._before * 5, seconds=dt.second)
            if self._after == 0:
                dt3: tp.Any = []
            else:
                dt3 = dt2 + datetime.timedelta(minutes=self._after * 5, seconds=dt.second)
        elif self._gtd == GranularityEnum.THIRTY_MIN:
            dt2 = dt + datetime.timedelta(minutes=self._shift * 30, seconds=dt.second)
            if self._before == 0:
                dt1 = []
            else:
                dt1 = dt2 - datetime.timedelta(minutes=self._before * 30, seconds=dt.second)
            if self._after == 0:
                dt3 = []
            else:
                dt3 = dt2 + datetime.timedelta(minutes=self._after * 30, seconds=dt.second)
        elif self._gtd == GranularityEnum.HOUR:
            dt2 = dt + datetime.timedelta(hours=self._shift, minutes=0, seconds=dt.second)
            if self._before == 0:
                dt1 = []
            else:
                dt1 = dt2 - datetime.timedelta(hours=self._before, minutes=0, seconds=dt.second)
            if self._after == 0:
                dt3 = []
            else:
                dt3 = dt2 + datetime.timedelta(hours=self._after, minutes=0, seconds=dt.second)
        elif self._gtd == GranularityEnum.TWELVE_HOURS:
            dt2 = dt + datetime.timedelta(hours=self._shift * 12, minutes=0, seconds=dt.second)
            if self._before == 0:
                dt1 = []
            else:
                dt1 = dt2 - datetime.timedelta(hours=self._before * 12, minutes=0, seconds=dt.second)
            if self._after == 0:
                dt3 = []
            else:
                dt3 = dt2 + datetime.timedelta(hours=self._after * 12, minutes=0, seconds=dt.second)
        else:
            dt2 = dt + datetime.timedelta(days=self._shift, hours=0, minutes=0, seconds=dt.second)
            if self._before == 0:
                dt1 = []
            else:
                dt1 = dt2 - datetime.timedelta(days=self._before, hours=0, minutes=0, seconds=dt.second)
            if self._after == 0:
                dt3 = []
            else:
                dt3 = dt2 + datetime.timedelta(days=self._before, hours=0, minutes=0, seconds=dt.second)

        if not dt1:
            return [dt2, dt3]
        elif not dt3:
            return [dt1, dt2]
        else:
            d: tp.Any = []
            if self._gtd == GranularityEnum.HOUR:
                while dt1 < dt2:
                    d.append(dt1)
                    dt1 += datetime.timedelta(hours=1)
                d.append(dt2)
                dt2 += datetime.timedelta(hours=1)
                while dt2 <= dt3:
                    d.append(dt2)
                    dt2 += datetime.timedelta(hours=1)
                return d
            else:
                return [dt1, dt2, dt3]


def get_interval(
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        gtd: GranularityEnum
) -> list[datetime.datetime]:
    """
    :param start_time: start of interval
    :param end_time: end of interval
    :param gtd: granularity
    :return: list of datetimes according to granularity
    """
    st = truncate_to_granularity(start_time, gtd)
    if st == start_time:
        if gtd == GranularityEnum.HOUR:
            st -= datetime.timedelta(hours=1)
        elif gtd == GranularityEnum.TWELVE_HOURS:
            st -= datetime.timedelta(hours=12)
        elif gtd == GranularityEnum.DAY:
            st -= datetime.timedelta(days=1)
        elif gtd == GranularityEnum.THIRTY_MIN:
            st -= datetime.timedelta(minutes=30)
        else:
            st -= datetime.timedelta(minutes=5)
    en = truncate_to_granularity(end_time, gtd)
    d: tp.Any = []
    while st < en:
        if gtd == GranularityEnum.HOUR:
            st += datetime.timedelta(hours=1)
        elif gtd == GranularityEnum.TWELVE_HOURS:
            st += datetime.timedelta(hours=12)
        elif gtd == GranularityEnum.DAY:
            st += datetime.timedelta(days=1)
        elif gtd == GranularityEnum.THIRTY_MIN:
            st += datetime.timedelta(minutes=30)
        else:
            st += datetime.timedelta(minutes=5)
        d.append(st)
    return d
