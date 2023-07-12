import configparser
import os

class Timer:
    _time_step = 0
    _config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

    _config = configparser.ConfigParser()
    _config.read(_config_file)

    _start_time = int(_config.get('Time', 'start_time'))
    _end_time = int(_config.get('Time', 'end_time'))
    _on_peak_period_start = int(_config.get('Time', 'on_peak_period_start'))
    _on_peak_period_end = int(_config.get('Time', 'on_peak_period_end'))
    _working_period_start = int(_config.get('Time', 'working_period_start'))
    _working_period_end = int(_config.get('Time', 'working_period_end'))
    _trip_period = float(_config.get('Time', 'trip_period'))
    _operation_duration = float(_config.get('Time', 'operation_duration'))
    _simulated_interval = int(_config.get('Time', 'simulated_interval'))

    @staticmethod
    def reset():
        Timer._time_step = Timer._start_time

    @staticmethod
    def get_time_step():
        return Timer._time_step

    @staticmethod
    def set_time_step(t):
        Timer._time_step = t

    @staticmethod
    def tick_time_step():
        Timer._time_step += Timer._simulated_interval

    @staticmethod
    def get_start_time():
        return Timer._start_time

    @staticmethod
    def get_end_time():
        return Timer._end_time

    @staticmethod
    def get_on_peak_period_start():
        return Timer._on_peak_period_start

    @staticmethod
    def get_on_peak_period_end():
        return Timer._on_peak_period_end

    @staticmethod
    def get_working_period_start():
        return Timer._working_period_start

    @staticmethod
    def get_working_period_end():
        return Timer._working_period_end

    @staticmethod
    def get_trip_period():
        return Timer._trip_period

    @staticmethod
    def get_operation_duration():
        return Timer._operation_duration

    @staticmethod
    def get_simulated_interval():
        return Timer._simulated_interval

    @staticmethod
    def get_units_in_one_hour():
        return 60//Timer._simulated_interval

    @staticmethod
    def is_peak_hours():
        if Timer._on_peak_period_start <= Timer._time_step <= Timer._on_peak_period_end:
            return True
        else:
            return False

    @staticmethod
    def is_working_hours():
        if Timer._working_period_start <= Timer._time_step <= Timer._working_period_end:
            return True
        else:
            return False

    @staticmethod
    def is_trip_started():
        if (Timer._working_period_start <= Timer._time_step <= Timer._working_period_end) and (Timer.get_time_step() % Timer._trip_period == 0):
            return True
        else:
            return False

    @staticmethod
    def is_end_time():
        return Timer._time_step > Timer._end_time


#For test
if __name__=='__main__':
    print("Simulated statrt time: ", Timer.get_start_time())
    print("Simulated end time: ", Timer.get_end_time())
    print("Peak hours started: ", Timer.get_on_peak_period_start())
    print("Peak hours ended: ", Timer.get_on_peak_period_end())
    print("Working hours started: ", Timer.get_working_period_start())
    print("Working hours ended: ", Timer.get_working_period_end())
    print("Trip period: ", Timer.get_trip_period())
    print("Operation duration: ", Timer.get_operation_duration())
    print("Simulated Interval: ", Timer.get_simulated_interval())
    print("Units in one hour: ", Timer.get_units_in_one_hour())
    print()

    Timer.tick_time_step()
    print("Time after tick: ", Timer.get_time_step())
    Timer.reset()
    print("Time after reset: ", Timer.get_time_step())
    print()

    print(f"Time {Timer.get_time_step()} is peak hour: {Timer.is_peak_hours()}")
    Timer.set_time_step(1000)
    print(f"Time {Timer.get_time_step()} is peak hour: {Timer.is_peak_hours()}")
    Timer.set_time_step(300)
    print(f"Time {Timer.get_time_step()} is working hour: {Timer.is_working_hours()}")
    print(f"Time {Timer.get_time_step()} is trip started: {Timer.is_trip_started()}")
    Timer.set_time_step(360)
    print(f"Time {Timer.get_time_step()} is working hour: {Timer.is_working_hours()}")
    print(f"Time {Timer.get_time_step()} is trip started: {Timer.is_trip_started()}")

    Timer.set_time_step(0)
    print(f"{Timer.get_time_step()} is end? {Timer.is_end_time()}")
    Timer.set_time_step(1439)
    print(f"{Timer.get_time_step()} is end? {Timer.is_end_time()}")
    Timer.set_time_step(1440)
    print(f"{Timer.get_time_step()} is end? {Timer.is_end_time()}")


