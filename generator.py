import openai
import os
import sys
import logging
import argparse
import json

openai.api_key = os.getenv("OPENAI_KEY")

if openai.api_key is None:
    logging.error("OpenAI key is missing!")
    sys.exit(1)

def analyse_directory(path):
    if not os.path.exists(path):
        logging.error("Input path does not exist.")
        sys.exit(1)

    project_name = os.path.basename(path)
    return project_name

def generate_readme(project_name, directory_path):
    if not os.path.isdir(directory_path):
        raise ValueError("The provided path is not a directory.")

    files_in_directory = os.listdir(directory_path)

    code_file_extensions = [".py", ".java", ".js", ".html", ".css", "Dockerfile"]
    relevant_files = []
    
    for file in files_in_directory:
        file_extension = os.path.splitext(file)[1]
        if file_extension in code_file_extensions:
            relevant_files.append(file)

    # Read the contents of relevant files and add them to the prompt
    code_content = ""
    for file in relevant_files:
        file_path = os.path.join(directory_path, file)
        with open(file_path, "r") as file:
            code_content += f"\n\n## {file}\n\n"
            code_content += "```\n"
            code_content += file.read()
            code_content += "\n```\n"

    
    # Edit the below prompt to customise the output from the gpt model
    prompt = f"Provide a descriptive README for this project called {project_name}. It should be in .md format with headings and paragraphs. Do not include a sentance along the lines of 'this project is named ...' Just use the project name as a title in plain english not project-name. In the usage section, indlude any terminal commands necessary to run the project. Also in this section include any setup for the project. If relevant, include any interesting technologies used in a 'technologies used' section. Add a disclaimer at the end of the readme that this is generated with openai using the link to my repository: 'https://github.com/erikroche/readme-generator'."
    prompt += f"Here are the relavent parts of the project to use in the readme: {code_content}"

    completion = openai.ChatCompletion.create(
        # The model used here is a more expensive gpt-3.5-turbo-16k version which can handle 16,000 tokens rather than the basic 4096 tokens of gpt-turbo-3.5
        model="gpt-3.5-turbo-16k",
        # Temperature controls the creativity/randomness of the gpt model. As temperature approaches 0, the model will become deterministic and repetitive
        temperature = 0.3,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    output = str(completion.choices[0].message)
    output = json.loads(output)
    return output['content']

def write_to_readme(content, directory_path):
    if not os.path.isdir(directory_path):
        raise ValueError("The provided path is not a directory.")

    readme_path = os.path.join(directory_path, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write(content)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    parser = argparse.ArgumentParser(description="Generate README with code snippets.")
    parser.add_argument("path", type=str, help="Path to analyze")
    args = parser.parse_args()

    project_name = analyse_directory(args.path)
    
    readme_path = os.path.join(args.path, "README.md")
    if os.path.exists(readme_path):
        overwrite = input("A README already exists in this directory. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() == "y":
            description = generate_readme(project_name, args.path)
            write_to_readme(description, args.path)
            logging.info("README overwritten successfully.")
        else:
            logging.info("No changes were made.")
    else:
        logging.info("No README found. Generating one with AI...")
        description = generate_readme(project_name, args.path)
        write_to_readme(description, args.path)
        logging.info("README generated successfully.")

if __name__ == "__main__":
    main()