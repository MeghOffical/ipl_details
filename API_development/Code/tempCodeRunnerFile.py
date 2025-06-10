@app.route('/api/point_table')
def point_table():
    season = request.args.get('season')
    if not season:
        return jsonify({'error': 'Season parameter is missing'}), 400
    try:
        data = ipl.point_table_extension(season)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500