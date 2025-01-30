import openai

# Load your OpenAI API key
openai.api_key = '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'

# Read the content of the .txt file
with open('logs/Metasploitable_Pentest_raw_best.txt', 'r', encoding='utf-8') as file:
    file_content = file.read()

# Prepare the API call to summarize the text
file_content = file_content[:8100]
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": """You will be given a text which contains row information gathered from a penetration test. Your task is to prepare a table by analyzing all the information gathered. The table should should contain following columns.
    CVE, CVSS, Risk, Host, Protocol, Port, Name, Synopsis, Description, Solution, Vulnerability State, IP Address, OS, CVSS Base Score, URL, Vulnerability Prority Rating (VPR), First Found, Last Found.
    An example is given below. 
    CVE	CVSS	Risk	Host	Protocol	Port	Name	Synopsis	Description	Solution	Vulnerability State	IP Address	OS	CVSS Base Score	URL	Vulnerability Priority Rating (VPR)	First Found	Last Found
CVE-2011-2523	7	High	yasod-virtualbox1.it.usyd.edu.au	FTP	21	vsftpd 2.3.4	Outdated FTP server with potential security vulnerabilities.	FTP server vsftpd 2.3.4 known to have backdoor vulnerability.	Upgrade to a secure version of FTP server.	Active	10.66.30.131	Unix, Linux	10	http://pastebin.com/AetT9sS5	High	2024-10-17 05:51:44.576024	2024-10-17 05:51:44.576027
    Make sure you only get an idea from the example and generate a new table for the given information in the following messages. Include all the vulnerabilities given in the message."""},
        {"role": "user", "content": file_content}
    ],
    max_tokens=4096  # Adjust token limit as needed for summary length
)

# Print the summary
print(response.choices[0].message.content)