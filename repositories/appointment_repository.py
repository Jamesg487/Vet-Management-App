from xmlrpc.client import DateTime, _datetime
from db.run_sql import run_sql
import datetime

from models.appointment import Appointment
import repositories.vet_repository as vet_repository
import repositories.pet_repository as pet_repository



def save(appointment):
    sql = "INSERT INTO appointments (pet_id, vet_id, date_time_start, date_time_end, appointment_notes) VALUES (%s, %s, %s, %s, %s) RETURNING *"
    values = [appointment.pet.id, appointment.vet.id, appointment.date_time_start, appointment.date_time_end, appointment.appointment_notes]
    results = run_sql( sql, values )
    appointment.id = results[0]['id']
    return appointment

def select_all():
    appointments = []

    sql = "SELECT * FROM appointments"
    results = run_sql(sql)
    for row in results:
        pet = pet_repository.select(row['pet_id'])
        vet = vet_repository.select(row['vet_id'])
        appointment = Appointment(pet, vet, row['date_time_start'], row['date_time_end'], row['appointment_notes'], row['id'])
        appointments.append(appointment)
    return appointments

def select(id):
    appointment = None
    sql = "SELECT * FROM appointments WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        pet = pet_repository.select(result['pet_id'])
        vet = vet_repository.select(result['vet_id'])
        appointment = Appointment(pet, vet, result['date_time_start'], result['date_time_end'], result['appointment_notes'], result['id'])
    return appointment

def delete_all():
    sql = "DELETE  FROM appointments"
    run_sql(sql)

def delete(id):
    sql = "DELETE  FROM appointments WHERE id = %s"
    values = [id]
    run_sql(sql, values)

def update(appointment):
    sql = "UPDATE appointments SET (pet_id, vet_id, date_time_start, date_time_end, appointment_notes) = (%s, %s, %s, %s, %s) WHERE id = %s"
    values = [appointment.pet.id, appointment.vet.id, appointment.date_time_start, appointment.date_time_end, appointment.appointment_notes, appointment.id]
    run_sql(sql, values)


def get_vet_appointment_times(vet_id):
    appointment_times = []

    sql = "SELECT * FROM appointments  WHERE vet_id = %s"
    values = [vet_id]
    results = run_sql(sql, values)
    for row in results:
        date_time_start = row['date_time_start']
        date_time_end =  row['date_time_end']
        datetime_appointment = f"{date_time_start} {date_time_end}"
        appointment_times.append(datetime_appointment)
    return appointment_times

