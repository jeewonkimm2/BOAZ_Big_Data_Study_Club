import time
from argparse import ArgumentParser

import pandas as pd
import psycopg2
from sklearn.datasets import load_breast_cancer



# def get_data():
#     df = pd.DataFrame(data = load_breast_cancer().data, columns = load_breast_cancer().feature_names)
#     df['label'] = load_breast_cancer().target
#     return df

def get_data():
    X, y = load_breast_cancer(return_X_y=True, as_frame=True)
    df = pd.concat([X, y], axis="columns")
    rename_rule = {
        "mean radius": "mean_radius",
        "mean texture": "mean_texture",
        "mean perimeter": "mean_perimeter",
        "mean area": "mean_area",
        "mean smoothness":"mean_smoothness",
        "mean compactness":"mean_compactness",
        "mean concavity":"mean_concavity",
        "mean concave points":"mean_concave_points",
        "mean symmetry":"mean_symmetry",
        "mean fractal dimension":"mean_fractal_dimension",
        "radius error":"standard_error_radius",
        "texture error":"standard_error_texture",
        "perimeter error":"standard_error_perimeter",
        "area error":"standard_error_area",
        "smoothness error":"standard_error_smoothness",
        "compactness error":"standard_error_compactness",
        "concavity error":"standard_error_concavity",
        "concave points error":"standard_error_concave_points",
        "symmetry error":"standard_error_symmetry",
        "fractal dimension error":"standard_error_fractal_dimension",
        "worst radius":"worst_radius",
        "worst texture":"worst_texture",
        "worst perimeter":"worst_perimeter",
        "worst area":"worst_area",
        "worst smoothness":"worst_smoothness",
        "worst compactness":"worst_compactness",
        "worst concavity":"worst_concavity",
        "worst concave points":"worst_concave_points",
        "worst symmetry":"worst_symmetry",
        "worst fractal dimension":"worst_fractal_dimension"
    }
    df = df.rename(columns=rename_rule)
    return df


# id SERIAL PRIMARY KEY,
# timestamp timestamp,
def create_table(db_connect):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS breast_cancer (
        id SERIAL PRIMARY KEY,
        timestamp timestamp,
        mean_radius float8,
        mean_texture float8,
        mean_perimeter float8,
        mean_area float8,
        mean_smoothness float8,
        mean_compactness float8,
        mean_concavity float8,
        mean_concave_points float8,
        mean_symmetry float8,
        mean_fractal_dimension float8,
        standard_error_radius float8,
        standard_error_texture float8,
        standard_error_perimeter float8,
        standard_error_area float8,
        standard_error_smoothness float8,
        standard_error_compactness float8,
        standard_error_concavity float8,
        standard_error_concave_points float8,
        standard_error_symmetry float8,
        standard_error_fractal_dimension float8,
        worst_radius float8,
        worst_texture float8,
        worst_perimeter float8,
        worst_area float8,
        worst_smoothness float8,
        worst_compactness float8,
        worst_concavity float8,
        worst_concave_points float8,
        worst_symmetry float8,
        worst_fractal_dimension float8,
        target int
    );"""
    print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()

def insert_data(db_connect, data):
    insert_row_query = f"""
    INSERT INTO breast_cancer
        (timestamp,mean_radius, mean_texture, mean_perimeter, mean_area, mean_smoothness,mean_compactness,
        mean_concavity,mean_concave_points,mean_symmetry,mean_fractal_dimension,standard_error_radius,
        standard_error_texture,standard_error_perimeter,standard_error_area,standard_error_smoothness,
        standard_error_compactness,standard_error_concavity,standard_error_concave_points,standard_error_symmetry,
        standard_error_fractal_dimension,worst_radius,worst_texture,worst_perimeter,worst_area,
        worst_smoothness,worst_compactness,worst_concavity,worst_concave_points,worst_symmetry,worst_fractal_dimension,
        target)
        VALUES (
            NOW(),
            {data.mean_radius},
            {data.mean_texture},
            {data.mean_perimeter},
            {data.mean_area},{data.mean_smoothness},{data.mean_compactness},{data.mean_concavity},{data.mean_concave_points},{data.mean_symmetry},{data.mean_fractal_dimension},
            {data.standard_error_radius},{data.standard_error_texture},{data.standard_error_perimeter},{data.standard_error_area},{data.standard_error_smoothness},{data.standard_error_compactness},{data.standard_error_concavity},
            {data.standard_error_concave_points},{data.standard_error_symmetry},{data.standard_error_fractal_dimension},{data.worst_radius},
            {data.worst_texture},{data.worst_perimeter},{data.worst_area},{data.worst_smoothness},{data.worst_compactness},
            {data.worst_concavity},{data.worst_concave_points},{data.worst_symmetry},{data.worst_fractal_dimension},{data.target}
        );
    """
    print(insert_row_query)
    with db_connect.cursor() as cur:
        cur.execute(insert_row_query)
        db_connect.commit()
        
def generate_data(db_connect, df):
    while True:
        insert_data(db_connect, df.sample(1).squeeze())
        time.sleep(1)
        
        
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--db-host", dest="db_host", type=str, default="localhost")
    args = parser.parse_args()

    db_connect = psycopg2.connect(
        user="jeewonuser",
        password="jeewonpassword",
        host=args.db_host,
        port=5432,
        database="jeewondatabase",
    )
    create_table(db_connect)
    df = get_data()
    generate_data(db_connect, df)