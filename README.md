# 2025-winter-data-and-democracy

## Project Background

US historical election results can be found in a set of PDF documents [at this link](https://history.house.gov/Institution/Election-Statistics/Election-Statistics/) though there is no comprehensive results repository in a machine readable format.

The purpose of this project is to test modern tools on this data to create a comprehensive results repository. Specifically we wish to test Claude and OpenAI's APIs on this image data to build a dataset. If there are other API based systems for testing than they can be added to the list.

## Project Goals Spring 2025

The following are project goals:

1. Building on the work from last quarter there are three priorites:
   1. The [open elections project](http://openelections.net/) contains information about historical election results. We want to add our results for our elections to this repository.
   2. Read over their guidelines for contributing and put together a plan for how our data has to be changed to be committed.
   3. Add some "connection" code which creates a set of specific CSV files that conform to the speficiations they require.
   4. Each team member identify 2 statues that they will manage individiually. Make sure that the states chosen are relatively active github repos on the web page.
   5. Using the connection code generate data and follow the open elections instructions for how to contribute, making sure to be professional in your communication and following their process step-by-step. **Note that this is being done under _your personal_ github, so if you behave poorly it will follow your account**.
   6. Approval can take some time, so once multiple states have been approved, continue until all states and data are completed.
2. Build a Jekyll github pages website for this data. This needs to have the following:
   1. Automated github action pipeline for creating the github page on any push to `main` branch.
   2. This should be a professional looking web page
   3. There should be links to the data in a "data" section
   4. There should be a well-written description of the code and how it works.
   5. There should be an "about" page which has information on everyone (including people from last quarter) who have contributed. Make sure to only include information that you are comfortable sharing.
3. Update this readme. This is going to be a public web site so _every_ piece of code, _every_ readme, etc. needs to be well written, up-to-date and appropriate.
   1. This includes removing things like references to the "quarter's to do list", etc.
   2. Make sure that everything runs via docker and the docker commands are up to date.
3. Redo the anaysis using openAI or another paid API to verify the quality of the results.
   1. If there is time, create a parallel data pipeline that uses another API to validate the results of Claude's OCR.

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
