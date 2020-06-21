import yaml


def parser_yaml(filename):
    new_data = {}
    with open(filename) as f:
        data = yaml.load_all(f, Loader=yaml.FullLoader)
        for i in data:
            new_data.update(i)
        return new_data

def read_by_group_name(filename, group_name):
    s = parser_yaml(filename)
    s2 = s.get(group_name)
    return s2

def main():
    f = './examples/test.yaml'
    g = 'A'
    s = read_by_group_name(f, g)
    print(s)

if __name__ == '__main__':
    main()
