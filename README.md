# OAuth Application for Session Management

This is an OAuth application that allows you to save the session on cookies and manage it with a middleware. It provides login functionality using Google OAuth.

## Table of Contents
- [Development](#development)
- [Usage](#usage)
- [Configuration](#configuration)
- [Containerization](#containerization)
- [Contributing](#contributing)
- [License](#license)

## Development  <a name="development"></a>

To run the project for development I provide you the file `local.yml`.

First, you need to build the project with the following command:
```shell
docker-compose -f local.yml build
```

Then, run a container using the following command:
```shell
docker-compose -f local.yml up
```

## Usage <a name="usage"></a>

To use this application, follow these steps:

1. Set up the necessary environment variables in a `.env` file or provide them directly to your environment.
2. Update the `Settings` class in `app/settings.py` with your desired settings.
3. Start the application by running `python main.py`.

## Configuration <a name="configuration"></a>

The application uses a `Settings` class in `app/settings.py` for configuration. The available configuration options are as follows:

| Option                              | Description                                                                 |
| ----------------------------------- | --------------------------------------------------------------------------- |
| APP_NAME                            | The name of the application                                                 |
| HOST                                | The host URL of your application                                            |
| SECRET_KEY                          | The secret key used for session encryption                                  |
| ENVIRONMENT                          | The environment in which the application is running (default: development)   |
| ACCESS_TOKEN_EXPIRATION_MINUTES     | The expiration time in minutes for access tokens (default: 1440)             |
| REFRESH_TOKEN_EXPIRATION_MINUTES    | The expiration time in minutes for refresh tokens (default: 43200)           |
| OBJECT_STORAGE_ACCESS_KEY           | Access key for object storage                                               |
| OBJECT_STORAGE_SECRET_KEY           | Secret key for object storage                                               |
| OBJECT_STORAGE_ENDPOINT_PUBLIC      | Public endpoint for object storage                                          |
| OBJECT_STORAGE_ENDPOINT_PRIVATE     | Private endpoint for object storage                                         |
| OBJECT_STORAGE_REGION               | Region for object storage                                                   |
| GOOGLE_ID_CLIENT                    | Client ID for Google OAuth                                                  |
| GOOGLE_SECRET_CLIENT                | Client secret for Google OAuth                                              |
| POSTGRES_USER                       | Username for PostgreSQL database                                            |
| POSTGRES_PASSWORD                   | Password for PostgreSQL database                                            |
| POSTGRES_HOST                       | Hostname of the PostgreSQL server                                           |
| POSTGRES_DB                         | Name of the PostgreSQL database                                             |

## Containerization <a name="containerization"></a>

To containerize the application, you can use the provided `Containerfile`. Build the Docker image using the following command:

```shell
docker build -t oauth-app .
```

Then, run a container using the following command:

```shell
docker run -p 3000:3000 oauth-app \
-e POSTGRES_PASSWORD='***' \
-e POSTGRES_USER='***' \
-e POSTGRES_DB='***' \
-e POSTGRES_PORT="5432" \
-e PORGRES_HOST="db_url"
```

## Contributing <a name="contributing"></a>

Contributions are welcome! If you have any improvements or bug fixes, feel free to submit a pull request.

## License <a name="license"></a>

This project is licensed under the [MIT License](LICENSE).
