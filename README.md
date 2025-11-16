## Frame 'em all

A murder-mystery game about deception - you are the killer.

Made for Junction 2025.

### Setup instructions

1. Run the following commands to fetch the repo from GitHub and install required packages (Python 3 installation required):

```
git clone https://github.com/JaaskelainenL/junction-25.git
cd junction-25
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```
2. Next, create file GEMINI_API_KEY in to the root folder of the project and put your Google Cloud / Gemini API key there

3. Run the game with the following command:

```
python main.py
```