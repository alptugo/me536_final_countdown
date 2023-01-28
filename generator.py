import subprocess
import json





def JSON_maker(cell_type, cell_size, shell_thickness, name):
    '''Writes JSOM to a file, contains lattice_paraameters for ntopology'''
    Scalar_0=cell_size
    Inputs_JSON = {
        "inputs": [
            {
                "name": "Scalar_0",
                "type": "scalar",
                "values": Scalar_0,
                "units": "mm"
            },
            {
                "name": "cell_type",
                "type": "enum",
                "value": cell_type
            },
            {
                "name": "shell_thickness",
                "type": "scalar",
                "values": shell_thickness,
                "units": "mm"
            },
            {
                "name": "name",
                "type": "text",
                "value": name
            }

        ]
    }
    with open("input.json", 'w') as outfile:
        json.dump(Inputs_JSON, outfile, indent=4)



#nTopology CLI command
command = '"C:\\Program Files\\nTopology\\nTopology\\ntopcl.exe" -j .\\input.json .\\ntop_generator.ntop -v 2'


def myPopen(cmd):
    '''Simple function to run commands'''
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.DEVNULL)
    print(proc.stdout.read().decode())
    return proc.stdout.read().decode()

cell_size=3
shell_thickness=1
#Creates JSON file for different objects and lattice types, and runs nTopology command for each combination
for i in range(1,401):
    for cell_type in range(14):
        JSON_maker(cell_type, cell_size, shell_thickness, str(i))
        myPopen(command)
        print(f"I'm on {i} of 401")