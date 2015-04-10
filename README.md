# state-of-states


##Using virtualenv.

    pip install virtualenv
    cd state-of-states
    
    #Create env
    virtualenv venv

    #Switch to it
    source venv/bin/activate

    #Let's install stuff, this file is what I have on mine
    pip install -r requirements.txt

    #When leaving
    deactivate

I've also excluded the venv folder in the gitignore.

Tutorial: http://docs.python-guide.org/en/latest/dev/virtualenvs/
