from db.run_sql import run_sql

from models.vet import Vet


def save(vet):
    sql = "INSERT INTO vets (name, species_specialism) VALUES (%s, %s) RETURNING *"
    values = [vet.name, vet.species_specialism]
    results = run_sql( sql, values )
    vet.id = results[0]['id']
    return vet

def select_all():
    vets = []

    sql = "SELECT * FROM vets"
    results = run_sql(sql)
    for row in results:
        vet = Vet(row['name'], row['species_specialism'], row['id'])
        vets.append(vet)
    return vets

def select(id):
    vet = None
    sql = "SELECT * FROM vets WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        vet = Vet(result['name'], result['species_specialism'], result['id'] )
    return vet

def delete_all():
    sql = "DELETE  FROM vets"
    run_sql(sql)

def delete(id):
    sql = "DELETE  FROM vets WHERE id = %s"
    values = [id]
    run_sql(sql, values)

def update(vet):
    sql = "UPDATE vets SET (name, species_specialism) = (%s, %s) WHERE id = %s"
    values = [vet.name, vet.species_specialism, vet.id]
    run_sql(sql, values)