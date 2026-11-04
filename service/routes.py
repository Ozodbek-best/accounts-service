"""Accounts REST API routes"""
from flask import jsonify, request, abort, url_for
from service import app
from service.models import Account, DataValidationError


@app.route("/")
def index():
    """Root URL"""
    return jsonify(name="Account REST API Service", version="1.0"), 200


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Create an Account"""
    account = Account()
    try:
        account.deserialize(request.get_json())
    except DataValidationError as error:
        abort(400, str(error))
    account.create()
    location = url_for("read_accounts", account_id=account.id, _external=True)
    return jsonify(account.serialize()), 201, {"Location": location}


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    accounts = [account.serialize() for account in Account.all()]
    return jsonify(accounts), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id):
    """Read an Account"""
    account = Account.find(account_id)
    if not account:
        abort(404, "Account was not found")
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update an Account"""
    account = Account.find(account_id)
    if not account:
        abort(404, "Account was not found")
    try:
        account.deserialize(request.get_json())
    except DataValidationError as error:
        abort(400, str(error))
    account.update()
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete an Account"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204
