<p align="center">
    <img src="/.github/images/banner.svg" alt="">
</p>
<p align="center">
 <img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white" alt="Django">
 <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
 <img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
    <img src="https://img.shields.io/badge/daisyui-5A0EF8?style=for-the-badge&logo=daisyui&logoColor=white" alt="DaisyUI">
</p>

&nbsp;

<h1 align="center">※ Django Product Management App ※ </h1>

&nbsp;

## 🛠️ How to dev

### Requirements

* [Python](https://www.python.org/downloads/) >= 3.12
    ⤷ You can use [pyenv-win](https://github.com/pyenv-win/pyenv-win) to manage Python versions on Windows.

### Setting up the Development Environment

1. Run the `Pre-Setup` script

    ```bash
    python .\scripts\pre_setup.py
     
    ```

2. Activate the newly created`.venv` virtual environment

    * Windows

        * CMD

            ```bash
            C:\GitHub\DjangoProductManagementApp\.venv\Scripts\activate.bat
             
            ```

        * PowerShell

            ```bash
            C:\GitHub\DjangoProductManagementApp\.venv\Scripts\Activate.ps1
             
            ```

    * Unix/Linux

        ```bash
        source C:\GitHub\DjangoProductManagementApp\.venv/bin/activate
         
        ```

3. Run the `Setup` script

    ```bash
    pdm run setup
     
    ```

4. Start the development server by running:

    4.1. Django

    ```bash
    python src/manage.py runserver
     
    ```

    4.2. Tailwind

    ```bash
    python src/manage.py tailwind start
     
    ```

5. Open [http://localhost:8000/](http://localhost:8000/) in your browser to access the app

> [!NOTE]
> Closing Visual Studio Code will also close the npm dev server.
> [!IMPORTANT]
> Tailwind must be started in a separate terminal after the Django server is started. This is pretty annoying and could be improved with a script in the future.

&nbsp;

## Prod

> [!WARNING]
> Work in progress.
> `# TODO: Add prod deployment instructions`
