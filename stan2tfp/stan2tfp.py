# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import os
import pkg_resources
import sys
import tempfile


def gen_tfp_code(path_to_stan_code):
    plat = sys.platform
    if not os.path.exists(path_to_stan_code):
        raise FileNotFoundError(path_to_stan_code)
    call_stan2tfp_cmd = pkg_resources.resource_filename(
        __name__, "/bin/{}-stan2tfp.exe".format(plat)
    )
    stan2_tfp_input = path_to_stan_code
    cmd = [call_stan2tfp_cmd, stan2_tfp_input]
    proc = Popen(cmd, stdout=PIPE)
    tfp_code = proc.communicate()[0]
    return tfp_code


def save_code(tfp_code, fname):
    with open(fname, "w") as f:
        f.writelines(tfp_code.split("\n"))


def get_tfp_model_obj(tfp_code):
    exec_dict = {}
    exec(tfp_code, exec_dict)
    return exec_dict["model"]


def init_model_with_data(model_obj, data_dict):
    return model_obj(**data_dict)


def model_from_tfp_code(tfp_code, data_dict):
    tfp_model_obj = get_tfp_model_obj(tfp_code)
    model = init_model_with_data(tfp_model_obj, data_dict)
    return model


def model_from_path(path_to_stan_code, data_dict):
    tfp_code = gen_tfp_code(path_to_stan_code)
    model = model_from_tfp_code(tfp_code, data_dict)
    return model


def model_from_stan_code(stan_code, data_dict):
    fd, path = tempfile.mkstemp()
    with open(fd, "w") as f:
        f.write(stan_code)
    model = model_from_path(path, data_dict)
    os.unlink(path)
    return model


# """Main module."""
