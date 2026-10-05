class Pago {
  final int id;
  final int unidadId;
  final String concepto;
  final String periodo;
  final double valor;
  final String estado;
  final String? fechaVencimiento;
  final String? fechaPago;
  final String? referencia;
  final String? observaciones;
  final bool activo;

  Pago({
    required this.id,
    required this.unidadId,
    required this.concepto,
    required this.periodo,
    required this.valor,
    required this.estado,
    this.fechaVencimiento,
    this.fechaPago,
    this.referencia,
    this.observaciones,
    required this.activo,
  });

  factory Pago.fromJson(Map<String, dynamic> json) {
  return Pago(
    id: json['id'],
    unidadId: json['unidad_id'],
    concepto: json['concepto'],
    periodo: json['periodo'],
    valor: double.parse(json['valor'].toString()),
    estado: json['estado'],
    fechaVencimiento: json['fecha_vencimiento'],
    fechaPago: json['fecha_pago'],
    referencia: json['referencia'],
    observaciones: json['observaciones'],
    activo: json['activo'],
  );
}

}
