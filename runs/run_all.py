from runs.run_optim import run_optim
from runs.run_ql import run_ql
from runs.run_rand import run_rand
from algorithms.agent import Generic_Agent

if __name__=='__main__':
    optim_ag = run_optim()
    ql_ag = run_ql()
    rand_ag = run_rand()
    Generic_Agent.plot_strategy(optim=optim_ag, qlearning=ql_ag, rand=rand_ag)