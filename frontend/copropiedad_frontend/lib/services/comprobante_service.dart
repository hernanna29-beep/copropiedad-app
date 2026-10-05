import 'dart:convert';

import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

import '../config/api_config.dart';

class ComprobanteService {
  Future<Map<String, dynamic>> subirComprobante({
    required String token,
    required int pagoId,
    required PlatformFile archivo,
  }) async {
    final bytes = await archivo.readAsBytes();

    final extension = archivo.extension?.toLowerCase();

    MediaType tipoArchivo;

    switch (extension) {
      case 'pdf':
        tipoArchivo = MediaType('application', 'pdf');
        break;
      case 'jpg':
      case 'jpeg':
        tipoArchivo = MediaType('image', 'jpeg');
        break;
      case 'png':
        tipoArchivo = MediaType('image', 'png');
        break;
      default:
        throw Exception(
          'Tipo de archivo no permitido. Use PDF, JPG o PNG.',
        );
    }

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('${ApiConfig.baseUrl}/comprobantes/$pagoId'),
    );

    request.headers['Authorization'] = 'Bearer $token';

    request.files.add(
      http.MultipartFile.fromBytes(
        'archivo',
        bytes,
        filename: archivo.name,
        contentType: tipoArchivo,
      ),
    );

    final response = await request.send();
    final responseBody = await response.stream.bytesToString();

    if (response.statusCode == 201) {
      return jsonDecode(responseBody) as Map<String, dynamic>;
    }

    if (response.statusCode == 400) {
      throw Exception('Archivo no válido: $responseBody');
    }

    if (response.statusCode == 401) {
      throw Exception('Sesión expirada o token inválido');
    }

    if (response.statusCode == 403) {
      throw Exception('No tienes permiso para subir este comprobante');
    }

    if (response.statusCode == 404) {
      throw Exception('Pago no encontrado');
    }

    throw Exception(
      'Error al subir comprobante: ${response.statusCode}',
    );
  }

  Future<List<Map<String, dynamic>>> listarComprobantes({
    required String token,
    required int pagoId,
  }) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/comprobantes/pago/$pagoId'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final datos = jsonDecode(response.body) as List<dynamic>;

      return datos
          .map((item) => item as Map<String, dynamic>)
          .toList();
    }

    if (response.statusCode == 401) {
      throw Exception('Sesión expirada o token inválido');
    }

    if (response.statusCode == 403) {
      throw Exception(
        'No tienes permiso para consultar estos comprobantes',
      );
    }

    if (response.statusCode == 404) {
      throw Exception('Pago no encontrado');
    }

    throw Exception(
      'Error al consultar comprobantes: ${response.statusCode}',
    );
  }
}
