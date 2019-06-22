import sys
import argparse

ap = argparse.ArgumentParser(description='Convert Hex Files')
ap.add_argument("--name", help="name of the user", type=str, required=True)
ap.add_argument("--second", type=str, required= True)

#args =  vars(ap.parse_args())
args = ap.parse_args()
print(args.name)

print(f"bla bla {args.name} second {args.second}")


