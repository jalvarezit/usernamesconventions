import json
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Generates a wordlist of usernames according to different conventions for the given name and surname")
    parser.add_argument("-i","--input-file",action="store", dest="input_file",default="sampledata.json", help="Input json file")
    parser.add_argument("-o","--output-file",action="store", dest="output_file",default="output", help="Output json file")
    parser.add_argument("-j","--output-json",action="store_true", dest="json", help="The output is generated as a json file instead of a wordlist")
    parser.add_argument("-s","--substitute-conventions",action="store", dest="conventions_subs", help="Specify a file with custom conventions and substitute them all", metavar="CONVENTIONS")    
    parser.add_argument("-a","--add-conventions",action="store", dest="conventions_add", help="Specify a file with custom conventions and add them to default ones", metavar="CONVENTIONS")
    parser.add_argument("-S","--set-separator",action="store",dest="separator",default="&", help="Specify a custom separator used for conventions")
    return parser

def get_conventions(separator):
    return [
        f"{separator}name_{separator}surname",
        f"{separator}name.{separator}surname",
        f"{separator}name",
        f"{separator}surname",
        f"{separator}n{separator}surname",
        f"{separator}name{separator}s",
        f"{separator}name{separator}surname",
        f"{separator}surname{separator}name",
        f"{separator}surname.{separator}name",
        f"{separator}surname_{separator}name",
        f"{separator}name-{separator}surname",
        f"{separator}n-{separator}surname",
        f"{separator}name-{separator}s",
        f"{separator}n.{separator}surname",
        f"{separator}name.{separator}s",
        f"{separator}n_{separator}surname",
        f"{separator}name_{separator}s"
    ]

def generate(user,conventions,separator):
    results = []
    for convention in conventions:
        result = convention
        result = result.replace(f"{separator}name",user["name"])
        result = result.replace(f"{separator}n",user["name"][0])
        result = result.replace(f"{separator}surname",user["surname"])
        result = result.replace(f"{separator}s",user["surname"][0])
        results += [result]
    return results

def read_conventions(filename):
    conventions = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            conventions += [line] 
    return conventions

def write_list(filedescr,datalist):
    for element in datalist:
        filedescr.write(f"{element}")

def main():
    parser = get_parser()
    args = parser.parse_args()
    if(args.conventions_subs):
        conventions = read_conventions(args.conventions_subs)
    elif args.conventions_add:
        conventions = read_conventions(args.conventions_add) + get_conventions(args.separator)
    with open(args.input_file) as input_file:
        data = json.load(input_file)
        with open(args.output_file, "w") as output_file:
            for user in data["users"]:
                content = generate(user,conventions,args.separator)
                if args.json:
                    user["usernames"] = content
                else:
                    write_list(output_file,content)
            if(args.json):
                json.dump(data, output_file)

main()