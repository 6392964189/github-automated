import os
import requests
import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

def fetch_user_repositories(github_url):
    username = github_url.split('/')[-1]

    # Fetch user's repositories using GitHub API
    api_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(api_url)
    repositories = response.json()


    return [repo['name'] for repo in repositories]

# Preprocess code in repositories
def preprocess_code(code):
    # Add your preprocessing logic here
    # You can handle large Jupyter notebooks, package files, etc.
    # Make sure the processed code fits within GPT's token limits
    processed_code = code

    return processed_code

# Evaluate code complexity using GPT
def evaluate_complexity(code):
    # Define your prompt engineering logic here
    # You can craft prompts to evaluate code complexity
    prompt = f"What is the complexity of this code?\nCode:\n{code}"
    
    # Generate response using GPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    # Return the generated response
    return response.choices[0].text.strip()

# Identify the most technically complex repository
def identify_most_complex_repository(github_url):
    # Fetch user's repositories
    repositories = fetch_user_repositories(github_url)

    # Variables to track the most complex repository
    most_complex_repo = None
    max_complexity_score = -1

    # Iterate over repositories
    for repo in repositories:
        # Fetch code from repository
        code = fetch_code_from_repository(github_url, repo)

        # Preprocess code
        processed_code = preprocess_code(code)

        # Evaluate code complexity
        complexity_score = evaluate_complexity(processed_code)

        # Track the most complex repository
        if complexity_score > max_complexity_score:
            max_complexity_score = complexity_score
            most_complex_repo = repo

    return most_complex_repo

# Fetch code from repository
def fetch_code_from_repository(github_url, repository):
    # Build the raw URL to fetch the code from
    raw_url = f"{github_url.rstrip('/')}/raw/master/{repository}"

    # Fetch code using requests library
    response = requests.get(raw_url)
    code = response.text

    return code


def main():
    # Get user's GitHub URL
    github_url = input("Enter GitHub user URL: ")

    # Identify the most technically complex repository
    most_complex_repo = identify_most_complex_repository(github_url)

    # Print the result
    print(f"The most complex repository is: {most_complex_repo}")

# Run the main function
if __name__ == '__main__':
    main()
