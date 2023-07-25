import time
import paramiko
from os import system
from sys import exit, stderr
from typing import Any
from loguru import logger

try:
    from makeConfigs import Configs

except ImportError as e:
    logger.error(e)
    logger.warning(
        "No configs file found, writeing configs and using default configs")
    defaultContent = '''
class Configs:
    __name__ = "Configs"
    class logConfigs:
        needConsoleOutPut   = True
        needFileOutPut      = True
        loglevel            = "DEBUG"
        fileName            = "makeProject.log"
        fileEncoding        = "utf-8"

    class timeConfigs:
        timeFormat          = "%Y-%m-%d [%H:%M:%S] "
        timeZone            = "Asia/Shanghai"

    class SSHConfigs:
        host                = "192.168.31.100"
        port                = "22"
        username            = "root"
        password            = "20091126"
'''
    file = open("makeConfigs.py", "w", encoding="utf-8")
    file.write(defaultContent)
    file.close()
    from makeConfigs import Configs


def getNowTime() -> str:
    return time.strftime(
        Configs.timeConfigs.timeFormat, time.localtime()
    )


def writeLog(data: Any, logType: str = "INFO") -> None:
    logObject = open(
        Configs.logConfigs.fileName, "a",
        encoding=Configs.logConfigs.fileEncoding
    )
    funcMap = {
        "INFO":     logger.info,
        "DEBUG":    logger.debug,
        "ERROR":    logger.error,
        "CRITICAL": logger.critical,
        "WARNING":  logger.warning,
        "SUCCESS":  logger.success,
        "TRACE":    logger.trace
    }
    toUseFunc = funcMap[logType]
    if type(data) == list:
        for item in data:
            item = item.replace("\n", "")
            if (Configs.logConfigs.needFileOutPut):
                logObject.write(
                    getNowTime() + str(item) + '\n'
                )
            if (Configs.logConfigs.needConsoleOutPut):
                toUseFunc(str(item))
        logObject.close()
        return

    if type(data) == str:
        data = data.replace("\n", "")
        if (Configs.logConfigs.needFileOutPut):
            logObject.write(getNowTime() + data + '\n')
        if (Configs.logConfigs.needConsoleOutPut):
            toUseFunc(data)
        logObject.close()
        return

    else:
        logObject.close()
        writeLog("Error: logType is not supported", "ERROR")
        raise TypeError("Data type not supported")


@logger.catch
def executeCommand(command: str) -> None:
    writeLog("Executing command: " + command)
    writeLog("Command Exit Code:" + str(system(command)))


@logger.catch
def sshExec(commands: list) -> tuple:
    SSHConnConf = Configs.SSHConfigs
    host_ip = SSHConnConf.host
    user_name = SSHConnConf.username
    host_port = SSHConnConf.port
    password = SSHConnConf.password
    command = ""
    for item in commands:
        command += item + ";"
    # SSH远程连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
    ssh.connect(host_ip, host_port, user_name, password)
    # 执行命令并获取执行结果
    _, stdout, stderr = ssh.exec_command(command)
    out = stdout.readlines()
    err = stderr.readlines()
    # 关闭连接
    ssh.close()
    return (out, err)


@logger.catch
def main() -> int:
    # TODO Fix copyDist.py
    # if len(argv) > 1 and argv[1] == '--changeAssest':
    #     copyCommand = "rm -rf /Volumes/picture/dist & cp -r ./dist /Volumes/picture"
    # else:
    #     copyCommand = "python copyDist.py"
    buildCommand = [
        './build.sh'
    ]
    writeLog(f'CopyCommand: {buildCommand}')
    if Configs.logConfigs.loglevel != None:
        logger.remove()
        logger.add(
            stderr, level=Configs.logConfigs.loglevel
        )
    for command in buildCommand:
        executeCommand(command)
    writeLog("Compiled successfully")
    sshLists = [
        "cd /home/dralfred/myOj/OnlineJudgeDeploy/",
        "./getBackend.sh",
        "docker restart oj-backend"
    ]
    out, err = sshExec(sshLists)
    writeLog(out), writeLog(err)
    writeLog("Deployed successfully")
    writeLog("Program Exited with code 0")
    return 0


if __name__ == '__main__':
    exit(main())
