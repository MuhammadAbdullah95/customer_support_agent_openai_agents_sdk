from QAsystem.retrievelgeneration import get_result
from agents.tool import function_tool

@function_tool
def FAQs_retreivel(query: str):
    """
    Retreive FAQs answers from the hotel's vector database
    Args:
        query (str): Query of the user
    """

    answer = get_result(query)
    return answer