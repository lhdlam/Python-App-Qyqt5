import argparse


def createArgParser():
    # Create ArgsParser
    parser = argparse.ArgumentParser()

    # Accept just one input as path
    parser.add_argument("path", help="Path to Product Folder or its parent")

    # -p
    # --products
    parser.add_argument("-p", "--products",
                        type=str,
                        help="Product list file",
                        required=True)

    # -t
    # --path-type
    parser.add_argument("-t", "--path-type",
                        type=int, choices=[1, 2], default=1,
                        help="Path type (1: One Product folder, 2: Product folder's parent)"
                        )

    # -m
    # --mode
    parser.add_argument("-m", "--mode",
                        type=int, choices=[1, 2, 3, 4, 5], default=1,
                        help="Path type (1: Download, 2: Text data validation, 3: Text data process, 4: Item Info, 5:Export)"
                        )

    # -o
    # --overwrite
    parser.add_argument("-o", "--overwrite",
                        action="store_true",
                        help="Overwrite or not"
                        )
    # -s
    # --sheet
    parser.add_argument("-s", "--sheet",
                        type=int, default=1,
                        help="Sheet number, default 1 (the most left sheet)"
                        )

    # -r
    # --report
    parser.add_argument("-r", "--report",
                        type=str,
                        default="report.csv",
                        help="Report file",
                        )

    # -u
    # --update-version-only
    parser.add_argument("-u", "--update-version-only",
                    action="store_true",
                    default=False,
                    help="Update version information only")

    return parser

def createExportArgParser():
    # Create ArgsParser
    parser = argparse.ArgumentParser()

    # Accept just one input as path
    parser.add_argument("-p","--path", 
                        nargs='+',
                        default=[],
                        help="Path to Product Folder or its parent")

    parser.add_argument("-e", "--export-path",
                    type=str,
                    default="./",
                    help="Export path")

    parser.add_argument("-a", "--add-header",
                    action="store_true",
                    help="Add header to csv file")

    parser.add_argument("-f", "--force-export",
                    action="store_true",
                    help="Force to export without image processing result checking")

    # -r
    # --report
    parser.add_argument("-r", "--report",
                        type=str,
                        default="report.csv",
                        help="Report file",
                        )

    return parser
if __name__ == '__main__':
    # Create Menus
    argsParser = createArgParser()

    # Parsing command line args
    args = argsParser.parse_args()

    # Product path
    print("Product path : ", args.path)
    print("Product list file :", args.products)
    print("Path type: ", args.path_type)
    print("Run mode :", args.mode)
    print("Overwrite :", args.overwrite)
    print("Sheet number :", args.sheet)
    print("Update version only :", args.update_version_only)
