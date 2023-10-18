# Call external libraries
import psycopg2
import locale
from flask import Flask, jsonify, abort, make_response, request

# Set locale to Spanish
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Create default Flask application
app = Flask(__name__)

# Define conex as a global variable
conex = None

# ================================================================
# D A T A   A C C E S S   C O D E
# ================================================================

# Function to execute data modification sentence
def execute(auxsql):
    global conex  # Declare conex as global
    data = None
    try:
        # Create data access object
        conex = psycopg2.connect(
            host='10.90.28.179',
            database='demo',
            user='postgres',
            password='Parda99$'
        )
        # Create a local cursor for SQL execution
        cur = conex.cursor()
        # Execute SQL sentence
        cur.execute(auxsql)
        # Retrieve data if it exists
        data = cur.fetchall()
        # Close cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conex is not None:
            conex.close()
            print('Connection closed.')
    # Return data
    return data

# ================================================================
# A P I   R E S T F U L   S E R V I C E
# ================================================================

# -----------------------------------------------------
# Error support section
# -----------------------------------------------------

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request....!'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized....!'}), 401)

@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Forbidden....!'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found....!'}), 404)

# -----------------------------------------------------
# Create the Flask app
# -----------------------------------------------------

# Get Aircraft
# metodo con idioma en ingles
@app.route('/aircraft/en', methods=['GET'])
def get_aircraft():
    resu = execute("select ad.aircraft_code, ad.model->'en', ad.range from aircrafts_data ad")
    if resu != None:
        salida = {
            "status_code": 200,
            "status": "OK",
            "data": []
        }
        for cod, modelo, rango in resu:
            salida["data"].append({
                "code": cod,
                "model": modelo,
                "range": rango
            })
    else:
        abort(404)
    return jsonify({'data': salida}), 200

# metodo con idioma en ruso
@app.route('/aircraft/ru', methods=['GET'])
def get_aircraft2():
    resu = execute("select ad.aircraft_code, ad.model->'ru', ad.range from aircrafts_data ad")
    if resu != None:
        salida = {
            "status_code": 200,
            "status": "OK",
            "data": []
        }
        for cod, modelo, rango in resu:
            salida["data"].append({
                "code": cod,
                "model": modelo,
                "range": rango
            })
    else:
        abort(404)
    return jsonify({'data': salida}), 200


# get airports data
# metodo con idioma en ingles
@app.route('/airports/en', methods=['GET'])
def get_airports():
    resu = execute(
        "select ad.airport_code, ad.airport_name->'en', ad.city->'en', ad.coordinates, ad.timezone from airports_data ad")
    if resu != None:
        salida = {
            "status_code": 200,
            "status": "OK",
            "data": []
        }
        for cod, nombre, ciudad, coordenadas, zonaHoraria in resu:
            salida["data"].append({
                "code": cod,
                "name": nombre,
                "city": ciudad,
                "coordinates": coordenadas,
                "timezone": zonaHoraria
            })
    else:
        abort(404)
    return jsonify({'data': salida}), 200

# metodo con idioma en ruso
@app.route('/airports/ru', methods=['GET'])
def get_airports2():
    resu = execute(
        "select ad.airport_code, ad.airport_name->'ru', ad.city->'ru', ad.coordinates, ad.timezone from airports_data ad")
    if resu != None:
        salida = {
            "status_code": 200,
            "status": "OK",
            "data": []
        }
        for cod, nombre, ciudad, coordenadas, zonaHoraria in resu:
            salida["data"].append({
                "code": cod,
                "name": nombre,
                "city": ciudad,
                "coordinates": coordenadas,
                "timezone": zonaHoraria
            })
    else:
        abort(404)
    return jsonify({'data': salida}), 200

# metodo para obtener la lista de pasajeros de un vuelo
@app.route('/passengerList', methods=['GET'])
def get_passengerList():
    resu = execute("select * from passengerFlights")
    if resu != None:
        salida = {
            "status_code": 200,
            "status": "OK",
            "data": []
        }
        for numeroVuelo, AeropuertoSalida, AeropuertoLlegada, horaSalida, horaLlegada, idPasajero, nombrePasajero, in resu:
            salida["data"].append({
                "flight_no": numeroVuelo,
                "departure_airport": AeropuertoSalida,
                "arrival_airport": AeropuertoLlegada,
                "scheduled_departure": horaSalida,
                "scheduled_arrival": horaLlegada,
                "passenger_id": idPasajero,
                "passenger_name": nombrePasajero,

            })
    else:
        abort(404)
    return jsonify({'data': salida}), 200

# metodo para obtener la informacion sobre los asientos disponibles y no disponibles de un vuelo
@app.route('/flightOccupation', methods=['GET'])
def getNivelOcupacionVuelo():
    resu = execute(
        """
        SELECT
            f.flight_id AS "Vuelo id",
            s.fare_conditions AS "Clase tipo",
            COUNT(bp.seat_no) AS "Numero de sillas ocupadas",
            (
                SELECT COUNT(*) 
                FROM bookings.seats 
                WHERE seats.aircraft_code = f.aircraft_code 
                AND seats.fare_conditions = s.fare_conditions
            ) - COUNT(bp.seat_no) AS "Numero de sillas disponibles",
            (
                SELECT COUNT(*) 
                FROM bookings.seats 
                WHERE seats.aircraft_code = f.aircraft_code 
                AND seats.fare_conditions = s.fare_conditions
            ) AS "Total de sillas"
        FROM bookings.boarding_passes bp
        INNER JOIN bookings.ticket_flights tf 
        ON bp.ticket_no = tf.ticket_no AND bp.flight_id = tf.flight_id
        INNER JOIN bookings.flights f 
        ON bp.flight_id = f.flight_id
        INNER JOIN bookings.seats s 
        ON f.aircraft_code = s.aircraft_code AND bp.seat_no = s.seat_no
        GROUP BY f.flight_id, s.fare_conditions
        LIMIT 10
        """
    )
    if resu is not None:
        salida = {
            "status_code": 200,
            "status": "OK",
            "data": []
        }
        for (
            flight_id, fare_conditions, sillas_ocupadas, sillas_disponibles, total_sillas
        ) in resu:
            salida["data"].append({
                "Vuelo id": flight_id,
                "Clase tipo": fare_conditions,
                "Numero de sillas ocupadas": sillas_ocupadas,
                "Numero de sillas disponibles": sillas_disponibles,
                "Total de sillas": total_sillas,
            })
    else:
        abort(404)
    return jsonify({'data': salida}), 200




if __name__ == '__main__':
    app.run(host='192.168.0.11', port=5001, debug=True)