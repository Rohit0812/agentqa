# Document Question-Answering Agent with ReAct

A Python-based question-answering system that uses ReAct (Reasoning and Acting) to provide accurate answers from documents. The system supports multiple document formats and employs an agent-based approach for intelligent information retrieval and response generation.

## Features

- Document processing support for multiple formats (PDF, TXT)
- ReAct-based agent for intelligent question answering
- JSON-formatted responses
- Easy-to-use interface for batch question processing
- Flexible document handling through a dedicated Document class

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/document-qa-agent.git
cd document-qa-agent
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from utils.document import Document
from agentqa import ReActDocumentQA

# Initialize with a document
document_name = 'example.pdf'
document_type = 'PDF'

# Create document object
doc_obj = Document(doc_name=document_name, type=document_type)

# Initialize the QA agent
agent = ReActDocumentQA(doc_obj.document, index_name='example')

# Ask a question
question = "What is the main topic?"
answer = agent.process_question(question)
```

### Batch Processing

You can process multiple questions at once using the `run_app` function:

```python
questions = [
    "What is the main topic?",
    "Who are the key participants?"
]

result = run_app('document.pdf', 'PDF', questions)
print(result)
```

### Supported Document Types

- PDF (.pdf)
- Text files (.txt)

## Project Structure

```
document-qa-agent/
├── utils/
│   ├── document.py      # Document handling utilities
│   └── ...
├── agentqa.py          # ReAct agent implementation
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Example

```python
# Example with a text file
document_name = 'lily_story.txt'
document_type = 'TXT'
questions = [
    "What was the legend about the enchanted pond?",
    "What did Lily bring to the pond and why?"
]

result = run_app(document_name, document_type, questions)
print(result)

# Example with a PDF file
document_name = 'summit.pdf'
document_type = 'PDF'
questions = [
    "Who is Ahluvalia?",
]
result = run_app(document_name, document_type, questions)
print(result)
```

## Output Format

The system returns results in JSON format:

```json
{
    "questions": ["Question 1", "Question 2"],
    "answers": ["Answer 1", "Answer 2"]
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ReAct paper and implementation
- Contributors and maintainers
- Document processing libraries used in the project