""" Controller for the process endpoint. 
    Description: Contains API endpoint handler functions for CRUD (create, read, update, delete) and other model operations.  
"""

from models.process import process
from app.app import db
import json
from sqlalchemy.exc import SQLAlchemyError

def create(body): 
    """ Create a register in db based on a json from a request's body parameter.
		Also create the the process' tables based on the configuration field.

        Args:
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created process register with empty password field.
    """
    # instantiate process with the body dict as kwargs
    new_process = process(**body)
    # create new flask-sqlalchemy session
    db.session.add(new_process)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # test if the new process was created 
    try:
        res = process.query.filter_by(processname=new_process.processname).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # empty pass
    res.password=""
    # return register as dict
    return res.as_dict()

def read(processId):
    """ Query a register in db based on the id field of the process model, obtained from a request's processId url parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (dict): the requested process register with empty password field.
    """ 
    try:
        res = process.query.filter_by(processname=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # empty pass
    res.password=""
    return res.as_dict()
    

def update(processId, body):
    """ Update a register in db based on a json from a request's body parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).
        body (dict): dict containing the fields of the new register, obtained from json in the body of the request.

        Returns:
        res (dict): the newly created process register with empty password field.
    """
    # query the existing register
    try:
        res = process.query.filter_by(processname=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # replace model with body fields
    body['id']=res.id
    res.__dict__ = body
    # perform update 
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # test if the model was updated 
    try:
        res = process.query.filter_by(processname=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # empty pass
    res.password=""
    # return register as dict
    return res.as_dict()

def delete(processId):
    """ Delete a register in db based on the id field of the process model, obtained from a request's processId url parameter.

        Args:
        processId (str): id field of the process model, obtained from a request's processId url parameter (processs/<processId>).

        Returns:
        res (int): the deleted register id field
    """ 
    try:
        res = process.query.filter_by(processname=processId).first_or_404()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # perform delete 
    db.session.delete(res)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    return res.id

def read_all():
    """ Query all registers of the process model.

        Returns:
        res (dict): the requested process registers with empty password field.
    """ 
    try:
        res = process.query.all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error
    # convert to list of dicts and empty pass
    res2 =[]
    for r in res:
        r.password = ""
        res2.append(r.as_dict())
    return res2
   




