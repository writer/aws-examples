def get_agent_id_by_name(bedrock_client, name):
    try:
        list_agent = bedrock_client.list_agents().get("agentSummaries", [])
        agent_id_list = [
            agent.get("agentId")
            for agent in list_agent
            if agent.get("agentName", "") == name
        ]

        if not agent_id_list:
            raise ValueError(f"Agent with name '{name}' not found")

        if len(agent_id_list) > 1:
            raise ValueError(f"Search with by name '{name}' returned multiple agents")

        return agent_id_list[0]
    except Exception as e:
        print("Error fetching agent id by name:", e)


def get_action_group_id_by_name(bedrock_client, agent_id, name):
    try:
        list_action_group = bedrock_client.list_agent_action_groups(
            agentId=agent_id,
            agentVersion="1",
        ).get("actionGroupSummaries", [])

        action_group_id_list = [
            agent.get("actionGroupId")
            for agent in list_action_group
            if agent.get("actionGroupName", "") == name
        ]

        if not action_group_id_list:
            raise ValueError(f"Action group with name '{name}' not found")

        if len(action_group_id_list) > 1:
            raise ValueError(
                f"Search with by name '{name}' returned multiple action groups"
            )

        return action_group_id_list[0]
    except Exception as e:
        print("Error fetching group id by name:", e)


def get_agent_alias_id_by_name(bedrock_client, agent_id, name):
    try:
        response = bedrock_client.list_agent_aliases(
            agentId=agent_id,
        )

        agent_alias_id_list = [
            agent.get("agentAliasId")
            for agent in response.get("agentAliasSummaries", [])
            if agent.get("agentAliasName", "") == name
        ]

        if not agent_alias_id_list:
            raise ValueError(f"Alias with name '{name}' not found")

        if len(agent_alias_id_list) > 1:
            raise ValueError(f"Search with by name '{name}' returned multiple aliases")

        return agent_alias_id_list[0]
    except Exception as e:
        print("Error fetching agent alias id by name:", e)
