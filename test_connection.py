"""
Script para probar la conexión al servidor PostgreSQL remoto
"""
import socket
import sys

def test_port(host, port, timeout=5):
    """Prueba si un puerto está abierto"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error al probar puerto: {e}")
        return False

def test_ping(host):
    """Prueba si el host responde (ping)"""
    import subprocess
    try:
        # Windows
        result = subprocess.run(['ping', '-n', '1', host], 
                              capture_output=True, 
                              timeout=5)
        return result.returncode == 0
    except:
        return False

if __name__ == "__main__":
    host = "159.203.165.120"
    port = 5432
    
    print(f"Probando conectividad al servidor {host}:{port}...")
    print("-" * 50)
    
    # Probar ping
    print(f"1. Probando ping a {host}...")
    if test_ping(host):
        print("   [OK] El servidor responde al ping")
    else:
        print("   [ERROR] El servidor NO responde al ping")
        print("   [ADVERTENCIA] Esto puede significar que:")
        print("      - El servidor esta caido")
        print("      - Tu firewall esta bloqueando")
        print("      - El servidor tiene el ping deshabilitado (normal en algunos servidores)")
    
    print()
    
    # Probar puerto
    print(f"2. Probando puerto {port}...")
    if test_port(host, port, timeout=10):
        print(f"   [OK] El puerto {port} esta abierto y accesible")
        print("   [OK] Deberias poder conectarte desde pgAdmin y Django")
    else:
        print(f"   [ERROR] El puerto {port} NO esta accesible")
        print("   [ADVERTENCIA] Posibles causas:")
        print("      - El firewall del servidor esta bloqueando el puerto")
        print("      - El servidor PostgreSQL no esta corriendo")
        print("      - Tu firewall local esta bloqueando la conexion")
        print("      - El servidor solo permite conexiones desde IPs especificas")
    
    print()
    print("-" * 50)
    print("Siguiente paso:")
    print("1. Intenta conectarte desde pgAdmin con los mismos datos")
    print("2. Si pgAdmin funciona, el problema esta en la configuracion de Django")
    print("3. Si pgAdmin NO funciona, verifica las credenciales y el acceso al servidor")
