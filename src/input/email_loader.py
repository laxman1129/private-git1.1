from typing import List
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredEmailLoader  # for loading emails


# custom document loader
class EmailLoader(UnstructuredEmailLoader):
    """
    Wrapper to fallback to text/plain whren the default loader fails
    """

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if "text/html content not found in email" in str(e):
                    self.unstructured_kwargs["content_source"] = "text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            raise type(e)(f"{self.file_path} : {e}")
        return doc
