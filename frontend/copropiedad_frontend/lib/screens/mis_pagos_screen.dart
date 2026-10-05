import 'dart:typed_data';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:universal_html/html.dart' as html;

import 'package:copropiedad_frontend/models/pago.dart';
import 'package:copropiedad_frontend/services/comprobante_service.dart';
import 'package:copropiedad_frontend/services/pago_service.dart';
import 'package:copropiedad_frontend/services/session_service.dart';

class MisPagosScreen extends StatefulWidget {
  const MisPagosScreen({super.key});

  @override
  State<MisPagosScreen> createState() => _MisPagosScreenState();
}

class _MisPagosScreenState extends State<MisPagosScreen> {
  final _pagoService = PagoService();
  final _comprobanteService = ComprobanteService();

  List<Pago> _pagos = [];
  bool _cargando = true;
  String? _error;
  int? _subiendoComprobantePagoId;

  final Map<int, List<Map<String, dynamic>>> _comprobantesPorPago = {};

  @override
  void initState() {
    super.initState();
    _cargarPagos();
  }

  Future<void> _cargarPagos() async {
    final token = SessionService.token;

    if (token == null) {
      if (!mounted) return;

      setState(() {
        _cargando = false;
        _error = 'No hay una sesion activa.';
      });
      return;
    }

    try {
      final pagos = await _pagoService.obtenerMisPagos(token);

      if (!mounted) return;

      setState(() {
        _pagos = pagos;
        _cargando = false;
      });

      await _cargarComprobantes(pagos, token);
    } catch (e) {
      if (!mounted) return;

      setState(() {
        _cargando = false;
        _error = 'No fue posible cargar tus pagos.';
      });
    }
  }

  Future<void> _cargarComprobantes(
    List<Pago> pagos,
    String token,
  ) async {
    final comprobantes = <int, List<Map<String, dynamic>>>{};

    for (final pago in pagos) {
      try {
        final datos = await _comprobanteService.listarComprobantes(
          token: token,
          pagoId: pago.id,
        );

        comprobantes[pago.id] = datos;
      } catch (_) {
        comprobantes[pago.id] = [];
      }
    }

    if (!mounted) return;

    setState(() {
      _comprobantesPorPago
        ..clear()
        ..addAll(comprobantes);
    });
  }

  Color _colorEstado(String estado) {
    switch (estado.toUpperCase()) {
      case 'PAGADO':
        return Colors.green;
      case 'PENDIENTE':
        return Colors.orange;
      case 'VENCIDO':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  Color _colorEstadoComprobante(String estado) {
    switch (estado.toUpperCase()) {
      case 'APROBADO':
        return Colors.green;
      case 'EN_REVISION':
        return Colors.orange;
      case 'RECHAZADO':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  String _textoEstadoComprobante(String estado) {
    switch (estado.toUpperCase()) {
      case 'EN_REVISION':
        return 'EN REVISION';
      case 'APROBADO':
        return 'APROBADO';
      case 'RECHAZADO':
        return 'RECHAZADO';
      default:
        return estado;
    }
  }

  String _formatearValor(double valor) {
    return '\$${valor.toStringAsFixed(0).replaceAllMapped(
          RegExp(r'\B(?=(\d{3})+(?!\d))'),
          (match) => '.',
        )}';
  }

  Future<void> _descargarFactura(Pago pago) async {
    final token = SessionService.token;

    if (token == null) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No hay una sesion activa.'),
        ),
      );
      return;
    }

