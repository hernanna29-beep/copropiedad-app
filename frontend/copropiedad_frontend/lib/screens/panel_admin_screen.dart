import 'package:flutter/material.dart';

import 'comprobantes_admin_screen.dart';

class PanelAdminScreen extends StatelessWidget {
  const PanelAdminScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Panel administrativo'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          const Icon(
            Icons.admin_panel_settings,
            size: 72,
          ),
          const SizedBox(height: 16),
          const Text(
            'COPROPIEDAD APP',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'Panel administrativo',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 16,
            ),
          ),
          const SizedBox(height: 32),
          Card(
            child: ListTile(
              leading: const Icon(
                Icons.receipt_long,
                size: 32,
              ),
              title: const Text(
                'Comprobantes de pago',
              ),
              subtitle: const Text(
                'Revisar comprobantes enviados por residentes',
              ),
              trailing: const Icon(
                Icons.chevron_right,
              ),
              onTap: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) =>
                        const ComprobantesAdminScreen(),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}