For /cart route we optimize the @app.route('/cart') ,@app.route('/cart/remove/<id>', methods=['POST']), @app.route('/cart/delete', methods=['GET']), @app.route('/cart/<id>', methods=['POST'])
and also add helper functions and decorators in main.py
we also optimize /cart/__init__.py code

For /browse route we optimize @app.route('/browse') in main.py 
and optimize def list_products() function in /products/__init__.py
