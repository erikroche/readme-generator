# readme-generator

This project is a README generator that uses AI to generate descriptive README files for projects. It analyzes the provided directory and includes relevant code snippets in the generated README.

## Usage

To run the project, use the following terminal command:

```
python generator.py <path>
```

Replace `<path>` with the path to the directory you want to analyze.

## Setup

Before running the project, make sure you have set up the necessary dependencies and environment. Here are the steps to follow:

1. Install Python 3.x.
2. Install the required Python packages by running the following command:

   ```
   pip install openai
   ```

3. Set up your OpenAI API key by exporting it as an environment variable:

   ```
   export OPENAI_KEY=<your-api-key>
   ```
   Optional: add your Open AI key as an environment variable on startup inside .zshrc/.bashrc for more information view [this](https://saturncloud.io/blog/setting-environment-variables-on-os-x/#setting-environment-variables-through-the-command-line) article

   Replace `<your-api-key>` with your actual OpenAI API key.

4. Customise the model to fit your needs:

    In the `prompt` variable inside the generate_readme function, adjust the `prompt` as well as `temperature` and `model` to your needs.

## Technologies Used

The readme-generator project utilizes the following technologies:

- Python: The programming language used to develop the generator.
- OpenAI API: The AI model used to generate the README content.

## Disclaimer

This README is generated with OpenAI using the [readme-generator repository](https://github.com/erikroche/readme-generator).