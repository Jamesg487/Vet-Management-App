from flask import Flask, render_template, request, redirect
from flask import Blueprint
from models.vet import Vet
from datetime import datetime
import repositories.vet_repository as vet_repository
import repositories.appointment_repository as appointment_repository

vets_blueprint = Blueprint("vets", __name__)

@vets_blueprint.route("/vets")
def vets():
    vets = vet_repository.select_all()
    return render_template("vets/index.html", vets = vets)

@vets_blueprint.route("/vets/new")
def new_vet():
    return render_template("vets/new.html")

@vets_blueprint.route("/vets",  methods=['POST'])
def create_vet():
    name = request.form['name']
    species_specialism = request.form['species_specialism']
    vet = Vet(name, species_specialism)
    vet_repository.save(vet)
    return redirect('/vets')

@vets_blueprint.route("/vets/<id>")
def show_vet(id):
    vet = vet_repository.select(id)
    pets = vet_repository.pets_registered(vet)
    appointments = vet_repository.appointments(vet)
    for appointment in appointments:
        if appointment.date_time_start < datetime.today():
            appointment_repository.delete(appointment.id)
    appointments = vet_repository.appointments(vet)
    return render_template('vets/show.html', vet=vet, pets=pets, appointments=appointments)

@vets_blueprint.route("/vets/<id>/edit")
def edit_vet(id):
    vet = vet_repository.select(id)
    return render_template('vets/edit.html', vet=vet)

@vets_blueprint.route("/vets/<id>",  methods=['POST'])
def update_vet(id):
    name = request.form['name']
    species_specialism = request.form['species_specialism']
    vet = Vet(name, species_specialism, id)
    vet_repository.update(vet)
    return redirect('/vets')

@vets_blueprint.route("/vets/<id>/delete", methods=['POST'])
def delete(id):
    vet_repository.delete(id)
    return redirect('/vets')