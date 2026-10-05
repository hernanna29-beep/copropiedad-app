import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/pago.dart';

class PagoService {
  Future<List<Pago>> obtenerMisPagos(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/pagos/mis-pagos'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> datos = jsonDecode(response.body);

      return datos
          .map((json) => Pago.fromJson(json))
          .toList();
    }

    if (response.statusCode == 401) {
      throw Exception('Sesión expirada o token inválido');
    }

    if (response.statusCode == 403) {
      throw Exception(
        'No tienes permiso para consultar tus pagos',
      );
    }

    throw Exception(
      'Error al consultar pagos: ${response.statusCode}',
    );
  }

  Future<List<int>> descargarFactura({
    required String token,
    required int pagoId,
  }) async {
    final response = await http.get(
      Uri.parse(
        '${ApiConfig.baseUrl}/pagos/$pagoId/factura',
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
        'No tienes permiso para descargar esta factura',
      );
    }

    if (response.statusCode == 404) {
      throw Exception('Factura no encontrada');
    }

    throw Exception(
      'Error al descargar factura: ${response.statusCode}',
    );
  }
}