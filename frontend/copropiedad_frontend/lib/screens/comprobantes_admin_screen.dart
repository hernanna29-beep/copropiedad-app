import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:universal_html/html.dart' as html;

import '../services/comprobante_admin_service.dart';
import '../services/session_service.dart';

class ComprobantesAdminScreen extends StatefulWidget {
  const ComprobantesAdminScreen({super.key});

  @override
  State<ComprobantesAdminScreen> createState() =>
      _ComprobantesAdminScreenState();
}

class _ComprobantesAdminScreenState
    extends State<ComprobantesAdminScreen> {
  final ComprobanteAdminService _service =
      ComprobanteAdminService();

  List<Map<String, dynamic>> _comprobantes = [];

  bool _cargando = true;
  String? _error;

  int? _procesandoId;
  int? _visualizandoId;

  @override
  void initState() {
    super.initState();
    _cargarComprobantes();
  }

  Future<void> _cargarComprobantes() async {
    final token = SessionService.token;

    if (token == null) {
      if (!mounted) {
        return;
      }

      setState(() {
        _cargando = false;
        _error = 'Sesión no disponible.';
      });

      return;
    }

    setState(() {
      _cargando = true;
      _error = null;
    });

    try {
      final datos = await _service.listarEnRevision(
        token: token,
      );

      if (!mounted) {
        return;
      }

      setState(() {
        _comprobantes = datos;
        _cargando = false;
      });
    } catch (e) {
      if (!mounted) {
        return;
      }

      setState(() {
        _cargando = false;
        _error = e.toString();
      });
    }
  }

  Future<void> _verComprobante(
    Map<String, dynamic> comprobante,
  ) async {
    final token = SessionService.token;

    if (token == null) {
      _mostrarMensaje('Sesión no disponible.');
      return;
    }

    final comprobanteId =
        comprobante['id'] as int;

    final tipoArchivo =
        comprobante['tipo_archivo']?.toString() ??
            'application/octet-stream';

    setState(() {
      _visualizandoId = comprobanteId;
    });

    try {
      final bytes =
          await _service.descargarComprobante(
        token: token,
        comprobanteId: comprobanteId,
      );

      final blob = html.Blob(
        [
          Uint8List.fromList(bytes),
        ],
        tipoArchivo,
      );

      final url =
          html.Url.createObjectUrlFromBlob(blob);

      final anchor = html.AnchorElement(
        href: url,
      )
        ..target = '_blank'
        ..style.display = 'none';

      html.document.body?.children.add(anchor);

      anchor.click();

      anchor.remove();

      html.Url.revokeObjectUrl(url);

      if (!mounted) {
        return;
      }

      _mostrarMensaje(
        'Comprobante abierto correctamente.',
      );
    } catch (e) {
      if (!mounted) {
        return;
      }

      _mostrarMensaje(
        'No fue posible abrir el comprobante.',
      );
    } finally {
      if (mounted) {
        setState(() {
          _visualizandoId = null;
        });
      }
    }
  }

  Future<void> _aprobarComprobante(
    int comprobanteId,
  ) async {
    final token = SessionService.token;

    if (token == null) {
      _mostrarMensaje('Sesión no disponible.');
      return;
    }

    setState(() {
      _procesandoId = comprobanteId;
    });

    try {
      await _service.actualizarEstado(
        token: token,
        comprobanteId: comprobanteId,
        estado: 'APROBADO',
      );

      if (!mounted) {
        return;
      }

      _mostrarMensaje(
        'Comprobante aprobado correctamente.',
      );

      await _cargarComprobantes();
    } catch (e) {
      if (!mounted) {
        return;
      }

      _mostrarMensaje(
        'No fue posible aprobar el comprobante.',
      );
    } finally {
      if (mounted) {
        setState(() {
          _procesandoId = null;
        });
      }
    }
  }

  Future<void> _mostrarDialogoRechazo(
    int comprobanteId,
  ) async {
    final controlador = TextEditingController();

    final observacion = await showDialog<String>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text(
            'Rechazar comprobante',
          ),
          content: TextField(
            controller: controlador,
            maxLines: 4,
            decoration: const InputDecoration(
              labelText: 'Observación',
              hintText:
                  'Indique el motivo del rechazo',
              border: OutlineInputBorder(),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Cancelar'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop(
                  controlador.text.trim(),
                );
              },
              child: const Text('Rechazar'),
            ),
          ],
        );
      },
    );

    controlador.dispose();

    if (observacion == null) {
      return;
    }

    await _rechazarComprobante(
      comprobanteId,
      observacion,
    );
  }

  Future<void> _rechazarComprobante(
    int comprobanteId,
    String observacion,
  ) async {
    final token = SessionService.token;

    if (token == null) {
      _mostrarMensaje('Sesión no disponible.');
      return;
    }

    if (observacion.isEmpty) {
      _mostrarMensaje(
        'Debe indicar una observación para rechazar el comprobante.',
      );
      return;
    }

    setState(() {
      _procesandoId = comprobanteId;
    });

    try {
      await _service.actualizarEstado(
        token: token,
        comprobanteId: comprobanteId,
        estado: 'RECHAZADO',
        observaciones: observacion,
      );

      if (!mounted) {
        return;
      }

      _mostrarMensaje(
        'Comprobante rechazado correctamente.',
      );

      await _cargarComprobantes();
    } catch (e) {
      if (!mounted) {
        return;
      }

      _mostrarMensaje(
        'No fue posible rechazar el comprobante.',
      );
    } finally {
      if (mounted) {
        setState(() {
          _procesandoId = null;
        });
      }
    }
  }

  void _mostrarMensaje(String mensaje) {
    if (!mounted) {
      return;
    }

    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          content: Text(mensaje),
        ),
      );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Comprobantes en revisión',
        ),
        actions: [
          IconButton(
            onPressed:
                _cargando ? null : _cargarComprobantes,
            icon: const Icon(
              Icons.refresh,
            ),
            tooltip: 'Actualizar',
          ),
        ],
      ),
      body: _construirContenido(),
    );
  }

  Widget _construirContenido() {
    if (_cargando) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.error_outline,
                size: 48,
              ),
              const SizedBox(height: 16),
              Text(
                _error!,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _cargarComprobantes,
                child: const Text(
                  'Reintentar',
                ),
              ),
            ],
          ),
        ),
      );
    }

    if (_comprobantes.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.check_circle_outline,
                size: 56,
              ),
              SizedBox(height: 16),
              Text(
                'No hay comprobantes pendientes de revisión.',
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _cargarComprobantes,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _comprobantes.length,
        itemBuilder: (context, index) {
          final comprobante =
              _comprobantes[index];

          return _construirTarjeta(
            comprobante,
          );
        },
      ),
    );
  }

  Widget _construirTarjeta(
    Map<String, dynamic> comprobante,
  ) {
    final id = comprobante['id'];
    final pagoId = comprobante['pago_id'];

    final nombreArchivo =
        comprobante['nombre_archivo'] ??
            'Sin nombre';

    final estado =
        comprobante['estado'] ??
            'SIN ESTADO';

    final tamano =
        comprobante['tamano_archivo'] ?? 0;

    final procesando =
        _procesandoId == id;

    final visualizando =
        _visualizandoId == id;

    return Card(
      margin: const EdgeInsets.only(
        bottom: 16,
      ),
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
                  size: 30,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'Comprobante #$id',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 16),

            Text(
              'Pago: #$pagoId',
            ),

            const SizedBox(height: 8),

            Text(
              'Archivo: $nombreArchivo',
            ),

            const SizedBox(height: 8),

            Text(
              'Tamaño: $tamano bytes',
            ),

            const SizedBox(height: 12),

            Chip(
              label: Text(
                estado,
              ),
            ),

            const SizedBox(height: 16),

            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed:
                    procesando || visualizando
                        ? null
                        : () {
                            _verComprobante(
                              comprobante,
                            );
                          },
                icon: visualizando
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child:
                            CircularProgressIndicator(
                          strokeWidth: 2,
                        ),
                      )
                    : const Icon(
                        Icons.visibility,
                      ),
                label: Text(
                  visualizando
                      ? 'Abriendo comprobante...'
                      : 'Ver comprobante',
                ),
              ),
            ),

            const SizedBox(height: 12),

            if (procesando)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(8),
                  child:
                      CircularProgressIndicator(),
                ),
              )
            else
              Row(
                children: [
                  Expanded(
                    child:
                        ElevatedButton.icon(
                      onPressed: () {
                        _aprobarComprobante(
                          id as int,
                        );
                      },
                      icon: const Icon(
                        Icons.check,
                      ),
                      label: const Text(
                        'Aprobar',
                      ),
                    ),
                  ),

                  const SizedBox(width: 12),

                  Expanded(
                    child:
                        OutlinedButton.icon(
                      onPressed: () {
                        _mostrarDialogoRechazo(
                          id as int,
                        );
                      },
                      icon: const Icon(
                        Icons.close,
                      ),
                      label: const Text(
                        'Rechazar',
                      ),
                    ),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}