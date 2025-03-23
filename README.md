# AutoPentester


<!-- Quick Start -->
## Installation
1. Create a virtual environment. (`python3 -m venv myenv`, `source myenv/bin/activate`)
2. Clone the project and install the requirements.
     - `git clone <repo_url>`
     - `cd AP_Artifact`
     - `pip3 install -r requirements.txt`
     - `pip3 install -e .`
3. To use OpenAI API
   - **Ensure that you have link a payment method to your OpenAI account.**
   - export your API key with `export OPENAI_API_KEY="<your key here>"`
4. To run the framework, type  `pentestgpt --loggin`
5. You will be asked for your OpenAI key and the IP address.
6. Do you want to continue from previous session? (y/n) -> Press n
7. Give a pentesting task. You can use a prompt like "I want to test the machine with the IP (targe_IP)"
8. Only for the first run, it will take 10 minutes to build the vectorbase of the RAG module at the beginning. Please wait until it starts its process.

### Log files
The processed log files are in the processed_log_files directory.
The quantitative results were calculated baseed on these log files.

### Survey analysis
The analysis of the survey is in the Survey_analysis directory.
Run the analysis.py to plot the graphs.
