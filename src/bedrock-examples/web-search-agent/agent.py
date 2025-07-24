from tools import call_function


class Agent:
    def __init__(
        self,
        bedrock_client,
        model_id,
        tool_config,
        system_prompt,
        messages=None,
        max_retries=3,
    ):
        if messages is None:
            messages = []

        self.bedrock_client = bedrock_client
        self.model_id = model_id
        self.messages = messages
        self.max_retires = max_retries
        self.tool_config = tool_config
        self.system_prompt = [{"text": system_prompt}]

    def call_converse_api_with_tools(self, messages):
        try:
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                system=self.system_prompt,
                messages=messages,
                toolConfig=self.tool_config,
            )
            return response

        except Exception as e:
            return {"error": str(e)}

    def handle_tool_use(self, func_name, func_params):
        allowed_tools = [tool["toolSpec"]["name"] for tool in self.tool_config["tools"]]

        if func_name in allowed_tools:
            results = call_function(func_name, func_params)
            return results

        raise Exception("An unexpected tool was used")

    def process_user_input(self, user_input):
        self.messages.append({"role": "user", "content": [{"text": user_input}]})
        print("Invoking LLM")

        response_message = self.call_converse_api_with_tools(
            messages=self.messages,
        )

        if "error" in response_message:
            return f"An error occurred: {response_message['error']}"

        # Add the intermediate output to the list of messages
        self.messages.append(response_message["output"]["message"])
        print("Received message from the LLM")

        function_calling = [
            content["toolUse"]
            for content in response_message["output"]["message"]["content"]
            if "toolUse" in content
        ]

        if function_calling:
            print(f"Function Calling - List of function calls : {function_calling}")
            tool_result_message = {"role": "user", "content": []}

            for function in function_calling:
                tool_name = function["name"]
                tool_args = function["input"] or {}

                print(f"Function calling - Calling Tool :{tool_name}(**{tool_args})")
                tool_response = self.handle_tool_use(tool_name, tool_args)

                print(f"Function calling - Got Tool Response: {tool_response}")
                tool_result_message["content"].append(
                    {
                        "toolResult": {
                            "toolUseId": function["toolUseId"],
                            "content": [{"text": tool_response}],
                        }
                    }
                )

            # Add the intermediate tool output to the list of messages
            self.messages.append(tool_result_message)

            print("Function calling - Calling LLM with Tool Result")
            response_message = self.call_converse_api_with_tools(messages=self.messages)

            if "error" in response_message:
                return f"An error occurred: {response_message['error']}"

            # Add the intermediate output to the list of messages
            self.messages.append(response_message["output"]["message"])

            print("Function calling - Received message from the LLM")
        return response_message["output"]["message"]["content"][0]["text"]

    def check_for_final_answer(self, user_input, ai_response):
        messages = []

        for message in self.messages:
            _messages = {"role": message["role"], "content": []}

            for _content in message["content"]:
                if "text" in _content.keys():
                    _messages["content"].append(_content)
                elif "toolResult" in _content.keys():
                    _messages["content"].extend(_content["toolResult"]["content"])

            messages.append(_messages)

        messages.append(
            {
                "role": "user",
                "content": [
                    {"text": f"User Query: {user_input}\nAI Response: {ai_response}"}
                ],
            }
        )

        try:
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                system=[
                    {
                        "text": "You are an expert at extracting the answer to user's query in the AI's response. "
                        "If you are not able to determine whether the query was answered then return: "
                        "Sorry cannot answer the query. Please try again. You have previous conversation "
                        "to provide you the context."
                    }
                ],
                messages=messages,
            )
            print(response)
            return response["output"]["message"]["content"][0]["text"]

        except Exception as e:
            return {"error": str(e)}

    def invoke(self, user_input):
        for i in range(self.max_retires):
            print(f"{'-'*15}Trial {i+1}{'-'*15}")
            response_text = self.process_user_input(user_input)

            if "FINAL ANSWER" in response_text:
                print(39 * "-")
                return response_text

            else:
                print("LLM Parser Invoked")
                llm_parser_output = self.check_for_final_answer(
                    user_input, response_text
                )
                print(f"LLM Parser Output:\n{llm_parser_output}")

                if "error" not in llm_parser_output:
                    print(39 * "-")
                    return llm_parser_output

        return "\n".join(
            [
                msg["content"][0].get("text", "<skipped> Tool Use <skipped>")
                for msg in self.messages
            ]
        )
