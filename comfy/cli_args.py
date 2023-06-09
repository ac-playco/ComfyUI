import argparse
import json
import os

# Create Temp Args
JSON_FILE_PATH = "temp/temp_args.json"

def check_and_create_directory():
    directory = os.path.dirname(JSON_FILE_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_args(arg_dict=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("--listen", type=str, default="127.0.0.1", metavar="IP", nargs="?", const="0.0.0.0", help="Specify the IP address to listen on (default: 127.0.0.1). If --listen is provided without an argument, it defaults to 0.0.0.0. (listens on all)")
    parser.add_argument("--port", type=int, default=8188, help="Set the listen port.")
    parser.add_argument("--enable-cors-header", type=str, default=None, metavar="ORIGIN", nargs="?", const="*", help="Enable CORS (Cross-Origin Resource Sharing) with optional origin or allow all with default '*'.")
    parser.add_argument("--extra-model-paths-config", type=str, default=None, metavar="PATH", nargs='+', action='append', help="Load one or more extra_model_paths.yaml files.")
    parser.add_argument("--output-directory", type=str, default=None, help="Set the ComfyUI output directory.")
    parser.add_argument("--auto-launch", action="store_true", help="Automatically launch ComfyUI in the default browser.")
    parser.add_argument("--cuda-device", type=int, default=None, metavar="DEVICE_ID", help="Set the id of the cuda device this instance will use.")
    parser.add_argument("--dont-upcast-attention", action="store_true", help="Disable upcasting of attention. Can boost speed but increase the chances of black images.")
    parser.add_argument("--force-fp32", action="store_true", help="Force fp32 (If this makes your GPU work better please report it).")
    parser.add_argument("--directml", type=int, nargs="?", metavar="DIRECTML_DEVICE", const=-1, help="Use torch-directml.")

    attn_group = parser.add_mutually_exclusive_group()
    attn_group.add_argument("--use-split-cross-attention", action="store_true", help="Use the split cross attention optimization instead of the sub-quadratic one. Ignored when xformers is used.")
    attn_group.add_argument("--use-pytorch-cross-attention", action="store_true", help="Use the new pytorch 2.0 cross attention function.")

    parser.add_argument("--disable-xformers", action="store_true", help="Disable xformers.")

    vram_group = parser.add_mutually_exclusive_group()
    vram_group.add_argument("--highvram", action="store_true", help="By default models will be unloaded to CPU memory after being used. This option keeps them in GPU memory.")
    vram_group.add_argument("--normalvram", action="store_true", help="Used to force normal vram use if lowvram gets automatically enabled.")
    vram_group.add_argument("--lowvram", action="store_true", help="Split the unet in parts to use less vram.")
    vram_group.add_argument("--novram", action="store_true", help="When lowvram isn't enough.")
    vram_group.add_argument("--cpu", action="store_true", help="To use the CPU for everything (slow).")

    parser.add_argument("--dont-print-server", action="store_true", help="Don't print server output.")
    parser.add_argument("--quick-test-for-ci", action="store_true", help="Quick test for CI.")
    parser.add_argument("--windows-standalone-build", action="store_true", help="Windows standalone build: Enable convenient things that most people using the standalone windows build will probably enjoy (like auto opening the page on startup).")

    if arg_dict is not None:
        # Parse the provided dictionary of arguments
        args = parser.parse_args([], namespace=argparse.Namespace(**arg_dict))
    else:
        # Parse the command-line arguments
        args = parser.parse_args()

    if args.windows_standalone_build:
        args.auto_launch = True

    # save args to a json file
    check_and_create_directory()
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(vars(args), f)
        
    return args

def set_args(arg_dict):
    args = parse_args(arg_dict)
    return args

def get_args():
    # load args from the json file
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            arg_dict = json.load(f)
        args = argparse.Namespace(**arg_dict)
    except FileNotFoundError:
        print(f'Error: {JSON_FILE_PATH} not found')
        args = parse_args()  # fall back to default args if json file not found
    return args

args = get_args()