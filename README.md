# GithubRepoAPI
A simple FastAPI application for demo GitHub repositories API with PostgreSQL integration.

## Running Integration Tests

This project uses `pytest` for integration testing. Follow these steps to run the tests:

1. Navigate to the project directory:
    ```bash
    cd GithubRepoAPI
    ```

2. Run the tests with `pytest`:
    ```bash
    pytest tests/
    ```

This will run all the test cases located in the `tests/` directory. `pytest` will automatically discover and run all test cases in this directory that follow its naming conventions.


## Running with Docker Compose


1. Clone the repository:
    ```
    git clone https://github.com/weiczhu/GithubRepoAPI.git
    ```
2. Navigate to the project directory:
    ```
    cd GithubRepoAPI
    ```
3. Build and start the Docker containers:
    ```
    docker-compose up --build
    ```
The application should now be running at `http://localhost:8000`.


## Testing the Project

You can test the project by making a `GET` request to the `/repositories/{owner}/{repo}` endpoint. For example, to get the details of the `Hello-World` repository owned by `octocat`, you can use the following `curl` command:

    ```bash
    curl http://0.0.0.0:8000/repositories/octocat/Hello-World
    ```

This should return a JSON response with the details of the Hello-World repository. Here's an example of what the response might look like:
    ```json
    {
    "fullName": "octocat/Hello-World",
    "description": "My first repository on GitHub!",
    "cloneUrl": "https://github.com/octocat/Hello-World.git",
    "stars": 2516,
    "createdAt": "2011-01-26T19:01:12"
    }
    ```

## Stopping the Project

To stop the Docker containers, use the following command:
    ```
    docker-compose down
    ```