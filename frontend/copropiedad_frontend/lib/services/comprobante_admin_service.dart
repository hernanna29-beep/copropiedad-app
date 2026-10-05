import 'dart:convert';
import 'dart:typed_data';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';

class ComprobanteAdminService {
  Future<List<Map<String, dynamic>>> listarEnRevision({
    required String token,
  }) async {
    final response = await http.get(
      Uri.parse(
        '${ApiConfig.baseUrl}/comprobantes/admin/en-revision',
      ),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final datos = jsonDecode(response.body) as List<dynamic>;

      return datos
          .map(
            (item) => item as Map<String, dynamic>,
          )
          .toList();
    }

    if (response.statusCode == 401) {
      throw Exception(
        'Sesión expirada o token inválido',
      );
    }

    if (response.statusCode == 403) {
      throw Exception(
        'No tienes permisos de administrador',
      );
    }

    throw Exception(
      'Error al consultar comprobantes: '
      '${response.statusCode}',
    );
  }

  Future<Map<String, dynamic>> actualizarEstado({
    required String token,
    required int comprobanteId,
    required String estado,
    String? observaciones,
  }) async {
    final response = await http.put(
      Uri.parse(
        '${ApiConfig.baseUrl}/comprobantes/admin/$comprobanteId',
      ),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'estado': estado,
        'observaciones': observaciones,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body)
          as Map<String, dynamic>;
    }

    if (response.statusCode == 401) {
      throw Exception(
        'Sesión expirada o token inválido',
      );
    }

    if (response.statusCode == 403) {
      throw Exception(
        'No tienes permisos de administrador',
      );
    }

    if (response.statusCode == 404) {
      throw Exception(
        'Comprobante no encontrado',
      );
    }

    throw Exception(
      'Error al actualizar comprobante: '
      '${response.statusCode}',
    );
  }

  Future<Uint8List> descargarComprobante({
    required String token,
    required int comprobanteId,
  }) async {
    final response = await http.get(
      Uri.parse(
        '${ApiConfig.baseUrl}/comprobantes/admin/'
        '$comprobanteId/archivo',
      ),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return response.bodyBytes;
    }

    if (response.statusCode == 401) {
      throw Exception(
        'Sesión expirada o token inválido',
      );
    }

    if (response.statusCode == 403) {
      throw Exception(
        'No tienes permisos para visualizar este comprobante',
      );
    }

    if (response.statusCode == 404) {
      throw Exception(
        'Archivo del comprobante no encontrado',
      );
    }

    throw Exception(
      'Error al obtener comprobante: '
      '${response.statusCode}',
    );
  }
}