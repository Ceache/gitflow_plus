from flow_exceptions import WorkflowInitializationError

class State:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name

State.quiescent = State("Quiesecent")
State.collecting = State("Collecting")
State.selecting = State("Selecting")
State.unavailable = State("Unavailable")
State.wantMore = State("Want More?")
State.noChange = State("Use Exact Change Only")
State.makesChange = State("Machine makes change")

class HasChange:
    def __init__(self, name): self.name = name
    def __str__(self): return self.name

HasChange.yes = HasChange("Has change")
HasChange.no = HasChange("Cannot make change")

# Inputs to a state machine
class Input: pass


# Condition function object for state machine

class Condition:
    def condition(input):
        assert 0, "condition() not implemented"


class WorkflowStep:
    def __init__(self, stepName, stepCondition, stepTransition, stepSuccessNext, stepFailNext):
        self.name = stepName
        self.condition = stepCondition
        self.transition = stepTransition
        self.successNext = stepSuccessNext
        self.failNext = stepFailNext

    def __str__(self):
        return self.name


# A table-driven state machine

class StateMachine:
    def __init__(self, initialState, tranTable):
        self.state = initialState
        self.transitionTable = tranTable

#needs to be a recursive call
    def nextState(self, input):

        for step in self.transitionTable:
            if step.name == 'start':
                if step.stepCondition is not None:
                    step.stepCondition.condition(input)

                if step.stepTransition is not None:
                    step.stepTransition.transition(input)
                    self.nextState('next')
                return


"""
state
transitions (options)
sucesss state
fail state

{(CurrentState, InputA) : (ConditionA, TransitionA, NextA),
 (CurrentState, InputB) : (ConditionB, TransitionB, NextB),
 (CurrentState, InputC) : (ConditionC, TransitionC, NextC),
 ...
}
    def goforit(self):
        buildTable(Object[][][]{

         ::State.quiescent,
            :Money.class, null,showTotal, State.collecting,


         ::State.collecting,
            :Quit.quit, null,returnChange, State.quiescent,
            :Money.class, null,showTotal, State.collecting,
            :FirstDigit.class, null,showDigit, State.selecting,

         ::State.selecting,
            :Quit.quit, null,returnChange, State.quiescent,
            :SecondDigit.class, notEnough,clearSelection, State.collecting,
            :SecondDigit.class, itemNotAvailable,clearSelection, State.unavailable,
            :SecondDigit.class, itemAvailable,dispense, State.wantMore,

         ::State.unavailable,
            :Quit.quit, null,returnChange, State.quiescent,
            :FirstDigit.class, null,showDigit, State.selecting,

         ::State.wantMore,
            :Quit.quit, null,returnChange, State.quiescent,
            :FirstDigit.class, null,showDigit, State.selecting,






class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.endStates = []
        self.startState = None

    def add_state(self, name, handler, end_state=0):
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name

    def run(self, content):
        if self.startState in self.handlers:
            handler = self.handlers[self.startState]
        else:
            raise WorkflowInitializationError(".set_start() has to be called before .run()")
        if not self.endStates:
            raise WorkflowInitializationError("at least one state must be an end_state")

        oldState = self.startState
        while 1:
            (newState, content) = handler(content, oldState)
            if newState in self.endStates:
                print("reached ", newState, "which is an end state")
                break
            else:
                handler = self.handlers[newState]
            oldState = newState



                        from statemachine import StateMachine

positive_adjectives = ["great","super", "fun", "entertaining", "easy"]
negative_adjectives = ["boring", "difficult", "ugly", "bad"]

def transitions(txt, state):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if state == "Start":
        if word == "Python":
            newState = "Python_state"
        else:
            newState = "error_state"
        return (newState, txt)
    elif state == "Python_state":
        if word == "is":
            newState = "is_state"
        else:
            newState = "error_state"
        return (newState, txt)
    elif state == "is_state":
        if word == "not":
            newState = "not_state"
        elif word in positive_adjectives:
            newState = "pos_state"
        elif word in negative_adjectives:
            newState = "neg_state"
        else:
            newState = "error_state"
        return (newState, txt)
    elif state == "not_state":
        if word in positive_adjectives:
            newState = "neg_state"
        elif word in negative_adjectives:
            newState = "pos_state"
        else:
            newState = "error_state"
        return (newState, txt)


if __name__== "__main__":
    m = StateMachine()
    m.add_state("Start", transitions)
    m.add_state("Python_state", transitions)
    m.add_state("is_state", transitions)
    m.add_state("not_state", transitions)
    m.add_state("neg_state", None, end_state=1)
    m.add_state("pos_state", None, end_state=1)
    m.add_state("error_state", None, end_state=1)
    m.set_start("Start")
    m.run("Python is great")
    m.run("Python is difficult")
    m.run("Perl is ugly")
                """