
from __future__ import annotations
import logging
import argparse
from pathlib import Path
import re
from Ai.AiModelIf import Prompt
from Context import Context
from ContextIf import ContextIf

# Regular expression to match python code blocks in a response
PYTHON_RESPONSE = re.compile(r'```python(.*?)```$', re.DOTALL)


def SYSTEM_PROMPT() -> Prompt:
    """
    Generates a system prompt used to inform the AI model about the role it should play.

    Returns:
        Prompt: A dictionary representing the system prompt with role and content.
    """
    return {
        "role": "system",
        "content": """
                Welcome! As a software architect and senior Python developer, I'm here to support you with my extensive knowledge and expertise. Here are some of the things I can assist you with:

                - Capable of explaining complex Python constructs in a clear and understandable manner for fellow Python enthusiasts.
                - Adding Types and Generics to operations and classes to ensure type binding as much as possible

                Feel free to ask me anything related to Python development, software architecture, or documentation. Let's get started!
            """}


def COMMENT_PYTHON(pythonFilePath: Path) -> Prompt:
    """
    Generates a user prompt to request analysis and commenting of a Python file.

    Args:
        pythonFilePath (Path): Path to the Python file to be analyzed.

    Returns:
        Prompt: A dictionary representing the user prompt with role and content.
    """
    return {
        "role": "user",
        "content": f"""
            Hello python expert,

            I need you to analyze a python file and add the necessary comments to make it more understandable. Please follow these instructions:

            1. Identify the purpose of the python class and add a class description as pythonDoc.
            2. Determine the purpose of each method and its parameters, then add pythonDoc to each method accordingly.
            3. Add type annotations and generics to implement type binding as much as possible
            4. Do NOT modify the existing code; only add comments.

            The python file to be analyzed is:

            ----start python file----
            {pythonFilePath.read_text()}
            ----end python file----

            Please return only the python code with comments. Ensure the following:
            - The returned code must be compilable with the python compiler.
            - Do not include any extraneous text such as 'Here is the commented python code.'
            - Do not return '```python' at the beginning or end of your response, as it will interfere with the python compiler.

            Thank you!
        """}


class CommentPythonFile:
    """
    A class to handle the commenting of a Python file using an AI model to generate comments.

    Attributes:
        path (Path): The path to the Python file to be commented.
        context (ContextIf): The context interface for interaction with the AI model.
    """

    def __init__(self, path: Path, context: ContextIf):
        """
        Initializes a CommentPythonFile object.

        Args:
            path (Path): The path to the Python file to be commented.
            context (ContextIf): The context interface for interaction with the AI model.
        """
        self.path = path
        self.context = context

    def comment(self) -> str:
        """
        Generates comments for the Python file by interacting with the AI model.

        Returns:
            str: The content of the commented Python file as a string.
        """
        aiChat = self.context.createChat()
        aiChat.append(SYSTEM_PROMPT())

        response = aiChat.chat(COMMENT_PYTHON(self.path))

        content = response["prompt"]["content"]

        logger.info("Total tokens: %d", response["totalTokens"])

        match = PYTHON_RESPONSE.search(content)
        if match:
            return match.group(1)
        else:
            return content


# Logger setup for the module
logger = logging.getLogger(__name__)


def main(arguments: argparse.Namespace) -> None:
    """
    Main function to handle the overall process of commenting a Python file.

    Args:
        arguments (argparse.Namespace): Command-line arguments parsed with argparse.
    """
    logging.basicConfig(level=logging.INFO)

    context = Context('gpt-4o')
    # context = Context('togethercomputer/CodeLlama-34b-Python')

    app = CommentPythonFile(Path(arguments.file), context)
    commentedFile = app.comment()

    Path(arguments.file).write_text(commentedFile, "utf-8")


if __name__ == '__main__':
    # Setup argument parser for command-line interface
    parser = argparse.ArgumentParser(description="Comment python files")
    parser.add_argument("--file", "-f", help="Python file to be commented", type=str, required=True)
    args = parser.parse_args()

    main(args)
