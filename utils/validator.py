from flask import jsonify

def check_required_fields(fields:list, data):
    for field in fields:
        if field not in data or not data.get(field) and data.get(field) != 0:
            return f'{field} cannot be empty'
    return


