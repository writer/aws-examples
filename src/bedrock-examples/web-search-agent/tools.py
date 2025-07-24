import json

from ddgs import DDGS


def web_search(query: str) -> str:
    """
    Function to research and collect more information to answer the query
    Args:
        query: The query that needs to be answered or more information needs to be collected.
    """
    try:
        results = DDGS().text(query=query, max_results=5)
        return "\n".join([json.dumps(result) for result in results])
    except Exception as e:
        return f"Failed to search. Error: {e}"


def call_function(tool_name, parameters):
    func = globals()[tool_name]
    output = func(**parameters)
    return output


tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "web_search",
                "description": "Fetch information about any query from the internet.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Query for which more information is required.",
                            }
                        },
                        "required": ["query"],
                    }
                },
            }
        }
    ],
    "toolChoice": {"auto": {}},
}
