import os

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import gladiator as gl
from schema import RateSchema
from rates_service import get_port_codes_for_region_or_return_port, get_average_prices_between_dates_and_ports

app = Flask(__name__)

username = os.environ.get("POSTGRES_USERNAME")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@{}".format(username, password, host)
db = SQLAlchemy(app)

yyyy_mm_dd_regex = '^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'

field_validations = (
    ('origin', gl.required),
    ('destination', gl.required),
    ('date_from', gl.required, gl.type_(str), gl.regex_(yyyy_mm_dd_regex)),
    ('date_to', gl.required, gl.type_(str), gl.regex_(yyyy_mm_dd_regex))
)


@app.route("/rates", methods=["GET"])
def read_rates():
    args = request.args
    origin = args.get("origin")
    destination = args.get("destination")
    date_from = args.get("date_from")
    date_to = args.get("date_to")

    validation_result = gl.validate(field_validations, {
        'origin': origin,
        'destination': destination,
        'date_from': date_from,
        'date_to': date_to
    })

    if bool(validation_result) is not True:
        return validation_result.errors[0][1] + ' ' + validation_result.errors[0][0], 400

    port_codes_for_origin = get_port_codes_for_region_or_return_port(db, origin)
    port_codes_for_destination = get_port_codes_for_region_or_return_port(db, destination)

    average_prices = get_average_prices_between_dates_and_ports(db, date_from, date_to, port_codes_for_origin,
                                                                port_codes_for_destination)
    return RateSchema(many=True).dump(average_prices)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
