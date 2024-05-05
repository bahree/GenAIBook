try:
    response = openai_client.chat_completions(
        messages=message_list,
        openai_settings=ChatCompletionsSettings(
            **bot_config["approach_classifier"]["openai_settings"]
        ),
        api_base=f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com",
        api_key=AZURE_OPENAI_KEY,
    )
    except openai.error.InvalidRequestError as e:
        self.logger.error(f"AOAI API Error: {e}", exc_info=True)
        raise e

    classification_response: str = response["choices"][0]["message"]["content"]
    self.log_aoai_response_details(
        f'Classification Prompt:{history[-1]["utterance"]}',
        f"Response: {classification_response}",
        response,
    )
    if classification_response == "1":
        return ApproachType.structured
    elif classification_response == "2":
        return ApproachType.unstructured
    elif classification_response == "3":
        return ApproachType.chit_chat
    elif classification_response == "4":
        # Continuation: Return last question type from history if it exists
        ...
        else:
            return ApproachType.unstructured
    elif classification_response == "5":
        # User has typed something that violates guardrails
        return ApproachType.inappropriate
    else:
        return ApproachType.unstructured
        
 
