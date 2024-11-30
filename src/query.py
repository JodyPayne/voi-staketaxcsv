import logging
import time
from requests.exceptions import JSONDecodeError, Timeout, ConnectionError

# Define request types
REQUEST_TYPE_GET = "GET"
REQUEST_TYPE_POST = "POST"


def get_with_retries(session, url, params=None, headers=None, retries=4, backoff_factor=2, timeout=10):
    """
    Perform a GET request with retry logic.
    """
    return _make_request_with_retries(
        REQUEST_TYPE_GET, session, url, params, headers, retries, backoff_factor, timeout
    )


def post_with_retries(session, url, data=None, headers=None, retries=3, backoff_factor=1, timeout=10):
    """
    Perform a POST request with retry logic.
    """
    return _make_request_with_retries(
        REQUEST_TYPE_POST, session, url, data, headers, retries, backoff_factor, timeout
    )


def _make_request_with_retries(request_type, session, url, data, headers, retries, backoff_factor, timeout):
    """
    Generic function to handle GET and POST requests with retries.
    """
    for attempt in range(retries):
        try:
            if request_type == REQUEST_TYPE_GET:
                response = session.get(url, params=data, headers=headers, timeout=timeout)
            elif request_type == REQUEST_TYPE_POST:
                response = session.post(url, json=data, headers=headers, timeout=timeout)
            else:
                raise ValueError(f"Unsupported request type: {request_type}")

            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return parsed JSON response

        except (JSONDecodeError, Timeout, TimeoutError, ConnectionError) as e:
            logging.warning(f"Request attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                wait_time = backoff_factor * (2 ** attempt)
                logging.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logging.error("Max retries reached. Unable to get a valid response.")
                raise

        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            raise

    raise Exception("Failed to fetch data after maximum retries.")


def version_ge(version1, version2):
    """
    Compare two version strings (e.g., "2.1.0" >= "2.0.1").
    """
    version1_parts = [int(part) for part in version1.split('.')]
    version2_parts = [int(part) for part in version2.split('.')]

    # Normalize version parts length for accurate comparison
    max_length = max(len(version1_parts), len(version2_parts))
    version1_parts.extend([0] * (max_length - len(version1_parts)))
    version2_parts.extend([0] * (max_length - len(version2_parts)))

    return version1_parts >= version2_parts


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Query module loaded successfully.")
