import 'package:flutter/material.dart';

import 'package:copropiedad_frontend/screens/mis_pagos_screen.dart';
import 'package:copropiedad_frontend/screens/panel_admin_screen.dart';
import 'package:copropiedad_frontend/services/auth_service.dart';
import 'package:copropiedad_frontend/services/session_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _emailController =
      TextEditingController(text: 'juan.naranjo@example.com');

  final TextEditingController _passwordController =
      TextEditingController(text: 'Copropiedad2026!');

  final AuthService _authService = AuthService();

  bool _cargando = false;
  String? _error;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _iniciarSesion() async {
    setState(() {
      _cargando = true;
      _error = null;
    });

    try {
      final respuesta = await _authService.login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );

      SessionService.iniciarSesion(respuesta.accessToken);

      if (!mounted) {
        return;
      }

      final rol = SessionService.rol;

      if (rol == 'ADMIN') {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (_) => const PanelAdminScreen(),
          ),
        );
      } else if (rol == 'RESIDENTE') {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (_) => const MisPagosScreen(),
          ),
        );
      } else {
        SessionService.cerrarSesion();

        setState(() {
          _error = 'Rol de usuario no reconocido.';
          _cargando = false;
        });
      }
    } catch (e) {
      if (!mounted) {
        return;
      }

      setState(() {
        _error = 'Credenciales incorrectas.';
        _cargando = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('COPROPIEDAD APP'),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(
            maxWidth: 420,
          ),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(
                  Icons.apartment,
                  size: 72,
                ),
                const SizedBox(height: 24),
                TextField(
                  controller: _emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: 'Correo electrónico',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Contraseña',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),
                if (_error != null) ...[
                  Text(
                    _error!,
                    style: const TextStyle(
                      color: Colors.red,
                    ),
                  ),
                  const SizedBox(height: 16),
                ],
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _cargando ? null : _iniciarSesion,
                    child: _cargando
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                            ),
                          )
                        : const Text('Iniciar sesión'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}