import json

# Project level libraries.
from utils.document import Document
from agentqa import ReActDocumentQA

def run_app(doc_name, doc_type, questions):
    # Create document object
    obj = Document(doc_name=doc_name, type=doc_type)
    document = obj.document
    
    # Initialize agent
    index_name = doc_name[:doc_name.find('.')]
    agent = ReActDocumentQA(document, index_name=index_name)
    
    answers = []
    for question in questions:
        answers.append(agent.process_question(question))
    
    result = json.dumps({
        'questions': questions,
        'answers': answers
    })
    return result

if __name__ == "__main__":
    
    #document_name = 'lily_story.txt'
    #document_type = 'TXT'
    #questions = [
    #    "What Lily did one morning?",
    #    "What did Lily bring to the pond and why?"
    #]
    
    document_name = 'story.pdf'
    document_type = 'PDF'
    questions = [
        "Where did Clara live?",
        "What Clara and Leo did together?",
        "Tell me about adventure of Clara and Leo."
    ]
    result = run_app(document_name, document_type, questions)

    print("-----------------------------------")
    print("\n Final Result:", result)