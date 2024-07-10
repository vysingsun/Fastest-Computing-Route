# install some library
pip install -r requirements.txt
# if has error need to install jinja
pip install jinja


# run the project
python -m uvicon main:app --reload
# or
uvicorn main:app --host 0.0.0.0
