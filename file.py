import datetime
import os
import pathlib


def create_outfile(list_seq):
    pathlib.Path("result").mkdir(parents=True, exist_ok=True)
    path_to_file = os.path.join("result", f"{datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.csv")
    try:
        with open(path_to_file, "w") as file:
            file.write("seq; column; new_column; value_searched\n")
            for s in list_seq:
                file.write(f"{s['seq']}; {s['column']}; {s['new_column']};  {s['value_searched']}\n")
            file.close()
            print(f"file {path_to_file} created")
    except Exception as e:
        print(f"except: {e}")
        raise