import openai
from pentestgpt.utils.APIs.module_import import dynamic_import
from pentestgpt.prompts.prompt_class import PentestGPTPrompt
import csv
import sys

# Load your OpenAI API key
openai.api_key = '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'

class Report_gen():
    def __init__(self, parsing_model="gpt-4-1106-preview", log_dir="logs"):
        self.log_dir = log_dir

        use_langfuse_logging=False
        report_generator_model_object = dynamic_import(
            parsing_model, self.log_dir, use_langfuse_logging=use_langfuse_logging
        )
        self.reportGenerator = report_generator_model_object
        self.prompts = PentestGPTPrompt

        (text_4,
                        self.report_generator_session_id,
                    ) = self.reportGenerator.send_new_message(
                        self.prompts.report_generator_init
                    )
        

    def generate_report(self,raw_text_path):
        file_path = 'resources/vulnerabilities.csv'

        headers = [
            'CVE', 'CVSS', 'Risk', 'Host', 'Protocol Port', 'Name', 
            'Synopsis', 'Description', 'Solution', 'Vulnerability State', 
            'IP Address', 'OS', 'CVSS Base Score', 'URL', 
            'Vulnerability Priority Rating (VPR)', 'First Found', 'Last Found']

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

        raw_text_file = open(raw_text_path, 'r')
        raw_text = raw_text_file.read()
        blocks = list(raw_text.split('======================================================================================='))

        with open(file_path, mode='a', newline='') as file:
            for i in blocks[1:]:
                result_text = list(i.split('RAW TOOL OUTPUT:'))[1]
                
                string_list = self.reportGenerator.send_message(self.prompts.report_generator_init + result_text[:7500], self.report_generator_session_id)
                print(result_text)
                print('##################################### ', string_list)
                print()

                writer = csv.writer(file)
                writer.writerow(list(string_list.split(',')))

report_gen = Report_gen()
report_gen.generate_report('logs/Pentest_raw_outputs.txt')   