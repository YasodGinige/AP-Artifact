import subprocess
import pexpect
import re

class CyberTools():
    def __init__(self):
        self.nmap_memory = []
        self.metasploit_memory = []
        self.command_memory = []

    def run_nmap_commands(self, commands):
        pwd = 'GinSandeepa@44'                   ### ????????????????????????????????????????
        results = []
        for command in commands:
            if command[:4] == 'sudo':
                sudo_command = f"echo {pwd} | {command}"
            else:
                sudo_command = f"echo {pwd} | sudo -S {command}"
            try:
                result = subprocess.run(sudo_command, shell=True, text=True, check=True, capture_output=True)
                results.append(result.stdout)
                self.nmap_memory.append(result.stdout)
            except subprocess.CalledProcessError as e:
                results.append(e.stderr)
                self.nmap_memory.append(e.stderr)
        self.nmap_memory.append('< NEW >')
        return results

    def run_metasploit_commands(self, commands):
        child = pexpect.spawn('/usr/bin/msfconsole', timeout=120)
        results = []
        for command in commands:
            child.sendline(command)  # Send the command to msfconsole
            child.expect('msf6 >')   # Wait for the prompt to return
            results.append(child.before)
            self.metasploit_memory.append(child.before)

        child.sendline('exit')
        child.close()
        self.metasploit_memory.append('< NEW >') 
        return results

    def extract_commands(self, text):
        pattern = r'["`](.*?)["`]'
        raw_commands = re.findall(pattern, text)
        commands = [cmd for cmd in raw_commands if not cmd.strip().startswith('-')]
        self.command_memory.append(commands)
        return commands


