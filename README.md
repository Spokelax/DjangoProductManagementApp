<p align="center">
    <img src="/.github/images/banner.svg" alt="">
</p>
<p align="center">
 <img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white" alt="Django">
 <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
 <img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
    <img src="https://img.shields.io/badge/daisyui-5A0EF8?style=for-the-badge&logo=daisyui&logoColor=white" alt="DaisyUI">
</p>
<p align="center">
    <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
    <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
</p>

&nbsp;

<h1 align="center">※ Django Product Management App ※ </h1>

&nbsp;

## 🛠️ How to dev

### Requirements

* [Python](https://www.python.org/downloads/) >= 3.12
    ⤷ You can use [pyenv-win](https://github.com/pyenv-win/pyenv-win) to manage Python versions on Windows.
* [NodeJS](https://nodejs.org/en/download)
* [NPM](https://www.npmjs.com/get-npm)

### Setting up the Development Environment

1. Run the `Pre-Setup` script

    ```bash
    python .\scripts\pre_setup.py
     
    ```

2. Activate the newly created`.venv` virtual environment

    * Windows

        * CMD

            ```bash
            .venv\Scripts\activate.bat
             
            ```

        * PowerShell

            ```bash
            \.venv\Scripts\Activate.ps1
             
            ```

    * Unix/Linux

        [Note that the activation file may vary, for example mine is named `activate.fish` for the fish shell.]

        ```bash
        source .venv/bin/activate
         
        ```

3. Run the `Setup` script

    ```bash
    pdm run setup
     
    ```

4. Define your `NPM_BIN_PATH` environment variable

    1. Create a `.env` file in the root directory of the project if it doesn't exist.

    2. Find out where your npm binary is located. You can do this by running the following command in your terminal:

        * On Windows

            ```bash
            where npm
             
            ```

        * On Unix/Linux

            ```bash
            which npm
             
            ```

    3. Add the following line to your `.env` file, replacing the path with the one you found in the previous step:

        * For Unix/Linux (default on Arch)

            ```bash
            NPM_BIN_PATH=/usr/bin/npm
            ```

5. Install the Tailwind CSS dependencies by running:

    ```bash
    python src/manage.py tailwind install
     
    ```

6. Start the development server by running:

    4.1. Django

    ```bash
    python src/manage.py runserver
     
    ```

    4.2. Tailwind

    ```bash
    python src/manage.py tailwind start
     
    ```

7. Open [http://localhost:8000/](http://localhost:8000/) in your browser to access the app

8. You can now populate the database by accessing the Django admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/) and logging in with the superuser account you created during setup.

> [!NOTE]
> Closing Visual Studio Code will also close the npm dev server.
> [!IMPORTANT]
> Tailwind must be started in a separate terminal after the Django server is started. This is pretty annoying and could be improved with a script in the future.

&nbsp;

## How to deploy (prod)

> [!CAUTION]
> Work in progress.

## [#TODO Zone]

[ ] #TODO: Write data sample population script for the database
[ ] #TODO: Add prod deployment instructions

## ©️ Credits

* [Flaticon](https://www.flaticon.com/) for the icons used in the app
