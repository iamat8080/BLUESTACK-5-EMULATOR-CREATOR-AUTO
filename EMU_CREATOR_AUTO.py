import binascii
import os
import random
import shutil
import subprocess
import time
import uuid
import constant
from helper import get_traceback
import selenium.webdriver.common.service
import selenium.webdriver.remote.webdriver


cd_ = ["se_310410", "se_310260"]
ppro_ = ["stul", "stou", "snpe", "stwp", "stfg", "smtn", "anfg", "saet", "ptxg", "rogt", "xpxz", "lgvt"]


class CREATE_BSTK:
    def __init__(self, TH):
        self.uuid__ = str(uuid.uuid4())
        self.GAID_ = str(uuid.uuid4())
        self.path_X = fr"C:\ProgramData\BlueStacks_nxt\Engine\Pie64_{TH}"
        self.i_THREAD_NUM = self.TH = TH
        self.VM = r"C:\Program Files\BlueStacks_nxt\BstkVMMgr.exe"

    def exist(self):
        path = fr"C:\ProgramData\BlueStacks_nxt\Engine\Pie64_{self.TH}"
        if not os.path.isdir(path):
            os.mkdir(path)
            return False
        path = fr"C:\ProgramData\BlueStacks_nxt\Engine\Pie64_{self.TH}\Data.vhdx"
        if not os.path.isfile(path):
            return False
        path = fr"C:\ProgramData\BlueStacks_nxt\Engine\Pie64_{self.TH}\Pie64_{self.TH}.bstk"
        if not os.path.isfile(path):
            return False
        # for filename in glob.glob(f"./Output/ERRORRs/Output*.txt"):
        #     os.remove(filename)
        return True

    def bstk(self):
        if not os.path.isdir(self.path_X):
            os.mkdir(self.path_X)
        TH = self.TH
        path = self.path_X
        uuid__ = self.uuid__
        try:
            path_ = r"./dat/Pie64.bstk"
            datad_ = open(path_)
            data_ = datad_.readlines()
            datad_.close()
            if os.path.isfile(f"{path}/Pie64_{TH}.bstk"):
                os.remove(f"{path}/Pie64_{TH}.bstk")
            write_ = open(f"{path}/Pie64_{TH}.bstk", "w")
            for i in data_:
                if "54519f11-026f-4e53-ac3f-be1f672e4a75" in i:
                    i = i.replace('54519f11-026f-4e53-ac3f-be1f672e4a75', self.uuid__)
                if "Pie64" in i:
                    i = i.replace('Pie64', f"Pie64_{self.TH}")
                if "20884c3f-8699-47ed-a499-cd51f38f6a8f" in i:
                    i = i.replace('20884c3f-8699-47ed-a499-cd51f38f6a8f', self.GAID_)

                write_.writelines(i)
            write_.close()
        except Exception as e:

            return False
        return True

    def REGISTER(self, NEW=False):
        self.uuid__ = str(uuid.uuid4())
        self.GAID_ = str(uuid.uuid4())
        # if self.exist():
        #     if not NEW:
        #         return True
        if not self.bstk():
            return False
        if not self.vhd():
            return False

        path = fr"C:\ProgramData\BlueStacks_nxt\Engine\Pie64_{self.TH}\Pie64_{self.TH}.bstk"

        try:
            for i in range(4):
                time.sleep(3)
                try:
                    subprocess.Popen(f'"{self.VM}" unregistervm "Pie64_{self.TH}"',
                                     shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
                except Exception as e:
                    pass
                if i == 1:
                    time.sleep(3)
                time.sleep(4)
                b = subprocess.Popen(f'"{self.VM}" registervm {path}', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, encoding="utf-8",
                                     creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
                time.sleep(1)
                b.wait()
                output, erro = b.communicate()
                if erro:

                    try:
                        re_id = erro.split("} already exists")[0]
                        re_iid = re_id.split("UUID {")[1]

                        time.sleep(2)
                        p = subprocess.Popen(f'"{self.VM}" closemedium disk {re_iid.strip()}', stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, encoding="utf-8"
                                             , creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
                        time.sleep(2)
                        p.wait()
                        output, erro = p.communicate()
                        if erro:

                        continue
                    except:
                        return False

                """ 2 set HHD stuff """
                time.sleep(4)
                pa = subprocess.Popen(
                    f'"{self.VM}" storagectl {self.uuid__} --name IDE --add ide --controller PIIX3 --portcount 2 '
                    f"--hostiocache on --bootable on", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, encoding="utf-8", creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
                time.sleep(1)
                pa.wait()
                output, erro = pa.communicate()
                if erro:

                    continue

                pb = subprocess.Popen(
                    f'"{self.VM}" storageattach {self.uuid__} --storagectl IDE --port 0 --type hdd --device 0 '
                    fr'--medium "C:\ProgramData\BlueStacks_nxt\Engine\Nougat32\fastboot.vdi"',
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, encoding="utf-8", creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
                time.sleep(1)
                pb.wait()
                output, erro = pb.communicate()
                if erro:

                    continue

                pc = subprocess.Popen(
                    f'"{self.VM}" storagectl {self.uuid__} --name SATA --add sata --controller IntelAHCI'
                    f" --portcount 2 --hostiocache on --bootable off",
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, encoding="utf-8", creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
                time.sleep(1)
                pc.wait()
                output, erro = pc.communicate()
                if erro:

                    continue

                pd = subprocess.Popen(
                    f'"{self.VM}" storageattach {self.uuid__} --storagectl SATA --port 0 --type hdd --device 0 '
                    fr'--medium "C:\ProgramData\BlueStacks_nxt\Engine\Nougat32\Root.vhd"',
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, encoding="utf-8", creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
                time.sleep(1)
                pd.wait()
                output, erro = pd.communicate()
                if erro:

                    continue

                pe = subprocess.Popen(f'"{self.VM}" storageattach {self.uuid__} --storagectl SATA --port 1 --type hdd '
                                      fr'--device 0 --medium "C:\ProgramData\BlueStacks_nxt\Engine\Pie64_{self.TH}\Data.vhdx"',
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, encoding="utf-8",
                                      creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
                time.sleep(1)
                pe.wait()
                output, erro = pe.communicate()
                if erro:
                    continue
                time.sleep(2)
                return True
            else:
                return False
        except Exception as e:

            return False

    def UN_REGISTER(self):
        try:
            subprocess.Popen(f'"{self.VM}" unregistervm "Pie64_{self.TH}"',
                             shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            pass

    def vhd(self):
        try:
            os.remove(f"{self.path_X}/Data.vhdx")
            time.sleep(3)
        except Exception as e:

            pass

        # if not os.path.isfile(f"{self.path_X}/Data.vhdx"):
        try:
            shutil.copy2(fr"C:\ProgramData\BlueStacks_nxt\Engine\Pie64\Data.vhdx", f"{self.path_X}/Data.vhdx")
        except Exception as e:

            pass
        if not os.path.isfile(f"{self.path_X}/Data.vhdx"):
            return False
        return True

    def conf(self, FULL=True):
        path = r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf"
        data_ = open(path, "r+")
        uuf = str(random_hex_string(16))
        try:
            datax = []
            read_data = data_.readlines()
            dev = selenium.webdriver.common.service.utils.free_port()
            adb_dev = selenium.webdriver.common.service.utils.free_port()
            for line in read_data:
                if f"Pie64_{self.TH}" in line:
                    break
            else:
                new_data = open(r"./dat/bluestacks.conf")
                new_datax = new_data.readlines()
                new_data.close()
                for line in new_datax:
                    if f"Pie64.android_id" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.android_id="{uuf}"\n')

                    # if f"Pie64.adb_port" in line:
                    #     line = line.replace(line, f'bst.instance.Pie64_{self.TH}.adb_port="{9000 + int(self.TH)}"\n')
                    if f"Pie64.adb_port" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.adb_port="{dev}"\n')

                    # if f"Pie64.status.adb_port" in line:
                    #     line = line.replace(line,
                    #                         f'bst.instance.Pie64_{self.TH}.status.adb_port="{9000 + int(self.TH)}"\n')
                    if f"Pie64.status.adb_port" in line:
                        line = line.replace(line,
                                            f'bst.instance.Pie64_{self.TH}.status.adb_port="{dev}"\n')

                    if f"Pie64.display_name" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.display_name="THREAD_{self.TH}"\n')

                    if f"Pie64.max_fps" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.max_fps="10"\n')

                    if f"Pie64.status.session_id" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.status.session_id="0"\n')

                    if f"Pie64." in line:
                        line = line.replace("Pie64.", f'Pie64_{self.TH}.')

                    if f"Pie64_{self.TH}.device_carrier_code" in line:
                        line = line.replace(line,
                                            f'bst.instance.Pie64_{self.TH}.'
                                            f'device_carrier_code="{random.choice(cd_)}"\n')

                    if f"Pie64_{self.TH}.device_profile_code" in line:
                        line = line.replace(line,
                                            f'bst.instance.Pie64_{self.TH}.device_profile_code='
                                            f'"{random.choice(ppro_)}"\n')

                    if f"Pie64_{self.TH}.android_google_ad_id" in line:
                        line = line.replace(line,
                                            f'bst.instance.Pie64_{self.TH}.android_google_ad_id="{self.GAID_}"\n')

                    if f"Pie64_{self.TH}.show_sidebar" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.show_sidebar="0"\n')

                    if f"Pie64_{self.TH}.ram" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.ram="1024"\n')

                    datax.append(line)

            for line in read_data:
                if f"Pie64_{self.TH}.android_id" in line:
                    line = line.replace(line, f'bst.instance.Pie64_{self.TH}.android_id="{uuf}"\n')

                if FULL:

                    # if f"Pie64_{self.TH}.adb_port" in line:
                    #     line = line.replace(line, f'bst.instance.Pie64_{self.TH}.adb_port="{9000 + int(self.TH)}"\n')
                    if f"Pie64_{self.TH}.adb_port" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.adb_port="{dev}"\n')

                    # if f"Pie64_{self.TH}.status.adb_port" in line:
                    #     line = line.replace(line, f'bst.instance.Pie64_{self.TH}.status.adb_port="{9000 + int(self.TH)}"\n')
                    if f"Pie64_{self.TH}.status.adb_port" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.status.adb_port="{dev}"\n')

                    if f"Pie64_{self.TH}.device_carrier_code" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.'
                                                  f'device_carrier_code="{random.choice(cd_)}"\n')

                    if f"Pie64_{self.TH}.device_profile_code" in line:
                        line = line.replace(line, f'bst.instance.Pie64_{self.TH}.'
                                                  f'device_profile_code="{random.choice(ppro_)}"\n')

                if f"Pie64_{self.TH}.display_name" in line:
                    line = line.replace(line, f'bst.instance.Pie64_{self.TH}.display_name="THREAD_{self.TH}"\n')

                if f"Pie64_{self.TH}.max_fps" in line:
                    line = line.replace(line, f'bst.instance.Pie64_{self.TH}.max_fps="7"\n')

                if f"Pie64_{self.TH}.android_google_ad_id" in line:
                    line = line.replace(line,
                                        f'bst.instance.Pie64_{self.TH}.android_google_ad_id="{self.GAID_}"\n')

                if f"Pie64_{self.TH}.status.session_id" in line:
                    line = line.replace(line, f'bst.instance.Pie64_{self.TH}.status.session_id="0"\n')

                if f"Pie64_{self.TH}.show_sidebar" in line:
                    line = line.replace(line, f'bst.instance.Pie64_{self.TH}.show_sidebar="0"\n')

                if f"Pie64_{self.TH}.ram" in line:
                    line = line.replace(line, f'bst.instance.Pie64_{self.TH}.ram="1024"\n')

                if 'enable_adb_access="0"' in line:
                    line = line.replace(line, f'bst.enable_adb_access="1"\n')

                if "fresh_cpu_ram" in line:
                    line = line.replace(line, f'bst.fresh_cpu_ram="1024"\n')

                if "fresh_cpu_core" in line:
                    line = line.replace(line, f'bst.fresh_cpu_core="1"\n')

                if "show_cloud_instance" in line:
                    line = line.replace(line, f'bst.feature.show_cloud_instance="0"\n')

                if "feature.rooting" in line:
                    line = line.replace(line, f'bst.feature.rooting="1"\n')

                if "bluestacksX" in line:
                    line = line.replace(line, f'bst.feature.bluestacksX="0"\n')

                if "bst.create_desktop_shortcuts" in line:
                    line = line.replace(line, f'bst.create_desktop_shortcuts="0"\n')

                if "bst.country=" in line:
                    line = line.replace(line, f'bst.country="US"\n')

                datax.append(line)

            data_.seek(0)
            for i in datax:
                data_.writelines(i)
            data_.truncate()
            data_.close()
        except Exception as e:
            return False
        return True

    def REMOVE_ALL(self):

        try:
            shutil.rmtree(self.path_X, ignore_errors=True)
        except:
            pass


def bytes_to_hex(buffer: bytes) -> str:
    return binascii.hexlify(buffer).decode()


def random_hex_string(length: int):
    get_random_bytes = os.urandom
    buffer = get_random_bytes(int(length / 2))
    return bytes_to_hex(buffer)
