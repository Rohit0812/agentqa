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

3. Store the OpenAPI Chat Model keys in the ```.env```

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

## Example

```python
# Example with a text file
document_name = 'lily_story.txt'
document_type = 'TXT'
questions = [
    "What Lily did one morning?",
    "What did Lily bring to the pond and why?"
]

result = run_app(document_name, document_type, questions)
print(result)

# Example with a PDF file
document_name = 'story.pdf'
document_type = 'PDF'
questions = [
        "Where did Clara live?",
        "What Clara and Leo did together?",
        "Tell me about adventure of Clara and Leo."
      ] 
result = run_app(document_name, document_type, questions)
```

## Output Format

The system returns results in JSON format:

```json
{
    "questions": ["Question 1", "Question 2"],
    "answers": ["Answer 1", "Answer 2"]
}
```

## Important Notes

1. Performance Dependencies:
   - The agent's performance is heavily dependent on prompt engineering and the language models used
   - Current implementation uses basic prompts and lower-version models which may not be optimal
   - Results can be improved significantly with better prompt engineering and more advanced language models

2. Document Processing Limitations:
   - The document searcher's performance varies based on document complexity
   - Current implementation works best with simple PDF documents where paragraph segmentation is straightforward
   - For complex documents, proper pre-processing and segmentation should be implemented
   - Document indexing should be optimized for better retrieval performance

## Scope for Improvement

1. Document Processing:
   - Implement advanced document segmentation techniques
   - Add support for more document formats
   - Develop better indexing mechanisms for complex documents
   - Optimize paragraph extraction and processing

2. Agent Enhancement:
   - Optimize prompt engineering for better question understanding and answer generation
   - Upgrade to more advanced language models
   - Implement better context management for follow-up questions
   - Add support for multi-document querying

3. Performance Optimization:
   - Implement caching mechanisms for frequently accessed documents
   - Optimize document search algorithms
   - Add parallel processing for batch questions
   - Implement better error handling and recovery mechanisms

4. User Interface:
   - Add a web interface for easier interaction
   - Implement real-time processing feedback
   - Add visualization for document segmentation
   - Develop better result formatting options

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- ReAct paper and implementation (https://arxiv.org/pdf/2210.03629)
- Document processing libraries used in the project
