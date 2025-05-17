# DjangoProductManagementApp

&nbsp;

## Requirements

- Python >= 3.12

&nbsp;

## Dev

1. **(Optional) Create a virtual environment**:

    ```bash
    python -m venv .venv
    ```

    1. Windows

        ```bash
        .venv\Scripts\activate
        ```

    2. Linux

        ```bash
        source .venv/bin/activate  
        ```

2. Install PDM:

    ```bash
    pip install pdm
    ```

3. Install dependencies:

    ```bash
    pdm install dev
    ```

4. Database setup

    ```python
    pdm run python src/manage.py makemigrations
    pdm run python src/manage.py migrate

    ```

5. Run the development server: `pdm run backend:dev`

&nbsp;

## Prod

TODO
