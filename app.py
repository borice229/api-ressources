from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Charger les données une fois au démarrage
df = pd.read_csv("data/Ressources.csv", sep=",")

# Nettoyage simple
df.columns = [col.strip() for col in df.columns]


# -----------------------------------
# Endpoint 1 : toutes les ressources
# -----------------------------------
@app.route("/ressources", methods=["GET"])
def get_ressources():
    return jsonify(df.to_dict(orient="records"))


# -----------------------------------
# Endpoint 2 : filtrage par matricule
# -----------------------------------
@app.route("/ressources/<matricule>", methods=["GET"])
def get_by_matricule(matricule):
    result = df[df["Matricule"].astype(str) == str(matricule)]
    
    if result.empty:
        return jsonify({"message": "Matricule introuvable"}), 404

    return jsonify(result.to_dict(orient="records"))


# -----------------------------------
# Endpoint 3 : stats simples RH
# -----------------------------------
@app.route("/stats", methods=["GET"])
def get_stats():
    stats = {
        "nb_ressources": len(df),
        "types_contrat": df["Type de contrat"].value_counts().to_dict(),
        "lieu_travail": df["Lieu travail"].value_counts().to_dict()
    }
    return jsonify(stats)


# -----------------------------------
# Run server
# -----------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)