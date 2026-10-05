import 'jwt_service.dart';

class SessionService {
  static String? _token;
  static String? _rol;

  static void iniciarSesion(String token) {
    _token = token;
    _rol = JwtService.obtenerRol(token);
  }

  static String? get token => _token;

  static String? get rol => _rol;

  static bool get estaAutenticado => _token != null;

  static void cerrarSesion() {
    _token = null;
    _rol = null;
  }
}