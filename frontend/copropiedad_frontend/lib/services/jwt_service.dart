import 'dart:convert';

class JwtService {
  static Map<String, dynamic> decodificarPayload(String token) {
    final partes = token.split('.');

    if (partes.length != 3) {
      throw const FormatException('Token JWT inválido');
    }

    final payload = base64Url.decode(
      base64Url.normalize(partes[1]),
    );

    final datos = jsonDecode(
      utf8.decode(payload),
    );

    if (datos is! Map<String, dynamic>) {
      throw const FormatException('Payload JWT inválido');
    }

    return datos;
  }

  static String? obtenerRol(String token) {
    final payload = decodificarPayload(token);
    final rol = payload['rol'];

    return rol is String ? rol : null;
  }
}