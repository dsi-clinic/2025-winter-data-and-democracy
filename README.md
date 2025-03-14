# 2025-winter-data-and-democracy

## Project Background

US historical election results can be found in a set of PDF documents [at this link](https://history.house.gov/Institution/Election-Statistics/Election-Statistics/) though there is no comprehensive results repository in a machine readable format.

The purpose of this project is to test modern tools on this data to create a comprehensive results repository. Specifically we wish to test Claude and OpenAI's APIs on this image data to build a dataset. If there are other API based systems for testing than they can be added to the list.

## Project Goals

The following are project goals:
1. Write code which analyzes, parses and OCRs the images from the 1920-1998. This should 
2. Once the images are in table format, checking should be done to verify that integrity of the data. Specifically:
   1. There are totals in many of the datasets. These can be used as checksums to verify the scanning was accurate.
   2. Numbers should also have guardrails on them. For example, all vote totals should be integers. 
   3. Other tests and checks should be developed by the group working on this project.
3. The outcome should be a set of _standard_ csv files. The data definition of this should look something like:

```sql
state char(2),
year int,
race_type varchar(12),
congressional_district int,
candidate_name varchar(100),
candidate_party varchar(100),
votes int
```

Where `race_type` should be Senate, HR or Presidential (if there are others listed they should be included). `congressional_district` should only exist when appropriate. Note that there may need to be additional information added to the schema, the purpose of this is to give you a sense of what the schema should roughly look lke.

4. Finally the scripts need to run from top-to-bottom to generate the results. This should _not_ be a set of jupyter notebooks, but a set of python scripts.

## Tasks for the first week

To complete this task we will need a few different pieces of code:

1. Python functions which download the pdf files and put them into a temp directory (such as /data/temp). Note that they should _not_ be committed into the repo as they are quite large, they should be downloaded
2. Read over the PDF documents.
3. Become familiar with the claude API and figure out how to send images to it. You have a claude API key in the slack channel (this should _NOT_ be committed to the repo. If the API Key ends up in the repo it will negatively impact your entire team's grade).

## Usage

### Docker

### Docker & Make

We use `docker` and `make` to run our code. There are three built-in `make` commands:

* `make build-only`: This will build the image only. It is useful for testing and making changes to the Dockerfile.
* `make run-notebooks`: This will run a jupyter server which also mounts the current directory into `\program`.
* `make run-interactive`: This will create a container (with the current directory mounted as `\program`) and loads an interactive session. 

The file `Makefile` contains information about about the specific commands that are run using when calling each `make` statement.

### Developing inside a container with VS Code

If you prefer to develop inside a container with VS Code then do the following steps. Note that this works with both regular scripts as well as jupyter notebooks.

1. Open the repository in VS Code
2. At the bottom right a window may appear that says `Folder contains a Dev Container configuration file...`. If it does, select, `Reopen in Container` and you are done. Otherwise proceed to next step. 
3. Click the blue or green rectangle in the bottom left of VS code (should say something like `><` or `>< WSL`). Options should appear in the top center of your screen. Select `Reopen in Container`.




## Style
We use [`ruff`](https://docs.astral.sh/ruff/) to enforce style standards and grade code quality. This is an automated code checker that looks for specific issues in the code that need to be fixed to make it readable and consistent with common standards. `ruff` is run before each commit via [`pre-commit`](https://pre-commit.com/). If it fails, the commit will be blocked and the user will be shown what needs to be changed.

To check for errors locally, first ensure that `pre-commit` is installed by running `pip install pre-commit` followed by `pre-commit install`. Once installed, check for errors by running:
```
pre-commit run --all-files
```

## Repository Structure

### utils
Project python code

### notebooks
Contains short, clean notebooks to demonstrate analysis.

### data

Contains details of acquiring all raw data used in repository. If data is small (<50MB) then it is okay to save it to the repo, making sure to clearly document how to the data is obtained.

If the data is larger than 50MB than you should not add it to the repo and instead document how to get the data in the README.md file in the data directory. 

This [README.md file](/data/README.md) should be kept up to date.

### output
Should contain work product generated by the analysis. Keep in mind that results should (generally) be excluded from the git repository.
