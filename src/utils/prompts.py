"""Claude API prompts for election data extraction.

This module contains the necessary prompts for interacting with the Claude API to
extract U.S. election data from images. It defines:
- A system prompt that instructs Claude on the response format and how to handle data extraction.
- A user prompt that provides detailed instructions on what election-related information to extract.
- A custom function to generate tailored prompts for specific election years or race types (e.g., Presidential, Senate, House races).

The extracted data is expected to be organized in a CSV format with fields like STATE, YEAR, RACE_TYPE, CONGRESSIONAL_DISTRICT, CANDIDATE_NAME, CANDIDATE_PARTY, and VOTES.

Key handling cases:
- Special cases for Presidential and Senate races (e.g., missing candidate names or congressional districts).
- Validation of data fields like YEAR and VOTES to ensure they are integers.
"""

# System prompt that instructs Claude on how to format the response
SYSTEM_PROMPT = """
Your goal is to only provide the data in a csv format. You do not believe in responding in any other format.
The data is in the image. Ignore all data in table format. You do not see tables.
However, you can tell if a page is formatted as two columns. Write names exactly as they appear
do not try to predict correct spellings assume the document given is correct.
"""

# User prompt with detailed instructions on what to extract
USER_PROMPT = """
You will be provided with an image containing U.S. election data, and your task is to extract and organize
the following information into a CSV file:

STATE (name of the state as a string)
YEAR (election year as an integer)
RACE_TYPE (type of election race, e.g., Senate, House, Governor)
CONGRESSIONAL_DISTRICT (district number for representative races as an integer, or leave blank for non-applicable races)
CANDIDATE_NAME (name of the candidate as a string)
CANDIDATE_PARTY (political party of the candidate as a string, e.g., Democratic, Republican, Independent)
VOTES (number of votes received as an integer)

Ensure all headers are included in the output, even if some fields are blank, and encode the data properly (e.g., UTF-8)
to ensure compatibility. Validate that YEAR and VOTES are integers and handle any inconsistencies or special characters
in numeric fields gracefully.

If the image contains additional information not relevant to the specified fields, omit it unless it directly supports
these categories.

Special cases to handle:
- Presidential races do not have candidate names listed
- Presidential and Senate Races do not have congressional districts
- There should only be seven columns of output

Provide the output in a properly formatted CSV structure with commas as delimiters, enclosing text values containing
special characters or commas in quotes. DO NOT INCLUDE ANY OTHER INFORMATION BUT THE DATA IN THE OUTPUT.

Order the data based on the page it came from.
"""


# Custom prompt for handling special cases or specific years
def get_custom_prompt(year=None, race_type=None):
    """Generate a customized prompt for specific election years or race types.

    Args:
        year: Election year (int or string)
        race_type: Type of race (e.g., "Presidential", "Senate")

    Returns:
        str: Customized user prompt
    """
    prompt = USER_PROMPT

    if year:
        prompt += f"\n\nThis image is from the {year} election year. Please ensure this is reflected in the data."

    if race_type:
        if race_type.lower() == "presidential":
            prompt += "\n\nThis contains Presidential election data. Remember that Presidential races do not have candidate names listed and do not have congressional districts."
        elif race_type.lower() == "senate":
            prompt += "\n\nThis contains Senate election data. Remember that Senate races do not have congressional districts."
        elif race_type.lower() == "house":
            prompt += "\n\nThis contains House election data. Make sure to capture the congressional district numbers correctly."

    return prompt
