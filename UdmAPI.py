import paramiko

# command = "df"

# Update the next three lines with your
# server's information

# host = "192.168.1.1"
# username = "root"
# password = "Scheiboeck2002!"

# client = paramiko.client.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(host, username=username, password=password)
# _stdin, _stdout, _stderr = client.exec_command(command)
# print(_stdout.read().decode())
# client.close()

# /etc/init.d/S04ubnt-fan-speed start
# killall -9 S04ubnt-fan-speed ubnt-fan-speed
# echo 1 > /sys/class/hwmon/hwmon0/device/pwm1_enable
# echo 1 > /sys/class/hwmon/hwmon0/device/pwm2_enable

# echo 255 > /sys/class/hwmon/hwmon0/device/pwm1
# echo 255 > /sys/class/hwmon/hwmon0/device/pwm2
FAN_AUTO = "auto"
FAN_LOW = "75"
FAN_MEDIUM = "100"
FAN_HIGH = "255"
FAN_MIDDLE = "150"


class UdmAPI:
    def __init__(self, username, password, host):
        self._logged_in = False
        self._username = username
        self._password = password
        self._host = host

        if self._username == "":
            return

        self._client = paramiko.client.SSHClient()
        self._state = {}

        self.login()

    def login(self):
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(
            self._host,
            username=self._username,
            password=self._password,
            allow_agent=False,
        )

    def exec(self, command):
        _stdin, _stdout, _stderr = self._client.exec_command(command)
        print(_stdout.read().decode())

    def setTemp(self, mode: list[str]):
        if mode == FAN_AUTO:
            self.resetControl()
        else:
            self.takeControl()

            self.exec("echo %s > /sys/class/hwmon/hwmon0/device/pwm1" % mode)
            self.exec("echo %s > /sys/class/hwmon/hwmon0/device/pwm2" % mode)
            print(mode)

    def takeControl(self):
        self.exec("killall -9 S04ubnt-fan-speed ubnt-fan-speed")
        # self.exec("echo 1 > /sys/class/hwmon/hwmon0/device/pwm1_enable") default
        # self.exec("echo 1 > /sys/class/hwmon/hwmon0/device/pwm2_enable") default

    def resetControl(self):
        self.exec("/etc/init.d/S04ubnt-fan-speed start")

    def getTemp(self):
        self.exec("ubnt-systool cputemp")

    def close(self):
        self._client.close()

    def update(self):
        self.getTemp()

    @property
    def state(self):
        return self._state
