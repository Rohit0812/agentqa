import os
from typing import Tuple
from openai import OpenAI

# Project level imports.
from utils.searcher import EntitySearcher
from utils.prompts import instruction_prompt

from dotenv import load_dotenv
load_dotenv()

class ReActDocumentQA:
    def __init__(self, document: str, index_name: str, model="gpt-4o-mini", max_iterations=5):
        """
        Initialize the ReAct agent with a document and OpenAI configuration.
        
        Args:
            document (str): The input document text
            index_name (str): Index name for the document.
            model (str): OpenAI model to use (default: gpt-4-turbo-preview)
            max_iterations (int): Maximum number of reasoning iterations
        """
        self.__entity_searcher = EntitySearcher(index_path=index_name)
        
        # Prepares index of document
        self.__entity_searcher.prepare_index(document)

        self.__kw_lookup = {}
        self.__model = model
        self.__max_iterations = max_iterations
        self.__client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def __search(self, keywords: str) -> str:
        """
        Search the document for relevant keywords and return 1st paragraph.
        """
        results = self.__entity_searcher.search_entity(keywords)
        
        if not results:
            return "No Results"
        
        self.__kw_lookup[keywords] = {
            'paragraphs': [text for text, distance in results],
            'cursor': 0
            }
        return self.__kw_lookup[keywords]['paragraphs'][0]

    def __lookup(self, keywords: str) -> str:
        """
        Return next paragraph.
        """
        paragraphs = self.__kw_lookup[keywords]['paragraphs']
        cursor = self.__kw_lookup[keywords]['cursor']
        cursor += 1
        
        if cursor == len(paragraphs):
            return "No Results"
        
        self.__kw_lookup[keywords] = {
            'paragraphs': paragraphs,
            'cursor': cursor
        }
        return paragraphs[cursor]
        
    def __execute_action(self, action: str) -> Tuple:
        """
        Execute a single action and return its result.
        """
        action, param = action[:action.find('[')], action[action.find('[')+1:-1]
        if action == "Search": # Search relevant portions of a doc and return 1st paragraph.
            result = self.__search(param)
            return result, False
        if action == "Lookup": # Returns next paragraph.
            try:
                result = self.__lookup(param)
            except:
                print("LLM didn't follow instruction...")
                # In case, llm defy prompt instruction.
                result = self.__search(param)
            return result, False
        if action == "Finish":
            return param, True
        
        # If llm fails to generate Search[], Lookup[] or Finish[]
        print("LLM didn't follow instruction.")
        return "", False


    def __thought_action(self, content: str, stop: str) -> str:
        """
        Plan the next action based on the content emitted so far.
        """
        try:
            response = self.__client.chat.completions.create(
                model=self.__model,
                messages=[
                    {"role": "system", "content": content},
                ],
                temperature=0,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=stop,
            )
            return response.choices[0].message.content
        except Exception as e:
            print("Exception happened!!!")
            return ""

    def process_question(self, question: str, print_prompt: bool = False) -> str:
        """
        Process a question using iterative reasoning steps.
        
        Args:
            question (str): The question to answer
            
        Returns:
            str: The reasoning process and final answer
        """
        prompt = f"{instruction_prompt}Question: {question}\n"
        
        answer, success_flag = "", False 
        iteration = 0
        while iteration < self.__max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Plan next thought and action
            message = f"{prompt}Thought {iteration}:"
            stop = [f"\nObservation {iteration}:"]
            thought_action = self.__thought_action(message, stop)
            try:
                thought, action = thought_action.strip().split(f"\nAction {iteration}: ")
            except:
                thought = thought_action.strip().split('\n')[0]
                message = f"{prompt}Thought {iteration}: {thought}\nAction {iteration}:"
                action = self.__thought_action(message, stop=[f"\n"]).strip()
            
            # Execute the planned thought and action
            observation, done = self.__execute_action(action)
            step_content = f"Thought {iteration}: {thought}\nAction {iteration}: {action}\nObservation {iteration}: {observation}\n"
            prompt += step_content

            print("step content:\n", step_content)
            
            # Check if we should finish
            if done:
                answer = observation
                success_flag = True    
                break
        
        if print_prompt:
            print("prompt at the end", prompt)
        
        # If we hit max iterations without a final answer, generate one
        if not success_flag:
            answer = "Data Not Available"
        
        return answer
