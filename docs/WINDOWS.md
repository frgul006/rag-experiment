# Setting Up a Python Development Environment on Windows

## Installing Windows Subsystem for Linux (WSL) 2

[How to install WSL 2 on Windows 10](https://www.omgubuntu.co.uk/how-to-install-wsl2-on-windows-10)

1. Open a command prompt with **Administrator** permissions.
2. Run the following command to install WSL 2:

   ```bash
   wsl.exe --install
   ```

3. Reboot your computer.
4. Upon login, complete the Ubuntu setup with a username and password.

   > Note: These don’t need to be the same as your Windows username and password.

### Post-Installation

- Launch Ubuntu via the `Start Menu`, or install the Microsoft Terminal app to use your new Ubuntu installation.
- Run the following command to update the Ubuntu packages:

  ```bash
  sudo apt update && sudo apt upgrade
  ```

---

## Installing Required Packages

[Install Python pyenv on WSL Ubuntu](https://www.techtronic.us/install-python-pyenv-on-wsl-ubuntu/)

Run the following command to install the essential packages for building Python:

```bash
sudo apt-get install git gcc make openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev zlib1g-dev libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev lzma libjpeg-dev mypy liblzma-dev
```

---

## Installing pyenv

Execute the following command to install `pyenv`:

```bash
curl https://pyenv.run | bash
```

---

## Editing Files in Ubuntu Terminal Using Vim

1. Open the file with `vim`:

   ```bash
   vim NAME_OF_FILE
   ```

2. Press `I` to enter interactive (insert) mode.
3. Make your changes.
4. Press `Escape` followed by `:wq` to save and exit.

---

## Configuring Bash Profile and Bashrc

1. Add the following to `~/.bash_profile`:

   ```bash
   if [ -f "$HOME/.bashrc" ]; then
       . "$HOME/.bashrc"
   fi
   ```

2. Add the following to `~/.bashrc` to initialize pyenv:

   ```bash
   export GPG_TTY=$(tty)
   export PIPENV_VENV_IN_PROJECT=1
   export PYENV_ROOT="$HOME/.pyenv"
   command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   ```

---

## Installing Python and pipenv

1. Install Python 3.11.6:

   ```bash
   pyenv install 3.11.6
   ```

2. Set it as the global Python version:

   ```bash
   pyenv global 3.11.6
   ```

3. Upgrade pip:

   ```bash
   pip install pip --upgrade
   ```

4. Install pipenv:

   ```bash
   pip install pipenv
   ```

---

## Installing Rust Compiler

Run the following command:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

---

## Verification

Check the versions to make sure everything is set up correctly:

- `pyenv --version`
- `python --version`
- `pipenv --version`
- `cargo --version`

---

## Install volta

<https://volta.sh/> is a universal JavaScript Tool Manager (replaces nvm for Node version management)

```bash
curl https://get.volta.sh | bash
```

## Install node

```bash
volta install node@18
```

## Git Setup

1. Generate GPG Key:

   ```bash
   gpg --full-generate-key
   ```

2. List secret keys:

   ```bash
   gpg --list-secret-keys --keyid-format=long
   ```

3. Export signing key:

   ```bash
   gpg --armor --export SOME_SIGNING_KEY
   ```

4. Add signing key to github.com

https://github.com/settings/gpg/new

5. Git Configuration:

   ```bash
   git config --global user.signingkey SOME_SIGNING_KEY
   git config --global --unset gpg.format
   git config --global user.name "John Doe"
   git config --global user.email "john@doe.com"
   ```

6. Clone repo and set up development:

   ```bash
   git clone https://github.com/frgul006/rag-experiment.git
   cd rag-experiment/
   make install-dev
   ```
