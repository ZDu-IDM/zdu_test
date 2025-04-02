# Simple python simulation running native slurm cluster. This example is to run python script(model3.py) in slurm cluster
# which doing simple add() caculation function with 2 sweep parameters as add(a,b)=a+b). The function result will be
# printed to stdout.txt file and output/result.txt file in each simulation folder.
# Path for simulation in cluster machine: /home/username/example/suite_id/experiment_id/simulation_id
import os
import sys
from pathlib import Path
from functools import partial
from typing import Any, Dict

from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities import Suite
from idmtools.entities.experiment import Experiment
from idmtools.entities.simulation import Simulation
from idmtools.entities.templated_simulation import TemplatedSimulations
from idmtools_models.python.json_python_task import JSONConfiguredPythonTask

import logging
from logging import getLogger, DEBUG

root = getLogger()
logger = getLogger(__name__)
user_logger = getLogger('user')


# from memory_profiler import profile


# Define an utility function that will update a single parameter at a
# # time on the model and add that param/value pair as a tag on our simulation.
def param_update(simulation: Simulation, param: str, value: Any) -> Dict[str, Any]:
    """
    This function is called during sweeping allowing us to pass the generated sweep values to our Task Configuration.

    We always receive a Simulation object. We know that simulations all have tasks and that for our particular set
    of simulations they will all include JSONConfiguredPythonTask. We configure the model with calls to set_parameter
    to update the config. In addition, we can return a dictionary of tags to add to the simulations so we return
    the output of the 'set_parameter' call since it returns the param/value pair we set

    Args:
        simulation: Simulation we are configuring
        param: Param string passed to use
        value: Value to set param to

    Returns:

    """
    return simulation.task.set_parameter(param, value)


def main(**kwargs):
    job_directory = 'DATA_FILE'
    platform = Platform('CONTAINER', job_directory=job_directory)


    # Define our base task. Normally, you want to do set any assets/configurations you want across the
    # all the different Simulations we are going to build for our experiment. Here we set c to 0 since we do not want to
    # sweep it
    # task = JSONConfiguredPythonTask(script_path=os.path.join(COMMON_INPUT_PATH, "python", "model3.py"),
    #                                 envelope="parameters", parameters=(dict(c=0)))
    task = JSONConfiguredPythonTask(script_path='simple.py',
                                    envelope="parameters", parameters=(dict(c=0)))
    task.python_path = "python3"

    # now let's use this task to create a TemplatedSimulation builder. This will build new simulations from sweep builders
    # we will define later. We can also use it to manipulate the base_task or the base_simulation
    ts = TemplatedSimulations(base_task=task)
    # We can define common metadata like tags across all the simulations using the base_simulation object
    ts.base_simulation.tags['tag1'] = 1

    # Since we have our templated simulation object now, let's define our sweeps
    # To do that we need to use a builder
    builder = SimulationBuilder()

    # Let's sweep the parameter 'a' for the values 0-2
    builder.add_sweep_definition(partial(param_update, param="a"), range(3))  # 3

    # Let's sweep the parameter 'b' for the values 0-4
    builder.add_sweep_definition(partial(param_update, param="b"), range(5))  # 5
    ts.add_builder(builder)

    # Now we can create our Experiment using our template builder
    # experiment = Experiment.from_template(ts, name="python example")
    experiment = Experiment.from_template(ts, name="python: `test` (example)")
    # Add our own custom tag to experiment
    experiment.tags["tag1"] = 1

    # Create suite
    suite = Suite(name='Idm Suite')
    suite.update_tags({'name': 'suite_tag', 'idmtools': '123'})
    # Add experiment to the suite
    suite.add_experiment(experiment)

    # run_script_as_slurm = False
    # slurm = kwargs.pop('slurm', None)
    # if run_script_as_slurm and not slurm:
    #     kwargs['script'] = os.path.realpath(__file__)

    # experiment.run(platform=platform, wait_until_done=False, max_running_jobs=10,
    #           retries=1, dry_run=False, batch_size=50, max_workers=32, **kwargs)
    # exit()

    # print(kwargs)
    suite.run(platform=platform, wait_until_done=False, max_running_jobs=10,
              retries=1, dry_run=False, batch_size=50, max_workers=32, **kwargs)

    # sys.exit(0 if experiment.succeeded else -1)


if __name__ == "__main__":
    main()
    exit()

    