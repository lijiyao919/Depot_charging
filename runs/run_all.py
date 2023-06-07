from runs.run_optim import run_optim
from runs.run_ql import run_ql
from algorithms.agent import Generic_Agent

if __name__=='__main__':
    optim_ag = run_optim()
    ql_qg = run_ql()
    Generic_Agent.plot_strategy(optim=optim_ag, qlearning=ql_qg)