    try {
      final bytes = await _pagoService.descargarFactura(
        token: token,
        pagoId: pago.id,
      );

      final blob = html.Blob(
        [Uint8List.fromList(bytes)],
        'application/pdf',
      );

      final url = html.Url.createObjectUrlFromBlob(blob);

      final anchor = html.AnchorElement(href: url)
        ..setAttribute(
          'download',
          'factura_${pago.id}.pdf',
        )
        ..style.display = 'none';

      html.document.body?.children.add(anchor);

      anchor.click();

      anchor.remove();

      html.Url.revokeObjectUrl(url);

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Factura descargada correctamente.'),
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'No fue posible descargar la factura: $e',
          ),
        ),
      );
    }
  }

  Future<void> _subirComprobante(Pago pago) async {
    final token = SessionService.token;

    if (token == null) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No hay una sesion activa.'),
        ),
      );
      return;
    }

    final archivos = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'jpg', 'jpeg', 'png'],
    );

    if (archivos.isEmpty) {
      return;
    }

    final archivo = archivos.first;
    final bytes = await archivo.readAsBytes();

    if (bytes.length > 5 * 1024 * 1024) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'El archivo supera el tamaño máximo permitido de 5 MB.',
          ),
        ),
      );
      return;
    }

    setState(() {
      _subiendoComprobantePagoId = pago.id;
    });

    try {
      await _comprobanteService.subirComprobante(
        token: token,
        pagoId: pago.id,
        archivo: archivo,
      );

      final comprobantes =
          await _comprobanteService.listarComprobantes(
        token: token,
        pagoId: pago.id,
      );

      if (!mounted) return;

      setState(() {
        _comprobantesPorPago[pago.id] = comprobantes;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Comprobante enviado correctamente. Estado: EN REVISION.',
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'No fue posible subir el comprobante: $e',
          ),
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _subiendoComprobantePagoId = null;
        });
      }
    }
  }

  Widget _construirEstadoComprobante(Pago pago) {
    final comprobantes = _comprobantesPorPago[pago.id] ?? [];

    if (comprobantes.isEmpty) {
      return const SizedBox.shrink();
    }

    final comprobante = comprobantes.first;

    final estado =
        comprobante['estado']?.toString() ?? 'DESCONOCIDO';

    final color = _colorEstadoComprobante(estado);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.10),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: color.withValues(alpha: 0.30),
        ),
      ),
      child: Row(
        children: [
          Icon(
            Icons.verified_outlined,
            color: color,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Comprobante',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  _textoEstadoComprobante(estado),
                  style: TextStyle(
                    color: color,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Pagos'),
      ),
      body: _cargando
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : _error != null
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(
                          Icons.error_outline,
                          size: 56,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          _error!,
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: () {
                            setState(() {
                              _cargando = true;
                              _error = null;
                            });

                            _cargarPagos();
                          },
                          child: const Text('Reintentar'),
                        ),
                      ],
                    ),
                  ),
                )
              : _pagos.isEmpty
                  ? const Center(
                      child: Text(
                        'No tienes pagos registrados.',
                      ),
                    )
                  : RefreshIndicator(
                      onRefresh: _cargarPagos,
                      child: ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: _pagos.length,
                        itemBuilder: (context, index) {
                          final pago = _pagos[index];
                          final color = _colorEstado(pago.estado);
                          final subiendo =
                              _subiendoComprobantePagoId == pago.id;

                          return Card(
                            margin: const EdgeInsets.only(bottom: 12),
                            child: Padding(
                              padding: const EdgeInsets.all(16),
                              child: Column(
                                crossAxisAlignment:
                                    CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      const Icon(
                                        Icons.receipt_long,
                                      ),
                                      const SizedBox(width: 12),
                                      Expanded(
                                        child: Text(
                                          pago.concepto,
                                          style: Theme.of(context)
                                              .textTheme
                                              .titleMedium
                                              ?.copyWith(
                                                fontWeight:
                                                    FontWeight.bold,
                                              ),
                                        ),
                                      ),
                                      Container(
                                        padding:
                                            const EdgeInsets.symmetric(
                                          horizontal: 10,
                                          vertical: 6,
                                        ),
                                        decoration: BoxDecoration(
                                          color: color.withValues(
                                            alpha: 0.12,
                                          ),
                                          borderRadius:
                                              BorderRadius.circular(20),
                                        ),
                                        child: Text(
                                          pago.estado,
                                          style: TextStyle(
                                            color: color,
                                            fontWeight:
                                                FontWeight.bold,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 12),
                                  Text(
                                    'Periodo: ${pago.periodo}',
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    'Valor: ${_formatearValor(pago.valor)}',
                                    style: const TextStyle(
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  if (pago.fechaVencimiento != null) ...[
                                    const SizedBox(height: 4),
                                    Text(
                                      'Vencimiento: '
                                      '${pago.fechaVencimiento}',
                                    ),
                                  ],
                                  const SizedBox(height: 12),
                                  _construirEstadoComprobante(pago),
                                  if ((_comprobantesPorPago[pago.id] ??
                                          [])
                                      .isNotEmpty)
                                    const SizedBox(height: 12),
                                  SizedBox(
                                    width: double.infinity,
                                    child: OutlinedButton.icon(
                                      onPressed: subiendo
                                          ? null
                                          : () =>
                                              _descargarFactura(pago),
                                      icon: const Icon(
                                        Icons.picture_as_pdf,
                                      ),
                                      label: const Text(
                                        'Descargar factura',
                                      ),
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  SizedBox(
                                    width: double.infinity,
                                    child: ElevatedButton.icon(
                                      onPressed: subiendo
                                          ? null
                                          : () =>
                                              _subirComprobante(pago),
                                      icon: subiendo
                                          ? const SizedBox(
                                              width: 18,
                                              height: 18,
                                              child:
                                                  CircularProgressIndicator(
                                                strokeWidth: 2,
                                              ),
                                            )
                                          : const Icon(
                                              Icons.upload_file,
                                            ),
                                      label: Text(
                                        subiendo
                                            ? 'Subiendo comprobante...'
                                            : 'Subir comprobante',
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ),
    );
  }
}
