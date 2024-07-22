import subprocess
import pexpect
import time
import re

class CyberTools():
    def __init__(self):
        self.nmap_memory = []
        self.metasploit_memory = []
        self.command_memory = []
        self.prompt_regex = r'\x1b\[.*?msf6\x1b\[.*?\> '
        self.any_regex = re.compile(r'.*', re.DOTALL)

    def run_command(self, msfconsole, command):
        try:
            msfconsole.sendline(command)
            if command == 'r-un' or command == 'e-xploit':
                time.sleep(2)
                return read_output(msfconsole, timeout=30)
                
            elif command == 'who-ami':
                time.sleep(2)
                return read_output(msfconsole, timeout=10)
            else:
                msfconsole.expect(self.prompt_regex, timeout = 60)
                return msfconsole.after.decode('utf-8')
        except:
            return '\nAn error occured in the msfconsole.'


    def extract_commands(self, text):
        pattern = r'["`](.*?)["`]'
        raw_commands = re.findall(pattern, text)
        commands = [cmd for cmd in raw_commands if not cmd.strip().startswith('-')]
        self.command_memory.append(commands)
        return commands
    
    def read_output(self, msfconsole, timeout=30):
        start_time = time.time()
        output = []
        while True:
            line = msfconsole.readline()
            if line:
                output.append(line)
                if self.prompt_regex in line:
                    break
            if time.time() - start_time > timeout:
                break
        print('readline output:',output)
        return ''.join(output)

    def run_nmap_commands(self, commands):
        print('############', commands)
        pwd = 'yasod123'                   ### ????????????????????????????????????????
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
        output = '\n'.join(results)
        return output

    # def run_metasploit_commands(self, commands):
    #     commands.append('whoami')
    #     print('############', commands)
    #     sudo_password = 'yasod123'
    #     child = pexpect.spawn('sudo ' + commands[0], timeout=120)
    #     child.expect('password for .*:')
    #     child.sendline(sudo_password)
    #     child.expect('msf6 >')

    #     results = []
    #     for command in commands[1:]:
    #         child.sendline(command, timeout=120)  # Send the command to msfconsole
    #         child.expect('msf6 >')   # Wait for the prompt to return
    #         results.append(child.before)
    #         self.metasploit_memory.append(child.before)

    #     child.sendline('exit')
    #     child.close()
    #     self.metasploit_memory.append('< NEW >') 
    #     return results

    def run_metasploit_commands_new(self, commands):
        if commands[0] != 'msfconsole':
            commands.insert(0,'msfconsole')
        commands.append('whoami')
        print('############', commands)
        sudo_password = 'yasod123'
        msfconsole = pexpect.spawn('sudo ' + commands[0], timeout=120)
        msfconsole.expect('password for yasod:')
        msfconsole.sendline(sudo_password)
        msfconsole.expect(self.prompt_regex, timeout = 60)

        output_bucket = 'Each of the following command waits for 60s for the results to be completed. If the favourable result doesnt appear, you should move to the next task.\n'
        
        for command in commands[1:]:
            output = self.run_command(msfconsole, command)
            output_bucket += command+"\n"
            output_bucket += output
            if output == '\nAn error occured in the msfconsole.':
                break
            time.sleep(2)
        
        self.metasploit_memory.append(output_bucket)
        msfconsole.sendline('exit')
        msfconsole.close()
        return output_bucket

    def run_general_commands(self, commands):
        print('############', commands)
        pwd = 'yasod123'                   ### ????????????????????????????????????????
        results = []
        for command in commands:
            if command[:4] == 'sudo':
                sudo_command = f"echo {pwd} | {command}"
            else:
                sudo_command = f"echo {pwd} | sudo {command}"
            try:
                result = subprocess.run(sudo_command, shell=True, text=True, check=True, capture_output=True)
                results.append(result.stdout)
                self.nmap_memory.append(result.stdout)
            except subprocess.CalledProcessError as e:
                results.append(e.stderr)
                self.nmap_memory.append(e.stderr)
        output = '\n'.join(results)
        return output

    def run_metasploit_commands_search_itt(self, commands):
        if commands[0] != 'msfconsole':
            commands.insert(0,'msfconsole')
        commands.append('whoami')
        print('############', commands)
        sudo_password = 'yasod123'
        msfconsole = pexpect.spawn('sudo ' + commands[0], timeout=120)
        msfconsole.expect('password for yasod:')
        msfconsole.sendline(sudo_password)
        msfconsole.expect(self.prompt_regex, timeout = 60)

        output_bucket = 'Each of the following command waits for 60s for the results to be completed. If the favourable result doesnt appear, you should move to the next task.\n'
        
        for command in commands[1:]:
            if command[:6] == 'search':
                output = self.run_command(msfconsole, command)

            output = self.run_command(msfconsole, command)
            output_bucket += command+"\n"
            output_bucket += output
            if output == '\nAn error occured in the msfconsole.':
                break
            time.sleep(2)
        
        self.metasploit_memory.append(output_bucket)
        msfconsole.sendline('exit')
        msfconsole.close()
        return output_bucket


    
