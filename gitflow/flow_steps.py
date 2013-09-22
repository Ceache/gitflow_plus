

"""
[[[[steps]]]]
                   condition= - the condition to check before transition, if
                                      not included, will default to condDefault
                   condCriticalFailNext= - the command to execute if condition fails, if
                                      not included, will default to transError
                   condNonCriticalFailNext - 
                   transition= - the command to be executed if the condition passes
                   transFailNext= - the command to execute if transition fails, if
                                      not included, will default to transError
"""

class Step(object):
	pass