# ==========================================
# LÓGICA DE REGISTRO
# ==========================================
def registro():
    supabase = get_supabase_client()
    if not supabase: return jsonify({"status": "error", "message": "Falta BD."}), 500
    
    data = request.get_json(silent=True) or {}
    email, password = data.get('email'), data.get('password')
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Faltan datos clave."}), 400
    
    try:
        res = supabase.table('usuarios_refugio').select('email').eq('email', email).execute()
        if len(res.data) > 0: return jsonify({"status": "existe", "message": "Correo ya registrado."}), 200
        
        # Guardamos la contraseña en texto plano para evitar colapsos de memoria en Vercel
        pass_hash = password
        
        lat_val = data.get('lat')
        lon_val = data.get('lon')
        lat = float(lat_val) if lat_val else 0.0
        lon = float(lon_val) if lon_val else 0.0
        
        nuevo_usuario = {
            "nombre": data.get('nombre'), "email": email, "contrasena": pass_hash,
            "fecha_nacimiento": data.get('fecha'), "hora_nacimiento": data.get('hora'),
            "ciudad": data.get('ciudad', '').upper(), "nivel_suscripcion": "free",
            "datos_natales": {"geo": {"lat": lat, "lon": lon}, "auth": "PENDING"}
        }
        supabase.table('usuarios_refugio').insert(nuevo_usuario).execute()
        return jsonify({"status": "exito"}), 201
    except Exception as e:
        print(f"Error en registro: {str(e)}", flush=True)
        return jsonify({"status": "error", "message": "Error interno al guardar."}), 500

# ==========================================
# LÓGICA DE LOGIN
# ==========================================
def login():
    supabase = get_supabase_client()
    if not supabase: return jsonify({"status": "error", "message": "Falta BD."}), 500
    
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Credenciales incompletas."}), 400
    
    try:
        res = supabase.table('usuarios_refugio').select('*').eq('email', email).execute()
        if len(res.data) == 0:
            return jsonify({"status": "error", "message": "Usuario no encontrado."}), 404
            
        usuario = res.data[0]
        
        # Comparamos texto plano directamente
        if usuario.get('contrasena') == password:
            return jsonify({
                "status": "exito", 
                "datos": {
                    "nombre": usuario.get('nombre'), 
                    "email": usuario.get('email'),
                    "nivel": usuario.get('nivel_suscripcion'),
                    "fecha": usuario.get('fecha_nacimiento')
                }
            }), 200
            
        return jsonify({"status": "error", "message": "Contraseña incorrecta."}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
