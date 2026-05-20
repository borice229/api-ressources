from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# -----------------------------------
# Fonction nettoyage colonnes
# -----------------------------------
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )
    return df


# -----------------------------------
# Charger les données
# -----------------------------------
df = pd.read_csv("data/ressources.csv", sep=",")

# Nettoyage colonnes
df = clean_columns(df)

# Debug
print(df.columns.tolist())


# -----------------------------------
# Route Home
# -----------------------------------
@app.route("/", methods=["GET"])
def home():
    return {
        "message": "API Ressources OK",
        "endpoints": [
            "/ressources",
            "/ressources/<matricule>",
            "/stats"
        ]
    }


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

    result = df[df["matricule"].astype(str) == str(matricule)]

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

        "types_contrat":
            df["type_de_contrat"]
            .value_counts()
            .to_dict(),

        "lieu_travail":
            df["lieu_travail"]
            .value_counts()
            .to_dict()
    }

    return jsonify(stats)


# -----------------------------------
# Run server
# -----------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)