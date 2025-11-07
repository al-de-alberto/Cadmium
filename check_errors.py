"""
Script para revisar y depurar el código buscando errores comunes
"""
import os
import re
import sys

def check_python_files():
    """Revisa archivos Python para errores comunes"""
    errors = []
    
    # Verificar imports
    python_files = [
        'core/models.py',
        'core/views.py',
        'core/forms.py',
        'core/admin.py',
    ]
    
    for file_path in python_files:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            # Buscar problemas comunes
            for i, line in enumerate(lines, 1):
                # Verificar referencias a métodos que podrían no existir
                if 'es_administrador()' in line:
                    errors.append(f"{file_path}:{i} - Uso de es_administrador() como método (debe ser property)")
                
                # Verificar referencias a campos deprecated
                if '.rol ==' in line and 'usuario' in line.lower():
                    errors.append(f"{file_path}:{i} - Posible uso del campo 'rol' deprecated")
    
    return errors

def check_templates():
    """Revisa templates para errores comunes"""
    errors = []
    warnings = []
    
    templates_dir = 'templates/core'
    if not os.path.exists(templates_dir):
        return errors, warnings
    
    for filename in os.listdir(templates_dir):
        if not filename.endswith('.html'):
            continue
            
        file_path = os.path.join(templates_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # Verificar uso de _es_administrador en templates (no permitido)
                if '._es_administrador' in line:
                    errors.append(f"{file_path}:{i} - Uso de _es_administrador en template (usar es_administrador)")
                
                # Verificar uso de es_administrador() como método
                if 'es_administrador()' in line:
                    errors.append(f"{file_path}:{i} - Uso de es_administrador() como método en template")
                
                # Verificar referencias a get_rol_display (debe ser get_roles_display)
                if 'get_rol_display' in line and 'get_roles_display' not in line:
                    errors.append(f"{file_path}:{i} - Uso de get_rol_display (debe ser get_roles_display)")
                
                # Verificar bloques style inline
                if '<style>' in line:
                    warnings.append(f"{file_path}:{i} - Bloque <style> inline encontrado (mover a CSS)")
    
    return errors, warnings

def check_model_consistency():
    """Verifica consistencia del modelo"""
    errors = []
    
    with open('core/models.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Verificar que el property es_administrador esté definido
        if '@property' not in content or 'def es_administrador(self):' not in content:
            errors.append("core/models.py - Property es_administrador no encontrada")
        
        # Verificar que _es_administrador esté definido como campo
        if '_es_administrador = models.BooleanField' not in content:
            errors.append("core/models.py - Campo _es_administrador no encontrado")
    
    return errors

def main():
    """Función principal"""
    print("=" * 60)
    print("REVISIÓN Y DEPURACIÓN DEL CÓDIGO")
    print("=" * 60)
    print()
    
    all_errors = []
    all_warnings = []
    
    # Revisar archivos Python
    print("1. Revisando archivos Python...")
    python_errors = check_python_files()
    all_errors.extend(python_errors)
    
    # Revisar templates
    print("2. Revisando templates...")
    template_errors, template_warnings = check_templates()
    all_errors.extend(template_errors)
    all_warnings.extend(template_warnings)
    
    # Revisar modelo
    print("3. Revisando consistencia del modelo...")
    model_errors = check_model_consistency()
    all_errors.extend(model_errors)
    
    # Mostrar resultados
    print()
    print("=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    print()
    
    if all_errors:
        print(f"❌ ERRORES ENCONTRADOS: {len(all_errors)}")
        print("-" * 60)
        for error in all_errors:
            print(f"  • {error}")
        print()
    else:
        print("✅ No se encontraron errores críticos")
        print()
    
    if all_warnings:
        print(f"⚠️  ADVERTENCIAS: {len(all_warnings)}")
        print("-" * 60)
        for warning in all_warnings[:20]:  # Mostrar solo las primeras 20
            print(f"  • {warning}")
        if len(all_warnings) > 20:
            print(f"  ... y {len(all_warnings) - 20} más")
        print()
    
    print("=" * 60)
    
    return len(all_errors) == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

