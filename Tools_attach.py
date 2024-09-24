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
                    msfconsole.expect('\n', timeout=20)
                    output += msfconsole.before.decode('utf-8') + msfconsole.after.decode('utf-8')
                    if msfconsole.after.decode('utf-8').strip().endswith('> '):
                        break
                except pexpect.TIMEOUT:
                    print("Command timed out or no more output.")
                    break
                except pexpect.EOF:
                    print("EOF received from msfconsole.")
                    break
            return output
            
        elif command == 'whoa-mi':
            time.sleep(2)
            # msfconsole.expect(self.open_terminal, timeout = 30)
            # return msfconsole.after.decode('utf-8')
            index = msfconsole.expect([pexpect.TIMEOUT, pexpect.EOF, '> '], timeout=10)  # Look for the prompt or timeout
            if index == 0:
                print("Command timed out")
                return None
            elif index == 1:
                print("EOF received from msfconsole")
                return None
            # Capture the output after command execution
            return msfconsole.after.decode('utf-8')  
            # msfconsole.expect(self.prompt_regex, timeout = 30)
            # whoami_response = msfconsole.after.decode('utf-8')
            # human_input = self.repititionIdentifier.human_react(PTT, last_step, console, whoami = False)
            # if human_input.lower() == 'yes':
            #     #what to do
            #     sys.exit()
            # else:
            #     return whoami_response
        else:
            msfconsole.expect(self.prompt_regex, timeout = 30)
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
        if commands[-1] != 'whoami':
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

    def triger_the_tool(self, tool, commands_list, generator, commandExtractor, input_parsing_handler, command_extractor_session_id):
        if tool == 'nmap':
            return self.run_nmap_commands(commands_list)
        
        elif tool == 'metasploit':
            #return cyber_tools.run_metasploit_commands_new(commands_list)
            return self.run_metasploit_commands_search_itt(commands_list, generator, commandExtractor, self.prompts.msf_comm_extract, input_parsing_handler, command_extractor_session_id)
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

    def run_sub_generator(self, command, generator, commandExtractor, input_parsing_handler, command_extractor_session_id):
        generated_response = generator.invoke( self.prompts.metasploit_generation + command)

        self.write_raw_text('COMMANDS:\n'+ generated_response + '\n\n')

        extracted_output = commandExtractor.send_message(
            self.prompts.command_extractor_metasploit + generated_response, command_extractor_session_id
        )

        tool = 'metasploit'
        temp_command_list = list(extracted_output.split('\n'))
        
        print('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-')
        
        # if len(tool_list) >1:
        #         temp_command_list = list(tool_wise_commands[i].split('\n'))
        # else:
        # temp_command_list = tool_wise_commands

        for j, com in enumerate(temp_command_list):
            if 'msf6>' in com:
                temp_command_list[j] = com.split('msf6>')[1]
        
        self.tool_output = self.triger_the_tool(tool, temp_command_list, generator, commandExtractor, input_parsing_handler, command_extractor_session_id)
        print(self.tool_output)
        return self.tool_output

    def run_metasploit_commands_search_itt(self, commands, generator, command_extractor, input_parsing_handler, msf_comm_extract_prompt, session_id):
        if commands[0][:2] == 'cd':
            commands.pop(0)
        if commands[0] != 'msfconsole':
            commands.insert(0,'msfconsole')
        if commands[-1] != 'whoami':
            commands.append('whoami')
        print('##____###', commands)
        sudo_password = 'yasod123'
        msfconsole = pexpect.spawn('sudo ' + commands[0], timeout=120)
        msfconsole.expect('password for yasod:')
        msfconsole.sendline(sudo_password)
        msfconsole.expect(self.prompt_regex, timeout = 60)

        #output_bucket = 'Each of the following command waits for 60s for the results to be completed. If the favourable result doesnt appear, you should move to the next task.\n'
        output_bucket = ''

        temp_commands = commands[1:]
        for ind, command in enumerate(temp_commands):
            if command[:6] == 'search':
                output = self.run_command(msfconsole, command)
                extracted_output = command_extractor.send_message(msf_comm_extract_prompt + output[:800], session_id)
                exploit_list = extracted_output.split(',')
                msfconsole.sendline('exit')
                msfconsole.close()
                if temp_commands[ind+1][:3] == 'use':
                    exploit_list.append(temp_commands.pop(ind+1))
                
                print('SERCH EXPLOIT LIST:\n', exploit_list)
                for indx, command in enumerate(exploit_list):
                    output_bucket += self.run_sub_generator(command, generator, command_extractor, input_parsing_handler, session_id)
                    output_bucket += '\n\n'
                    parsed_input = input_parsing_handler(output_bucket, special_script = self.prompts.metasploit_summarization)

                    if indx == 0:
                        self.write_raw_text('RESULTS:\n' + parsed_input + '\n--------\n')
                    else:
                        self.write_raw_text(parsed_input + '\n--------\n')

                    print("\n+++++++++++++++++++++++++++++++++++++++\n")
                    print(parsed_input)
                    print("\n+++++++++++++++++++++++++++++++++++++++\n")
                    
                #output_bucket += self.run_msf_search_exploits(exploit_list, commands[ind+2:])

                print('MY ITERATIVE OUTPUT BUCKET:\n\n\n', output_bucket)
                return output_bucket

            output = self.run_command(msfconsole, command)
            output_bucket += command+"\n"
            output_bucket += output
            if command[:3] == 'use':
                temp_commands.insert(ind+1, 'info')
            if output == '\nAn error occured in the msfconsole.':
                break
            time.sleep(2)
        
        self.metasploit_memory.append(output_bucket)
        msfconsole.sendline('exit')
        msfconsole.close()
        return output_bucket

    



    
