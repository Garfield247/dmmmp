from inspect import isfunction
from .chart_data import update_chart_data


def task2json(job):
    _d = {}
    _d = {i:str(getattr(job,i)) for i in dir(job) if not i.startswith("_") and not isfunction(getattr(job,i)) and not str(getattr(job,i)).startswith("<")}
    if hasattr(job,"trigger"):
        _d_sub = {i:str(getattr(job.trigger,i)) for i in dir(job.trigger) if not i.startswith("_") and not isfunction(getattr(job.trigger,i)) and not str(getattr(job.trigger,i)).startswith("<")}
        _d["trigger"] = _d_sub

    return _d
