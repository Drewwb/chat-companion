import unittest
import re
from unittest.mock import patch, MagicMock
from PDFBot import get_bot_response

class TestChatbot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up mock data
        cls.mock_docs = [
            MagicMock(page_content="Mikes dogs name is Blue", metadata={"title": "doc1"}),
            MagicMock(page_content="Blakes coffee cup is the color red", metadata={"title": "doc2"}),
            MagicMock(page_content="Drew types on a keyboard in his free time", metadata={"title": "doc3"})
        ]

    def test_get_bot_response_with_dogs_question(self):
        # Test sending a message about dogs
        with patch('PDFreader.document_search.similarity_search') as mock_similarity_search:
            mock_similarity_search.return_value = self.mock_docs
            response = get_bot_response("What is Mikes dogs name?")

        # Predefined keyword to search for
        keyword = "blue"

        # Check if keyword is present in the response
        self.assertTrue(self.is_keyword_in_response(keyword, response))

    def test_get_bot_response_with_coffee_question(self):
        # Test sending a message about coffee cup
        with patch('PDFreader.document_search.similarity_search') as mock_similarity_search:
            mock_similarity_search.return_value = self.mock_docs
            response = get_bot_response("What color is Blakes coffee cup?")

        # Predefined keyword to search for
        keyword = "red"

        # Check if keyword is present in the response
        self.assertTrue(self.is_keyword_in_response(keyword, response))

    def test_get_bot_response_with_typing_question(self):
        # Test sending a message about typing
        with patch('PDFreader.document_search.similarity_search') as mock_similarity_search:
            mock_similarity_search.return_value = self.mock_docs
            response = get_bot_response("What does Drew do in his free time?")

        # Predefined keyword to search for
        keyword = "types"

        # Check if keyword is present in the response
        self.assertTrue(self.is_keyword_in_response(keyword, response))

    # Get rid of edge cases such as punctuation and periods
    def is_keyword_in_response(self, keyword, response):
        # Preprocess response and keyword (convert to lowercase and remove punctuation)
        response_processed = re.sub(r'[^\w\s]', '', response.lower())
        keyword_processed = re.sub(r'[^\w\s]', '', keyword.lower())
        # Check if keyword is present in the processed response
        return keyword_processed in response_processed

if __name__ == '__main__':
    unittest.main()