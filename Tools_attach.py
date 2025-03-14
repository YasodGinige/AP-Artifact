import subprocess
import pexpect
import time
import re
from repitition_identifier import RepititionIdentifier_module
from pentestgpt.prompts.prompt_class import PentestGPTPrompt
import sys
import os

class CyberTools():
    def __init__(self):
        self.nmap_memory = []
        self.metasploit_memory = []
        self.command_memory = []
        self.prompt_regex = r'\x1b\[.*?msf6\x1b\[.*?\> '
        self.open_terminal = r'[rR \n]'
        self.any_regex = re.compile(r'.*', re.DOTALL)
        self.repititionIdentifier = RepititionIdentifier_module()
        self.tool_output = ''
        self.prompts = PentestGPTPrompt
        self.log_dir = 'logs'

    def write_raw_text(self,text):
        if text == 'clear':
            text_file = open(os.path.join(self.log_dir, 'Pentest_raw_outputs.txt'),'w')
            text_file.close()
        else:
            text_file = open(os.path.join(self.log_dir, 'Pentest_raw_outputs.txt'),'a')
            text_file.write(text)
            text_file.close()

    def run_command(self, msfconsole, command):
        
        msfconsole.sendline(command)
        if command == 'run' or command == 'exploit' or command == 'whoami':
            output = ""
            while True:
                try:
                    msfconsole.expect('\n', timeout=12)
                    output += (msfconsole.before.decode('utf-8') + msfconsole.after.decode('utf-8'))
                    if msfconsole.after.decode('utf-8').strip().endswith('> '):
                        break

                except pexpect.TIMEOUT:
                    print("Command timed out or no more output.")
                    break
                except pexpect.EOF:
                    print("EOF received from msfconsole.")
                    break
            return output

        else:
            msfconsole.expect(self.prompt_regex, timeout = 20)
            return msfconsole.after.decode('utf-8')
        

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
        output = '\n'.join(results)
        return output


    def run_metasploit_commands_new(self, commands):
        if commands[0] != 'msfconsole':
            commands.insert(0,'msfconsole')
        if commands[-1] != 'whoami':
            commands.append('whoami')
        print('############', commands)
        sudo_password = 'GinSandeepa@44'
        msfconsole = pexpect.spawn(commands[0], timeout=120)
        
        msfconsole.expect(self.prompt_regex, timeout = 60)
        
        output_bucket = 'Each of the following command waits for 60s for the results to be completed. If the favourable result doesnt appear, you should move to the next task.\n'
        
        for command in commands[1:]:
            output = self.run_command(msfconsole, command)
            output_bucket += command+"\n"
            output_bucket += output
            if output == '\nAn error occured in the msfconsole.':
                break
            time.sleep(1)
        
        self.metasploit_memory.append(output_bucket)
        msfconsole.sendline('exit')
        msfconsole.close()
        return output_bucket

    def run_general_commands(self, commands):
        
        pwd = 'GinSandeepa@44'                   ### ????????????????????????????????????????
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

    def triger_the_tool(self, tool, commands_list, pentestModule):
        if tool == 'nmap':
            return self.run_nmap_commands(commands_list)
        
        elif tool == 'metasploit':
            #return cyber_tools.run_metasploit_commands_new(commands_list)
            return self.run_metasploit_commands_search_itt(commands_list, pentestModule)
        else:
            return self.run_general_commands(commands_list)

    def run_msf_search_exploits(self, exploit_list, rest_commands):
        concat_output = ''
        for ind, command in enumerate(exploit_list):
            temp_list = [command] + rest_commands
            concat_output += self.run_metasploit_commands_new(temp_list)
            concat_output +='\n\n'
        print('######## concat output:', concat_output)
        return concat_output

    #self.generatorAgent , self.commandExtractor, self.input_parsing_handler, self.prompts.msf_comm_extract, self.command_extractor_session_id
    #def run_sub_generator(self, command, generator, commandExtractor, input_parsing_handler, command_extractor_session_id):
    def run_sub_generator(self, command, pentestModule):
        generated_response = pentestModule.generatorAgent.invoke( self.prompts.metasploit_generation + command)

        self.write_raw_text('COMMANDS:\n'+ generated_response + '\n\n')

        extracted_output = pentestModule.commandExtractor.send_message(
            self.prompts.command_extractor_metasploit + generated_response, pentestModule.command_extractor_session_id
        )

        tool = 'metasploit'
        temp_command_list = list(extracted_output.split('\n'))
        
        print('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-')
        
        for j, com in enumerate(temp_command_list):
            if 'msf6>' in com:
                temp_command_list[j] = com.split('msf6>')[1]
        
        self.tool_output = self.triger_the_tool(tool, temp_command_list, pentestModule)
        print(self.tool_output)
        return self.tool_output



    def  run_single_exploit(self, commands):
        if commands[0][:2] == 'cd':
            commands.pop(0)
        if commands[0] != 'msfconsole':
            commands.insert(0,'msfconsole')
        if commands[-1] != 'whoami':
            commands.append('whoami')

        sudo_password = 'GinSandeepa@44'
        msfconsole = pexpect.spawn(commands[0], timeout=20)
        #msfconsole.expect('password for ygin2127:')
        #msfconsole.sendline(sudo_password)
        msfconsole.expect(self.prompt_regex, timeout = 20)

        output_bucket = ''
        temp_commands = commands[1:]
        for ind, command in enumerate(temp_commands):
            output = self.run_command(msfconsole, command)
            output_bucket += (command+"\n")
            output_bucket += output

            if command[:3] == 'use':
                temp_commands.insert(ind+1, 'info')
            time.sleep(1)

        self.metasploit_memory.append(output_bucket)
        msfconsole.sendline('exit')
        msfconsole.close()
        return output_bucket

    def run_search_exploits(self, search_command, pentestModule, exploit_given):
        
        sudo_password = 'GinSandeepa@44'
        msfconsole = pexpect.spawn('msfconsole', timeout=120)
        #msfconsole.expect('password for ygin2127:')
        #msfconsole.sendline(sudo_password)
        msfconsole.expect(self.prompt_regex, timeout = 60)

        output = self.run_command(msfconsole, search_command)
        extracted_output = pentestModule.commandExtractor.send_message(pentestModule.prompts.msf_comm_extract + output[:8000], pentestModule.command_extractor_session_id)
        exploit_list = extracted_output.split(',')
        exploit_list.insert(0, exploit_given)
        msfconsole.sendline('exit')
        msfconsole.close()
        
        print('SERCH EXPLOIT LIST:\n', exploit_list)
        summary_bucket = ''

        for indx, command in enumerate(exploit_list):

            generated_response = pentestModule.generatorAgent.invoke( self.prompts.metasploit_generation + command)
            self.write_raw_text('COMMANDS:\n'+ generated_response + '\n\n')

            extracted_output = pentestModule.commandExtractor.send_message(
                self.prompts.command_extractor_metasploit + generated_response, pentestModule.command_extractor_session_id
            )

            tool = 'metasploit'
            temp_command_list = list(extracted_output.split('\n'))
            
            for j, com in enumerate(temp_command_list):
                if 'msf6>' in com:
                    temp_command_list[j] = com.split('msf6>')[1]


            output = self.run_single_exploit(temp_command_list)
            summarized_output = pentestModule.input_parsing_handler(output, special_script = self.prompts.metasploit_summarization)
            summary_bucket += (summarized_output + '\n\n')

            if indx == 0:
                self.write_raw_text('RESULTS:\n' + summarized_output + '\n--------\n')
            else:
                self.write_raw_text(summarized_output + '\n--------\n')
            
        #output_bucket += self.run_msf_search_exploits(exploit_list, commands[ind+2:])

        print('MY ITERATIVE OUTPUT BUCKET:\n\n\n', summary_bucket)
        return summary_bucket





    #def run_metasploit_commands_search_itt(self, commands, generator, command_extractor, input_parsing_handler, msf_comm_extract_prompt, session_id):
    def run_metasploit_commands_search_itt(self, commands, pentestModule):

        flag = False
        exploit_given = ''
        for i in commands:
            if i[:3] == 'use':
                exploit_given = i
            if i[:6] == 'search':
                flag = True
                search_command = i

        if flag:
            output = self.run_search_exploits(search_command, pentestModule, exploit_given)
        else:
            output = self.run_single_exploit(commands)

        return output

    



    