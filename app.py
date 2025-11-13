from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'TIAMIOSSOTT12'

API_URL = "https://pokeapi.co/api/v2/pokemon/"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def buscaP():
    pokemon_name = request.form.get("pokemon_name", "").strip().lower()

    if not pokemon_name:
        flash("Por favor, ingresa un nombre de Pokémon", "error")
        return redirect(url_for("index"))

    try:
        response = requests.get(f"{API_URL}{pokemon_name}")

        if response.status_code == 200:
            pokemon_data = response.json()

            pokemon_info = {
                "name": pokemon_data["name"].title(),
                "id": pokemon_data["id"],
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"],
                "sprites": pokemon_data["sprites"]["front_default"],
                "types": [t["type"]["name"].title() for t in pokemon_data["types"]],
                "abilities": [a["ability"]["name"].title() for a in pokemon_data["abilities"]],
            }

            return render_template("resultado.html", pokemon=pokemon_info)

        else:
            flash(f'Pokémon "{pokemon_name}" no encontrado.', "error")
            return redirect(url_for("index"))

    except requests.exceptions.RequestException:
        flash("Error al conectar con la PokéAPI. Intenta de nuevo más tarde.", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
