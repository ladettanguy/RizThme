# To launch the discord client

First step is to add in your environments variables, a variables named "TOKEN" with in value, your discord application token

## For Linux user

For use automatically your virtual environment. (The virtual environment name need to be "venv/")

```console
foo@bar:~$ source entrypoint.sh
```

if you don't want to use a virtual environment. juste use the script like this:

```console
foo@bar:~$ bash entrypoint.sh
```
or 

```console
foo@bar:~$ sh entrypoint.sh
```

## For Windows user

> I don't know. 
> 
> Maybe it's time to use a real Operating System.

you can do like this if you realy want to use that in Windows system

```
pip install -r requirements.txt
python3 client.py
```