#!/usr/bin/env python3
import os.path, time

import yaml


from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

META_PATH = './case/common/'

def parser_yaml(filename):
    new_data = {}
    with open(filename) as f:
        data = yaml.load_all(f, Loader=yaml.FullLoader)
        for i in data:
            new_data.update(i)
        return new_data


def dump_to_yaml(data, file_name):
    with open(file_name, 'w') as yml:
        yaml.dump(data, yml, allow_unicode=True)

def replace(file_path, subst='# Ref From '):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if 'BLOCK_FROM' in line:
                    line = line.split('-')
                    new_file.write(line[0] + '# Ref:' + line[2])
                elif 'END_BLOCK' in line:
                    line = line.split('-')
                    new_file.write(line[0] + '# End:' + line[2])
                else:
                    new_file.write(line)

    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def parser_yaml_comments(file_name):
    replace(file_name)

def read_by_group_name(filename, group_name):
    s = parser_yaml(filename)
    s2 = s.get(group_name)
    return s2

def get_steps(item):
    steps = item.get("steps", [])
    return steps

def extends(steps):
    new_steps=[]
    ref_comment = {}
    end_comment = {}
    for step in steps:
        if 'ref' in step:
            ref_from, ref_obj = step.get("ref", {}).split('_')
            filename = META_PATH + ref_from + '.yaml'
            s2 = read_by_group_name(filename=filename, group_name =ref_obj)
            s3 = get_steps(s2)
            # add comment  here
            ref_comment.update({
                "BLOCK_FROM-{}".format(ref_from): ref_obj
            })
            new_steps.append(ref_comment)

            new_steps.extend(extends(s3))

            end_comment.update({
                "END_BLOCK-{}".format(ref_from): ref_obj
            })
            new_steps.append(end_comment)
            # end comment
            # init ...again
            ref_comment = {}
            end_comment = {}
        else:
            new_steps.append(step)
    return new_steps

def do_parser(filename):
    output_file = filename.replace("./case", './meta')
    if os.path.isfile(output_file) and \
        os.path.getctime(output_file) > os.path.getctime(filename):
        # Because nothing change, don't need to parser again !
        return "skip"

    all_group = parser_yaml(filename)
    new_all_group = {}
    for group_name in all_group:
        s = get_steps(all_group.get(group_name))
        new_steps = []
        new_steps = extends(s)
        all_group[group_name].update({
            "steps": new_steps
        })
    dump_to_yaml(all_group, output_file)
    parser_yaml_comments(output_file)
    return "done"

if __name__ == '__main__':
    f = META_PATH + 'data.yaml'
    o = META_PATH + 'test.yaml'
    do_parser("BAIDU", f, 'A', o)
