"""
Comando de Django para actualizar los horarios de asistencia según el turno
Ejecutar con: python manage.py update_asistencia_horarios
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from core.models import Asistencia


class Command(BaseCommand):
    help = 'Actualiza los horarios de entrada y salida de los registros de asistencia según su turno'

    def handle(self, *args, **options):
        # Mapear turno a horas de entrada y salida (horario chileno GMT-3)
        horarios_turno = {
            'apertura': {'entrada': '09:00', 'salida': '13:00'},
            'tarde': {'entrada': '13:00', 'salida': '17:00'},
            'cierre': {'entrada': '17:00', 'salida': '21:00'}
        }
        
        # Obtener todos los registros de asistencia que tengan un turno asignado
        asistencias = Asistencia.objects.filter(turno__isnull=False).exclude(turno='')
        
        actualizados = 0
        sin_turno = 0
        
        for asistencia in asistencias:
            turno = asistencia.turno
            if turno in horarios_turno:
                horario = horarios_turno[turno]
                hora_entrada = datetime.strptime(horario['entrada'], '%H:%M').time()
                hora_salida = datetime.strptime(horario['salida'], '%H:%M').time()
                
                # Actualizar las horas
                asistencia.hora_entrada = hora_entrada
                asistencia.hora_salida = hora_salida
                asistencia.save()
                actualizados += 1
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Actualizado: {asistencia.usuario.username} - {asistencia.fecha} - '
                        f'Turno: {asistencia.get_turno_display()} - '
                        f'Entrada: {hora_entrada} - Salida: {hora_salida}'
                    )
                )
            else:
                sin_turno += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Turno no reconocido: {asistencia.usuario.username} - {asistencia.fecha} - '
                        f'Turno: {turno}'
                    )
                )
        
        # Actualizar registros sin turno pero con hora_entrada (basado en la hora de entrada existente)
        asistencias_sin_turno = Asistencia.objects.filter(
            turno__isnull=True
        ) | Asistencia.objects.filter(turno='')
        
        for asistencia in asistencias_sin_turno:
            if asistencia.hora_entrada:
                hora_str = asistencia.hora_entrada.strftime('%H:%M')
                # Intentar determinar el turno basado en la hora de entrada
                if hora_str == '09:00':
                    asistencia.turno = 'apertura'
                    asistencia.hora_entrada = datetime.strptime('09:00', '%H:%M').time()
                    asistencia.hora_salida = datetime.strptime('13:00', '%H:%M').time()
                elif hora_str == '13:00':
                    asistencia.turno = 'tarde'
                    asistencia.hora_entrada = datetime.strptime('13:00', '%H:%M').time()
                    asistencia.hora_salida = datetime.strptime('17:00', '%H:%M').time()
                elif hora_str == '17:00':
                    asistencia.turno = 'cierre'
                    asistencia.hora_entrada = datetime.strptime('17:00', '%H:%M').time()
                    asistencia.hora_salida = datetime.strptime('21:00', '%H:%M').time()
                else:
                    # Si no coincide con ningún turno, asignar apertura por defecto
                    asistencia.turno = 'apertura'
                    asistencia.hora_entrada = datetime.strptime('09:00', '%H:%M').time()
                    asistencia.hora_salida = datetime.strptime('13:00', '%H:%M').time()
                
                asistencia.save()
                actualizados += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Actualizado (sin turno previo): {asistencia.usuario.username} - {asistencia.fecha} - '
                        f'Turno: {asistencia.get_turno_display()} - '
                        f'Entrada: {asistencia.hora_entrada} - Salida: {asistencia.hora_salida}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nProceso completado:\n'
                f'   - Registros actualizados: {actualizados}\n'
                f'   - Turnos no reconocidos: {sin_turno}\n'
                f'   - Total procesado: {asistencias.count() + asistencias_sin_turno.count()}'
            )
        )

