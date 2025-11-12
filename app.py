from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
app = Flask (__name__)
app.secret_key='TIAMIOSSOTT12'
API = "https://pokeapi.co/api/v2/pokemon/"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def buscaP():
    pokemon_name= request.form.get('pokemon_name',).strip().lower()
    
    if not pokemon_name:
        flash('por favor, ingresa un nombre de pokemon', 'error')
        return redirect(url_for('index'))
    
    try:
        resp = requests.get(f"{API}{pokemon_name}")
        if resp.status_code == 200:
            pokemon_data = resp.json()
            
            pokemon_info={
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'heigth': pokemon_data['heigth'],
                'weigth': pokemon_data['weigth'],
                'sprites': pokemon_data['sprites']['front_default'],
                'types': [t['type']['name'].title() for t in pokemon_data['type']],
                'abilities' : [a['ability']['name'].title() for a in pokemon_data['ability']]
            }
            return render_template('pokemon2.html', pokemon = pokemon_info)
        else:
            flash(f'pokemon"{pokemon_name}"no encontrado', 'error')
            return redirect(url_for(index))
        
    except requests.exceptions.RequestException as e:
        flash("error al buscar el pokemon", "error")
        return redirect(url_for(index))







if __name__ == "__main__":
    app.run(debug=True)