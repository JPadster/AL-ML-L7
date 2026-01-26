## Tools Overview
  
  ### Datetime
  
  The `datetime` package is effectively the default package for handling time data in python. It provides a useful introduction to the core concepts and is a go-to tooling for bespoke pythonic time based tasks.
  
  ```python
  from datetime import datetime
  
  time = datetime(year=2023, month=12, day=25)
  # Creates a datetime object for the specific date 25/12/2023.
  ```
  
  
  
  ### Numpy
  
  The `numpy` package provides the `datetime64` class for handling time. It is suitable for situations where you would already be using `numpy`. Usually when dealing with large arrays of data and where performance or scale are important. The `datatime64` class is more memory efficient than `datetime` but slightly less ergonomic in most situations. 
  
  ```python
  import numpy as np
  
  times = np.arange(\"2023-01-01\", \"2024-01-01\", dtype=\"datetime64[D]\")
  # Creates a array of numpy datetimes containing dates for all the days in the specified range.
  
  print(len(times))
  # Output: 365
  ```
  
  
  
  ### Pandas
  
  The `pandas` package provides an abundance of classes for handling time data, such as `DatetimeIndex` and `PeriodIndex`. It is likely to be suitable for when you wish to combine tabular based operations with time-based ones. It combines the efficiency of `numpy` with the functionality of `datetime`. However it's many classes can be a little confusing.
  
  ```python
  import pandas as pd
  
  index = pd.period_range(\"2020\", freq=\"M\", periods=12)
  data = pd.Series(range(12), index=index)
  # Creates a pandas Series of integers indexed by monthly periods in 2020.
  
  selection = data[\"2020-03-01\":\"2020-05-10\"]
  # Selects from the Series months intersecting the given period.
  
  print(len(selection))
  # How many months do you think were selected?
  ```
  
  
  
  ## The Pitfalls
  
  Ideally everyone would agree to measure time in some universally agreed *format*. If I agree to call a friend at some time using this agreed *format*, then there should be no confusion.
  
  For our time format we could use some units, such as seconds, counting from some universally agreed start time. Such as January 1st 1970.
  
  Nice idea! - this already exists and is called Unix time. It is one of many \"epoch\" based measures of time that count up or down from some fixed point in time.
  
  
  
  ### The Millenium Bug and Co
  
  The first issue is that we might run out of numbers using the Unix format. Using a signed 32-bit integer, Unix time will run out in 2038. So I can't arrange a call with my friend after this time. Not such a big deal, but what if my 32 bit computer operating system is also using Unix time?
  
  This kind of lack of consideration or forward-thinking led to the \"Millenium Bug\", where some computers were unable to represent dates after 2000 and some people though civilisation might collapse.
  
  
  
  ### Leap Years
  
  Time as we use it, is a bit of a mess. Most of us are dedicated to having a 60 second minute, a 60 minute hour, but then it gets less straight-forward as we deal with varying length months, leap seconds, leap days and daylight saving shifts.
  
  So if you tell a friend you're going to call them one million seconds Unix time, they are going to struggle to calculate when that is according to their diary and clock.
  
  
  
  ### Formats
  
  So instead of Unix time we use a less data efficient but more user friendly time format, counting years, months, days, hours, seconds and maybe smaller as required.
  
  ```python
  from datetime import datetime
  # NOTE! that we are importing *datetime* from the *datetime* project.
  
  call_me = datetime(year=2038, month=7, day=1, hour=10, minute=30, second=0)
  ```
  
  We still have to all agree some standard starting point and calendar. We will be conformist and use the [gregorian calendar](https://en.wikipedia.org/wiki/Gregorian_calendar) (12 months to a year, 31 days in January and so on). Then we base time of day on the sun passing over the Royal Observatory in Greenwich London.
  
  This is commonly referred to as [GMT (Greenwich Mean Time)](https://en.wikipedia.org/wiki/Greenwich_Mean_Time). We arrange our call with our friend again. `07/01/2039`.
  
  We are in the UK and they live in America, so there is some initial confusion about if we agreed the 7th of January or the 1st of July. Computers also find this confusing. We have to be very specific about how they should parse our times from strings or vice versa (format our times as strings).
  
  ```python
  from datetime import datetime
  
  # strptime for parsing strings into datatime
  a = datetime.strptime(\"07-01-38 10:30\", \"%m-%d-%y %H:%M\")
  b = datetime.strptime(\"1/7/38 10-30\", \"%d/%m/%y %H-%M\")
  
  assert a == b # datetimes a and b are the same
  
  # strftime for formatting a into a new string
  c = a.strftime(\"%Y-%m-%d %H:%M:%S\")
  
  print(c)
  # Output: 2038-07-01 10:30:00
  ```
  
  Carefully parsing these strings each time is annoying. So we ultimately all agree, in future, to format our time strings using `YYYY-MM-DD HH:MM:SS`, eg `2039-7-1 10:30`. This is considered normal based on the International Organization for Standardisation (ISO), but beware, is very commonly ignored in practice.
  
  ![UTC+0 timezones, aka GMT) ](/Module9/001.%20Time%20Objects%20in%20Python/img/Timezones2008_UTC+0_gray.png)
  
  A final hurdle remains. Our friend in the US doesn't wants to use GMT, he wants to use his local time. So then we start to worry about timezones. Ultimately we adopt the modern day standard of Coordinated Universal Time (UTC) and we get specific about which timezone we are in. We do this by adding a time zone difference relative to UTC \"zero\" (`2039-7-1 10:30+0`), which in the UK is still a difference of zero (ignoring daylight savings), which is often still called *GMT*.
  
  ```python
  from datetime import datetime
  from datetime import timezone
  from dateutil import tz
  
  # declare the timezone using datetime.timezone:
  datetime_london = datetime(year=2038, month=7, day=1, hour=10, tzinfo=timezone.utc)
  # or using dateutils:
  datetime_newyork = datetime(year=2038, month=7, day=1, hour=5, tzinfo=tz.gettz(\"America/New_York\"))
  
  assert datetime_london == datetime_newyork
  # They are equal because they have the same UTC.
  ```
  If necessary we can now shift our time based on timezones.
  
  ```python
  from datetime import datetime
  from datetime import timezone
  import dateutil.tz as tz
  
  # Initialise as utc+0.
  datetime_london = datetime(year=2038, month=7, day=1, hour=10, tzinfo=timezone.utc)
  # Change to utc-5.
  datetime_newyork.astimezone(tz.gettz(\"America/New_York\"))
  ```
  
  ![UTC-5 timezones, aka EST) ](/api/static/markdown_page/9787/img/Timezones2008_UTC-5_gray.png)
  
  We can also access attributes from our time data, such as day of the week, and use a variety of useful methods:
  
  ```python
  from datetime import datetime
  from datetime import timedelta
  
  call_me = datetime(year=2038, month=7, day=1, hour=10, minute=30)
  
  print(call_me.hour) # Output: 10
  
  day_index = call_me.weekday()
  # Monday is considered the \"first\" weekday, so...
  weekdays = [\"Monday\",\"Tuesday\",\"Wednesday\",\"Thursday\",\"Friday\",\"Saturday\",\"Sunday\"]
  
  print(weekdays[day_index])
  # Output: Thursday
  ```
  
  For other attributes and methods go consult the **latest** project documentation for [datetime](https://docs.python.org/3/library/datetime.html) as required.
  
  
  
  ### In Practice
  
  The `datetime` project refers to datetimes **without** timezone information as \"naive\" and **with** timezone information as \"aware\". In practice we can often get away with a \"naive\" representation of time unless joining data from many different places. In-fact in many cases we can parse and use some time series data without `datetime` or the other projects:
  
  ```python
  import pandas as pd
  
  data = pd.DataFrame(
      {
          \"id\": [0,1,2],
          \"time\": [360, 180, 240],
          \"observation\": [7, 3, 4]
      }
  )
  
  data = data.sort_values(by=\"time\")
  data[\"prev_observation\"] = data[\"observation\"].shift(1)
  data[\"delta\"] = data[\"observation\"] - data[\"prev_observation\"]
  print(data.delta.to_list())
  # Output: [nan, 1.0, 3.0]
  ```
  
  Parsing time data or creating time data is often the crux of our challenges with dealing with time. Some knowledge of the input data and some creativity is often required. Once we have parsed our data into a uniform format using our chosen project (`datetime`, `numpy` or `pandas`), we can then easily undertake common tasks using those projects.
  
  The above examples show instantiating, parsing and formatting time using the `datetime` project. The other projects have similar instantiation patterns and support conversion from `datetime` objects. However, there are sometimes differences. Whenever in doubt, consult the **latest** project documentation for [datetime](https://docs.python.org/3/library/datetime.html), [numpy](https://numpy.org/doc/stable/reference/arrays.datetime.html) or [pandas](https://pandas.pydata.org/docs/user_guide/timeseries.html).
  
  ```python
  from datetime import datetime
  import numpy as np
  import pandas as pd
  
  # datetime object
  a = datetime(year=2038, month=7, day=1, hour=10, minute=30)
  
  # numpy datetime64 objects
  b = np.datetime64(\"2038-07-01 10:30\")
  # numpy from datetime
  c = np.datetime64(a)
  
  assert a == b == c  # These are all equal
  
  # pandas timestamp objects
  d = pd.Timestamp(year=2038, month=7, day=1, hour=10, minute=30)
  # pandas from datetime
  e = pd.Timestamp(a)
  # pandas from numpy
  f = pd.Timestamp(b)
  
  assert d == e == f  # These are all equal
  ```
  
  For more information on \"aware\" vs \"naive\" datetime objects see the [documentation](https://docs.python.org/3/library/datetime.html).
  
  
  
  ## Arithmetic and Equalities
  
  The packages all support basic arithmetic using time difference (\"delta\") objects. The `datetime` project uses `datetime.timedelta`, numpy uses `numpy.timedelta64` and pandas `pandas.Timedelta`.
  
  ```python
  from datetime import datetime
  from datetime import timedelta
  
  year = datetime.now().year
  call_me = datetime(year=year, month=12, day=25)
  # NOTE! the often useful datetime.now()
  waiting_time = call_me - datetime.now()
  
  sleeps = int(waiting_time / timedelta(days=1))
  # How many sleeps until xmas?
  ```
  
  ```python
  # numpy example
  import numpy as np
  
  step = np.timedelta64(15, \"m\")
  a = np.datetime64(\"2038-07-01 10:30\")
  b = a + step
  c = b + (3 * step)
  
  assert c > a
  assert c - a == np.timedelta64(1, \"h\")
  ```
  
  ```python
  # pandas example
  import pandas as pd
  
  step = pd.Timedelta(15, \"m\")
  a = pd.Timestamp(\"2038-07-01 10:30\")
  b = a + step
  c = b + (3 * step)
  
  assert c > b > a
  assert c - a == pd.Timedelta(1, \"h\")
  ```
  
  Note that `pandas` (other than using Uppercase object names) is the same as numpy. This is generally the case as it uses `numpy.datetime64` and `numpy.timedelta64` in it's underlying design.
  
  
  
  ## Precision
  
  Sometimes precision matters. With `datetime` we are limited to microseconds:
  
  ```python
  from datetime import datetime
  
  time = datetime(year=2038, month=7, day=1, hour=10, minute=30, second=0, microsecond=0)
  ```
  
  For `numpy` and `pandas` we can [specify the unit](https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-units) you wish to work in, as small as attoseconds. But be warned, using inconsistent levels of precision can make arithmetic amd other operations more complex.
  
  ```python
  import numpy as np
  
  # Create a 1 year numpy timedelta64
  year = np.timedelta64(1, 'Y')
  
  try:
      days = np.timedelta64(year, 'D')
  except TypeError as e:
      print(e)
  # Cannot cast NumPy timedelta64 scalar from metadata [Y] to [D] according to the rule 'same_kind'
  ```
  
  
  ## Arrays of Times and Ranges
  
  Our data is typically going to arrive as an array or range of time. With `datetime` we have been building ranges of `datetime` objects using list comprehensions. With `numpy` we can more neatly use the `arange` operator to create ranges of times. Note that we can control the level of precision using the `dtype` argument.
  
  ```python
  import numpy as np
  
  # Create two ranges, one hourly the other every 15 minutes:
  hourly = np.arange(\"2038-07-01 00\", \"2038-07-10 00\", step=1, dtype=\"datetime64[h]\")
  quarter_hours = np.arange(\"2038-07-01 00\", \"2038-07-10 00\", step=15, dtype=\"datetime64[m]\")
  
  assert (hourly == quarter_hours[::4]).all()
  # This asserts that the arrays hourly and quarter_hours[::4] are equal.
  ```
  
  With `pandas` we have more flexibility with the types we can use to express arrays and ranges of times:
  
  | Class          | Notes                                        | Usage                                |
  |----------------|----------------------------------------------|--------------------------------------|
  | Timestamp      | Represents an instantaneous date and time.   | `ts = pd.Timestamp('today')`         |
  | Timedelta      | Represents an interval of elapsed time.      | `td = pd.Timedelta(60, \"m\")`         |
  | Period         | Represents a time period with start and end. | `per = pd.Period(\"2020-01-01\", 'D')` |
  | DatetimeIndex  | Immutable array of Timestamp objects.        | `pd.DatetimeIndex([ts, ts, ts])`     |
  | TimedeltaIndex | Immutable array of Timedelta objects.        | `pd.TimedeltaIndex([td, td, td])`    |
  | PeriodIndex    | Immutable array of Period objects.           | `pd.PeriodIndex([per, per, per])`    |
  
  We have already seen `Timestamp` which works like `datetime` or `datetime64` and `Timedelta` which works like `timedelta` or `timedelta64`. The new types are `Period` and the various Index classes.
  
  Periods are ranges of time. They represent a delta of time, but unlike `Timedelta` they represent the delta between two specific times. As such they have a start and end time.
  
  ```python
  import pandas as pd
  
  # we use H to specify a hourly period
  # we cover these frequencies later
  period = pd.Period(\"2020-03-11 13:00:00\", freq=\"H\")
  
  assert period.start_time != period.end_time
  # Periods have start times and end times that are (obviously) not equal.
  ```
  
  The Index versions of the above are arrays (or columns) of the above types. You can use indexes to speed up indexing operations or more generally be more explicit about the structure of your data.
  
  
  
  ### DatetimeIndex and Indexing
  
  We can explicitly create an index class or convert an existing column to the correct type (using `pd.to_datetime`) and then set this as the index.
  
  ```python
  import pandas as pd
  
  data = pd.DataFrame(
      {
          \"id\": [0,1,2,3],
          \"time\": [\"12/10/19\", \"3/4/05\", \"01/12/10\", \"3/4/05\"],
          \"observation\": [7, 3, 4, 2]
      }
  )
  # Convert time column to datetime (note that we have to declare we are using \"dayfirst\")
  data[\"time\"] = pd.to_datetime(data[\"time\"], dayfirst=True)
  # set as index
  data = data.set_index(\"time\")
  
  assert isinstance(data.index, pd.DatetimeIndex)
  
  # Example of indexing:
  print(data.loc[\"2005-04-03\"].observation.sum())
  # Output: 5
  ```
  
  
  
  ### Parsing Time with Pandas
  
  `pandas` will try to infer how to parse data into time, including when we index or slice our tables, but in some cases it will be best to be explicit. Either to deal with weird cases or to be sure that days are before months (\"european\" style) or vice versa (\"american\" style). `to_datetime` follows the same conventions as `datetime.strptime` using the `format` argument:
  
  ```python
  import pandas as pd
  
  str_dates = [\"14:46 on 16_03_19\", \"07:06 on 12_12_12\", \"01:10 on 01_10_01\"]
  print(pd.to_datetime(str_dates, format=\"%H:%M on %d_%m_%y\"))
  # Output: DatetimeIndex(['2019-03-16 14:46:00', '2012-12-12 07:06:00', '2001-10-01 01:10:00'], dtype='datetime64[ns]', freq=None)
  
  ```
  
  If you want to create some novel string based outputs you can use `strftime` as per with the `datetime` project. But, for the benefit of those who come after you, I suggest avoiding this:
  
  ```python
  import pandas as pd
  
  str_dates = [\"14:46 on 16_03_19\", \"07:06 on 12_12_12\", \"01:10 on 01_10_01\"]
  # Convert strings to datetimes:
  time = pd.to_datetime(str_dates, format=\"%H:%M on %d_%m_%y\")
  # Convert datetimes to new strings:
  time = time.map(lambda x: x.strftime(\"%Y_%B_%d[%H:%M]\"))
  
  # Bespoke/awkward string format:
  print(time[0])  # Output: 2019_March_16[14:46]
  ```
  
  In some cases we will want to create our own index range, you can use the `date_range` helper function to help:
  
  ```python
  import pandas as pd
  
  index = pd.date_range(\"2020\", \"2021\", freq=\"MS\")
  
  assert len(index) == 13  # Ranges are inclusive by default...
  
  index = pd.date_range(\"2020\", \"2021\", inclusive=\"left\", freq=\"MS\")
  
  assert len(index) == 12
  ```
  
  
  
  ### Frequency
  
  As above we often need an [explicitly defined frequency](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases), such as days, months or seconds:
  
  | Code | Definition             |
  |------|------------------------|
  | B    | business day frequency |
  | D    | calendar day frequency |
  | MS   | month start frequency  |
  | M    | month end frequency    |
  | Q    | quarter end frequency  |
  | H    | hourly frequency       |
  | T    | minutely frequency     |
  | S    | secondly frequency     |
  
  
  
  ### PeriodIndex and Indexing
  
  For when it is more useful to model our data points as having a duration, for example when they might partially overlap each other. We can create and use a `PeriodIndex` from our data:
  
  ```python
  import pandas as pd
  
  data = pd.DataFrame(
      {
          \"id\": [0,1,2,3],
          \"time\": [\"12/10/02\", \"3/4/05\", \"01/12/10\", \"3/4/12\"],
          \"observation\": [7, 3, 4, 0]
      }
  )
  # First convert time column to datetime:
  data[\"time\"] = pd.to_datetime(data[\"time\"], dayfirst=True)
  # Then to periods (days):
  data[\"time\"] = data[\"time\"].map(lambda x: x.to_period(\"D\"))
  # Set as index
  data = data.set_index(\"time\")
  
  assert isinstance(data.index, pd.PeriodIndex)  # True 
  
  # Index using a Period
  print(data.loc[\"2004\":\"2011\"])
  # How many/which rows do you think were selected?
  ```
  
  Or create a new index **range** using `period_range`:
  
  ```python
  import pandas as pd
  
  periods = pd.period_range(\"00:00\", freq=\"H\", periods=24)
  data = pd.Series(1, index=periods)
  
  assert isinstance(data.index, pd.PeriodIndex)
  
  # Select data from 12:30 to 14:05:
  lunch = data[\"12:30\":\"14:05\"]
  
  print(lunch.sum())
  # Given that data was a Series of 1s, what is the sum of the selection?
  ```
  
  In either case we have a powerful way of indexing our data using overlaps of periods of time.
  
  
  
  ## Final Thoughts
  
  This document has given you a primer to the common challenges when dealing with time in python. You have been shown (lots of) examples of how you can make use of the `datetime`, `numpy` and `pandas` projects. But a key take-away should **not** be that you need to learn all these project functions, classes and methods.
  
  Firstly, they share many common patterns. Secondly they are huge and we have barely scratched the surface of them. As always, do not be afraid to skim the documentations for [datetime](https://docs.python.org/3/library/datetime.html), [numpy](https://numpy.org/doc/stable/reference/arrays.datetime.html) or [pandas](https://pandas.pydata.org/docs/user_guide/timeseries.html) whenever necessary.
  
  Instead you should now have a feeling for when you need to use the projects:
  
  - small bespoke tasks -> `datetime`
  - big data tasks, limited complexity -> `numpy`
  - complex tabular data tasks -> `pandas`
  
  You should also have an appreciation of what is typically required to `parse` and `format` time data, and of the various operations such as arithmetic, equalities and indexing available.