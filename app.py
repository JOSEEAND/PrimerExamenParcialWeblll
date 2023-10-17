# Get Aircraft
# Método para elegir el idioma
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
# Método para elegir el idioma
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
