# Program: CML External Management Installer
# Date: 5/3/2022
# By: Rob Ivancie
# RPC Method: HTTP Requests
# Description: This program implements external mgmt addresses on all device nodes
#              running in a specified CML lab using pre-determined interfaces
#              connecting to an external switch via a bridge cloud in CML.
#              This ultimately allows the CML nodes to access external services.
# Updated: 11/7/2022 - added new xel2 template and code to differentiate between IOSv and IOSvl2 platforms
#
import ipaddress
import urllib3
import CMLinfo
import GetLabs
import GetLabsDetail
import GetNodeConfig
import GetToken
import GetUserInput
import GlobalVar
import UpdateNodeConfig
from tkinter import *
from tkinter import messagebox

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CML_URL = "https://" + CMLinfo.CML["host"] + "/api"
CML_USER = CMLinfo.CML["username"]
CML_PASS = CMLinfo.CML["password"]

labname = "CML Lab " + CMLinfo.CML["host"]

if __name__ == "__main__":
    auth_token = GetToken.get_token(CML_URL, CML_USER, CML_PASS)
    print("#" * 113)
    labids = GetLabs.get_labs(auth_token, CML_URL, labname)
    print("#" * 113)
    GetLabsDetail.get_labsdetail(auth_token, CML_URL, labids)
    print("#" * 113)
    GetUserInput.get_user_input(auth_token, CML_URL, CML_USER, CML_PASS)
    print("#" * 113)
    print("The following output can be saved and sessions imported into SecureCRT")
    print("session_name,hostname,protocol,username,folder,emulation")

# Iterative for each node in the selected lab
    for counter1 in range(int(GlobalVar.global_node_count)):
        GlobalVar.global_nodeid = ("n" + str(counter1))
        GlobalVar.global_node_mac = ("0000.0123.0" + str(format(counter1, '03d')))
        GlobalVar.global_node_address = ipaddress.IPv4Address(GlobalVar.global_userstartaddress) + counter1
        GetNodeConfig.get_node_config(auth_token, CML_URL)
        if GlobalVar.global_node_type != "SKIP":
            UpdateNodeConfig.update_node_config(auth_token, CML_URL)
            GlobalVar.global_secureCRT = GlobalVar.global_secureCRT + (GlobalVar.global_node_hostname + ","
                                                                       + str(GlobalVar.global_node_address)
                                                                       + ",Telnet,admin," + GlobalVar.global_title
                                                                       + ",VT100\n")
    def display_info():
        top = Tk()
        top.geometry("600x600")
        top.title("SecureCRT Import Data")
        text_box = Text(top, height = 25, width = 80)
        text_box.pack(expand=TRUE)
        text_box.insert(END, GlobalVar.global_secureCRT)
        top.mainloop()

    display_info()
#    print(GlobalVar.global_secureCRT)