import os
import traceback
from dotenv import load_dotenv
from atlassian import Confluence
import requests

# Load environment variables
load_dotenv()
confluence_username = os.getenv('CONFLUENCE_USERNAME')
confluence_token = os.getenv('ATLASSIAN_TOKEN')

if not confluence_username:
    raise ValueError("CONFLUENCE_USERNAME environment variable is not set")
if not confluence_token:
    raise ValueError("ATLASSIAN_TOKEN environment variable is not set")

# Test URL
TEST_URL = "https://schrodinger-sandbox.atlassian.net/wiki/spaces/ITLC/pages/196542469/IT+Knowledge+Base"

def extract_page_id_from_url(url):
    """Extract page ID from Confluence URL."""
    import re
    match = re.search(r'/pages/(\d+)/', url)
    if match:
        return match.group(1)
    return None

def test_confluence_access():
    try:
        # Initialize Confluence client
        confluence = Confluence(
            url='https://schrodinger-sandbox.atlassian.net',
            username=confluence_username,
            password=confluence_token
        )
        
        print("\nTesting Confluence Access:")
        print("---------------------------")
        
        # Test 1: Basic Connection
        print("\n1. Testing basic connection...")
        page_id = extract_page_id_from_url(TEST_URL)
        if not page_id:
            raise ValueError("Could not extract page ID from URL")
        print("✅ Successfully parsed page ID:", page_id)
        
        # Test 2: Page Access
        print("\n2. Testing page access...")
        page = confluence.get_page_by_id(page_id, expand='body.storage,version')
        print("✅ Successfully accessed page:", page['title'])
        
        # Test 3: Content Access
        print("\n3. Testing content access...")
        content = page['body']['storage']['value']
        print("✅ Successfully retrieved page content")
        print("\nPage Details:")
        print(f"Title: {page.get('title', 'N/A')}")
        print(f"ID: {page.get('id', 'N/A')}")
        if 'version' in page:
            print(f"Version: {page['version'].get('number', 'N/A')}")
        if 'space' in page:
            print(f"Space Key: {page['space'].get('key', 'N/A')}")
            
    except requests.exceptions.HTTPError as e:
        print("\n❌ API Permission Error:")
        print("Authentication failed. Please verify:")
        print("- Username is correct")
        print("- API token is valid")
        print("- API token has the required permissions")
        print("\nFull error details:")
        traceback.print_exc()
    except Exception as e:
        print("\n❌ Error:")
        traceback.print_exc()

if __name__ == "__main__":
    test_confluence_access()
