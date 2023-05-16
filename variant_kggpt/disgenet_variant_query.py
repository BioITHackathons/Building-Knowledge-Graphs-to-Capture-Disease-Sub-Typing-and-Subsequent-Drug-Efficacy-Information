import sqlite3
import json
from collections import defaultdict
from utils import split_text, view_sqlitedb


DISGENET_DB_PATH = "choose the path"  # download from https://www.disgenet.org/downloads the db (DisGeNET SQLite 2020 - v7.0 or the latest version)


def query_all_variant(cursor, variant_id, print_results=True):
    # Execute an SQL command to SELECT rows with the specified variantID from variantAttributes table
    cursor.execute("SELECT variantNID FROM variantAttributes WHERE variantId=?", (variant_id,))

    # Fetch the first row (assuming variantID is unique)
    row = cursor.fetchone()

    if row is not None:
        # Extract the variantNID
        variant_nid = row[0]

        # Execute an SQL command to SELECT rows with the extracted variantNID from variantDiseaseNetwork table
        cursor.execute(
            """
            SELECT da.diseaseId, da.diseaseName, va.variantId, ga.geneId, ga.geneName,
                vdn.source, vdn.association, vdn.associationType, vdn.sentence, vdn.pmid,
                vdn.score, vdn.EI, vdn.year
            FROM variantDiseaseNetwork AS vdn
            JOIN diseaseAttributes AS da ON vdn.diseaseNID = da.diseaseNID
            JOIN variantGene AS vg ON vdn.variantNID = vg.variantNID
            JOIN geneAttributes AS ga ON vg.geneNID = ga.geneNID
            JOIN variantAttributes AS va ON vdn.variantNID = va.variantNID
            WHERE vdn.variantNID=?
        """,
            (variant_nid,),
        )

        # Fetch all rows as a list of tuples
        rows = cursor.fetchall()

        # Define columns to include in JSON output
        columns = [
            "diseaseID",
            "diseaseName",
            "variantID",
            "geneID",
            "geneName",
            "source",
            "association",
            "associationType",
            "sentence",
            "pmid",
            "score",
            "EI",
            "year",
        ]

        # Convert the rows to a list of dictionaries with column names as keys
        results = [dict(zip(columns, row)) for row in rows]

        # Convert the list of dictionaries to a JSON string
        json_results = json.dumps(results, indent=2)

        # Print the JSON string
        if print_results:
            print(json_results)
        return json_results
    else:
        print("No matching variantNID found for the given variantID")
        return None


def get_evidences(cursor, variant_id):
    # Execute an SQL command to SELECT rows with the specified variantID from variantAttributes table
    cursor.execute("SELECT variantNID FROM variantAttributes WHERE variantId=?", (variant_id,))

    # Fetch the first row (assuming variantID is unique)
    row = cursor.fetchone()

    if row is not None:
        # Extract the variantNID
        variant_nid = row[0]

        # Execute an SQL command to SELECT rows with the extracted variantNID from variantDiseaseNetwork table
        cursor.execute(
            """
            SELECT vdn.pmid, vdn.year, vdn.sentence
            FROM variantDiseaseNetwork AS vdn
            JOIN diseaseAttributes AS da ON vdn.diseaseNID = da.diseaseNID
            JOIN variantGene AS vg ON vdn.variantNID = vg.variantNID
            JOIN geneAttributes AS ga ON vg.geneNID = ga.geneNID
            JOIN variantAttributes AS va ON vdn.variantNID = va.variantNID
            WHERE vdn.variantNID=?
        """,
            (variant_nid,),
        )

        # Fetch all rows as a list of tuples
        rows = cursor.fetchall()

        # Define columns to include in JSON output
        columns = ["pmid", "year", "sentence"]

        # Convert the rows to a list of dictionaries with column names as keys
        results = [dict(zip(columns, row)) for row in rows]

        # Convert the list of dictionaries to a JSON string
        json_results = json.dumps(results, indent=2)

        # Print the JSON string
        print(json_results)
        return json_results
    else:
        print("No matching variantNID found for the given variantID")
        return None


def get_disease_varaint_gene_graph(cursor, variant_id):
    # Execute an SQL command to SELECT rows with the specified variantID from variantAttributes table
    cursor.execute("SELECT variantNID FROM variantAttributes WHERE variantId=?", (variant_id,))

    # Fetch the first row (assuming variantID is unique)
    row = cursor.fetchone()

    if row is not None:
        # Extract the variantNID
        variant_nid = row[0]

        # Execute an SQL command to SELECT rows with the extracted variantNID from variantDiseaseNetwork table
        cursor.execute(
            """
            SELECT da.diseaseId, da.diseaseName, va.variantId, ga.geneId, ga.geneName,
                vdn.source, vdn.association, vdn.associationType, vdn.sentence, vdn.pmid,
                vdn.score, vdn.EI, vdn.year
            FROM variantDiseaseNetwork AS vdn
            JOIN diseaseAttributes AS da ON vdn.diseaseNID = da.diseaseNID
            JOIN variantGene AS vg ON vdn.variantNID = vg.variantNID
            JOIN geneAttributes AS ga ON vg.geneNID = ga.geneNID
            JOIN variantAttributes AS va ON vdn.variantNID = va.variantNID
            WHERE vdn.variantNID=?
        """,
            (variant_nid,),
        )

        # Fetch all rows as a list of tuples
        rows = cursor.fetchall()

        # Create a directed graph
        # Create a directed graph
        graph = Digraph(engine="dot")
        graph.attr(rankdir="LR")
        graph.attr(fontsize="10")
        graph.attr(nodesep="0.5", ranksep="2")
        graph.attr(concentrate="true")

        variant_gene_count = defaultdict(int)
        gene_disease_count = defaultdict(int)
        for row in rows:
            disease_id, _, variant_id, gene_id, _, _, _, _, _, _, _, _, _ = row
            variant_gene_count[(variant_id, gene_id)] += 1
            gene_disease_count[(gene_id, disease_id)] += 1

        for row in rows:
            disease_id, disease_name, variant_id, gene_id, gene_name, _, _, _, _, _, _, _, _ = row

            disease_label = f"Disease: {split_text(disease_name)} ({disease_id})"
            graph.node(f"disease_{disease_id}", disease_label, shape="ellipse", style="filled", fillcolor="lightblue")
            graph.node(
                f"variant_{variant_id}", f"Variant: {variant_id}", shape="ellipse", style="filled", fillcolor="lightgreen"
            )
            graph.node(
                f"gene_{gene_id}", f"Gene: {gene_name} ({gene_id})", shape="ellipse", style="filled", fillcolor="lightyellow"
            )

            edge_width = str(variant_gene_count[(variant_id, gene_id)] ** 0.5)
            graph.edge(f"variant_{variant_id}", f"gene_{gene_id}", penwidth=edge_width)

            edge_width = str(gene_disease_count[(gene_id, disease_id)])
            graph.edge(f"gene_{gene_id}", f"disease_{disease_id}", penwidth=edge_width)

        # Save the graph as a PNG image
        graph.render("graph_output", format="png", cleanup=True)

        print(f"Graph saved as 'graph_{variant_id}.png'")
    else:
        print("No matching variantNID found for the given variantID")


if __name__ == "__main__":
    variant_id = "rs6003"
    db_file = DISGENET_DB_PATH
    conn = sqlite3.connect(db_file)

    # Create a cursor object
    cursor = conn.cursor()
    view_sqlitedb(cursor)
    evidences = get_evidences(cursor, variant_id)
    print(evidences)

    get_disease_varaint_gene_graph(cursor, variant_id)

    conn.close()
