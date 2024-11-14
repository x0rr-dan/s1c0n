from os import system, path, mkdir
from core.color import Color
# 1.3 wellcome screen
def logo():
    system("clear")
    print(f"""{Color.green}{Color.bold}
    \t              ┏━┓╺┓ ┏━╸┏━┓┏┓╻
    \t              ┗━┓ ┃ ┃  ┃┃┃┃┗┫
    \t              ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.8

                        Simple Recon
                        Coded by {Color.reset}{Color.red}{Color.bold}x0r{Color.yellow}{Color.bold}\n\t       https://github.com/x0rr-dan/s1c0n{Color.red}{Color.bold}\n\t           Dinus Open Source Community{Color.red}""")
# 1.4 help
def break_and_help():
    print("\n\t   [?] Usage example: sicon -u target.com")

# 1.5 clean file that doesnt use
def clean(extension):
    system(f"rm -rf .list*.{extension}")

# 1.6 create folder report
def create_report_folder(target):
    folder_name = f"report_{target}"
    if not path.exists(folder_name):
        mkdir(folder_name)
    else:
        pass