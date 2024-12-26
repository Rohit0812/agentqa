import os
import PyPDF2
from dotenv import load_dotenv
load_dotenv()

class Document:
    doc_path = os.environ['DOC_PATH']

    def __init__(self, doc=None, doc_name=None, type=None):
        self.doc_name = doc_name
        self.__doc = doc
        self.__type = type

        self._process_doc()

    def _get_text(self):
        txt_path = os.path.join(self.doc_path, self.doc_name)
        with open(txt_path, "r") as file:  
            content = file.read()  
        self.__doc = content

    def _extract_text_from_pdf(self):
        pdf_path = os.path.join(self.doc_path, self.doc_name)
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        self.__doc = text
    
    def _preprocess_text(self):
        import re
        """
        Preprocess text to merge lines that belong to the same paragraph.
        """
        # Replace single newlines with a space if the line does not end with punctuation
        self.__doc = re.sub(r"(?<![.!?])\n(?!\n)", " ", self.__doc)

    def _process_doc(self):
        if not self.__type:
            self._preprocess_text
        elif self.__type.lower() == 'txt':
            self._get_text()
            self._preprocess_text()
        elif self.__type.lower() == 'pdf':
            self._extract_text_from_pdf()
            self._preprocess_text()
        else:
            raise AssertionError("Wrong Document Type.")
        
    @property
    def document(self):
        return self.__doc

if __name__ == "__main__":
    obj = Document(doc_name="lion_story.txt", type='TXT')
    obj.document