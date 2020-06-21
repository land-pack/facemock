#!/usr/bin/env python3

import yaml


from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

META_PATH = './'

def parser_yaml(filename):
    new_data = {}
    with open(filename) as f:
        data = yaml.load_all(f, Loader=yaml.FullLoader)
        for i in data:
            new_data.update(i)
        return new_data


# ref_comment = {
#     "BLOCK_FROM": "default"
# }
#
# end_comment = {
#     "END_BLOCK": "default"
# }

def extend_yaml(items=None):
    assert items is not None
    print('items -->', items)
    item = parser_yaml(file_name=file_name)
    for item in items:
        groups = item.get("groups", {})
        # print("groups -->", groups)
        steps = groups.get("steps", [])
        group_id = groups.get("id")
        new_steps = []
        for step in steps:
            print('~~~~~~~~ step -->', step)
            if 'ref' in step:
                file_name, Obj= step["ref"].split('_')
                # return extend_yaml(file_name)
                # print("ref from: ", file_name)
                # s = parser_yaml(file_name=file_name)
                ref_comment.update({
                    "BLOCK_FROM_{}".format(group_id): file_name
                })
                new_steps.append(ref_comment)
                # s = parser_yaml(file_name=file_name)
                new_steps.extend(extend_yaml(file_name))

                end_comment.update({
                    "END_BLOCK_{}".format(group_id): file_name
                })
                new_steps.append(end_comment)
            # else:
            #     # for i in s:
            #         # s2 = extend_yaml(i)
            #     ex_item = s2.get("groups", {})
            #     ex_steps = ex_item.get("steps", [])
            #     new_steps.extend(ex_steps)
            #     # end_comment.update({
            #     #     "END_BLOCK_{}".format(group_id): file_name
            #     # })
            #     # new_steps.append(end_comment)
            #     # del step['ref'] # remove it because it has been extended
            else:
                new_steps.append(step)

        groups.update({"steps": new_steps})
        print("groups-->", groups)
        return new_steps

def scan_ref(line, filename):
    if 'ref' in line:
        return scan_ref()




def dump_to_yaml(data, file_name):
    # yaml.dump(data, ff, allow_unicode=True)
    with open(file_name, 'w') as yml:
        yaml.dump(data, yml, allow_unicode=True)

def replace(file_path, subst='# Ref From '):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                print("line -->{}".format(repr(line)))
                if 'BLOCK_FROM' in line:
                    line = line.split('-')
                    new_file.write(line[0] + '# Ref:' + line[2])
                    # new_file.write(line.replace('- BLOCK_FROM', '# Ref:'))
                elif 'END_BLOCK' in line:
                    line = line.split('-')
                    new_file.write(line[0] + '# End:' + line[2])
                    # new_file.write(line.replace('- END_BLOCK', '# -- End -- '))
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
    # groups = item.get("groups", {})
    steps = item.get("steps", [])
    # group_id = groups.get("id")
    return steps

def extends(steps):
    new_steps=[]
    ref_comment = {}
    end_comment = {}
    for step in steps:
        print('~~~~~~~~ step -->', step)
        if 'ref' in step:
            ref_from, ref_obj = step.get("ref", {}).split('_')
            filename = META_PATH + ref_from + '.yaml'
            s2 = read_by_group_name(filename=filename, group_name =ref_obj)
            s3 = get_steps(s2)
            # add comment  here
            ref_comment.update({
                "BLOCK_FROM-{}".format(ref_from): ref_obj
            })
            print('~the ~~~~~~~ step -->', ref_comment)
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

if __name__ == '__main__':
    # s = parser_yaml(filename='data.yaml')
    # print(s)

    original = read_by_group_name(filename='data.yaml',group_name ='A')
    print(original)

    s = get_steps(original)
    print('the steps ', s)

    # extends(s)
    new_steps = []
    new_steps = extends(s)
    print('*' * 30)
    print(new_steps)
    # s2 = extend_yaml(s)
    # for i in s:
    # s2 = extend_yaml(file_name='data.yaml')
    # print(s)
    original.update({
        "steps": new_steps
    })

    ff = './test.yaml'
    dump_to_yaml(original, ff)

    parser_yaml_comments(ff)
