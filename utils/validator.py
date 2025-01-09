from flask import jsonify

def check_required_fields(fields:list, data):
    for field in fields:
        if field not in data or not data.get(field):
            return f'{field} cannot be empty'
    return


