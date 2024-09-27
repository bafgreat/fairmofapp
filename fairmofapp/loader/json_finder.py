import os
import json
from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC
import streamlit as st


def get_schema():
    """
    Defines the schema for the Whoosh index.

    The schema includes fields like:
    - refcode: a unique reference code (TEXT)
    - PLD: pore limiting diameter (NUMERIC)
    - LCD: largest cavity diameter (NUMERIC)
    - ASA: accessible surface area (NUMERIC)
    - AV: accessible volume (NUMERIC)
    - n_channel: number of channels (NUMERIC)
    - void_fraction: void fraction (NUMERIC)
    - metal: metals involved in the MOF (TEXT)
    - metal_symbols: symbols of metals involved in the MOF (TEXT)
    - ligand_inchi: InChI of ligands (TEXT)
    - ligand_smile: SMILES of ligands (TEXT)
    - chemical_name: chemical name (TEXT)
    - sbu type: the topology of sbu (TEXT)
    - color: color of MOF (TEXT)
    - topology: topology of MOF (TEXT)
    - id: unique identifier (NUMERIC)
    - iupac name: iupac name (TEXT)
    - doi: doi (TEXT)

    **returns:**
        - Schema: The defined Whoosh schema.
    """
    return Schema(
        refcode=TEXT(stored=True),
        PLD=NUMERIC(stored=True),
        LCD=NUMERIC(stored=True),
        ASA=NUMERIC(stored=True),
        AV=NUMERIC(stored=True),
        n_channel=NUMERIC(stored=True),
        void_fraction=NUMERIC(stored=True),
        metal=TEXT(stored=True),
        metal_symbols=TEXT(stored=True),
        ligand_inchi=TEXT(stored=True),
        ligand_smile=TEXT(stored=True),
        chemical_name=TEXT(stored=True),
        sbu_type=TEXT(stored=True),
        color=TEXT(stored=True),
        topology=TEXT(stored=True),
        id=NUMERIC(stored=True),
        iupac_name=TEXT(stored=True),
        doi=TEXT(stored=True)
    )


def safe_join(value):
    """
    Safely joins list items into a string, or returns the value if it's already a string.

    **parameter:**
        - value (list or str or None): The value to be joined, which can be a list of strings,
                                       a single string, or None.

    **returns:**
        str: A comma-separated string if value is a list, or the original string if value is
             a string. If value is None, returns an empty string.
    """
    if isinstance(value, list):
        return ','.join(value)
    elif isinstance(value, str):
        return value
    elif isinstance(value, float):
        return value
    elif isinstance(value, int):
        return value
    else:
        return ''


def create_index(json_dir, index_dir):
    """
    Creates a Whoosh index from a directory of JSON files.

    Reads JSON files from the `json_dir`, extracts relevant data, and indexes them using Whoosh.
    The index is stored in `index_dir`.

    **parameters:**
        json_dir (str): Path to the directory containing JSON files.
        index_dir (str): Path to the directory where the index will be created.

    **returns:**
        None
    """
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    idx = index.create_in(index_dir, get_schema())

    with idx.writer() as writer:
        for filename in os.listdir(json_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(json_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for refcode, properties in data.items():
                        if isinstance(properties, dict):
                            # Exclude experimental cif and GFN-xtb optimised cif from indexing
                            # Get numeric fields
                            pld = properties.get("PLD", 0)
                            lcd = properties.get("LCD", 0)
                            asa = properties.get("ASA", 0)
                            av = properties.get("AV", 0)
                            n_channel = properties.get("Number of channels", 0)
                            void_fraction = properties.get("Void fraction", 0)
                            mof_id = properties.get("id", 0)


                            # Get text fields
                            metal = safe_join(properties.get("metals", []))
                            metal_symbols = safe_join(properties.get("metals symbols", []))  # Ensuring consistent field name
                            ligand_inchi = safe_join(properties.get("ligand inchikey", []))
                            ligand_smile = safe_join(properties.get("ligand smiles", []))
                            chemical_name = safe_join(properties.get("chemical name", []))
                            sbu_type = safe_join(properties.get("sbu type", []))
                            color = safe_join(properties.get("color", []))
                            topology = safe_join(properties.get("topology", []))
                            iupac_name = safe_join(properties.get("iupac name", []))
                            doi = safe_join(properties.get("doi", []))
                            # Print progress
                            print(f"Indexing PLD: {pld} for {refcode}")
                            # Add document to index
                            writer.add_document(
                                refcode=refcode,
                                PLD=pld,
                                LCD=lcd,
                                ASA=asa,
                                AV=av,
                                n_channel=n_channel,
                                void_fraction=void_fraction,
                                metal=metal,
                                metal_symbols=metal_symbols,
                                ligand_inchi=ligand_inchi,
                                ligand_smile=ligand_smile,
                                chemical_name=chemical_name,
                                sbu_type=sbu_type,
                                color=color,
                                topology=topology,
                                id=mof_id,
                                iupac_name=iupac_name,
                                doi=doi

                            )
                        else:
                            print(f"Skipping {refcode} because it is not a dictionary.")
    print("Index created successfully.")


# Call create_index function with your JSON files directory and index directory
create_index("../../data/compiled_json", "../../data/index_dir")
