from src.models.db import db

def primjer():
    
    # Primjer unosa podataka
    query = "INSERT INTO test (text) VALUES (?)"
    result = db.execute_query(query, ("Testni unos",)) # Obratite pozornost na zarez jer se ocekuje lista, python things ig
    print(result)

    # Primjer dohvaćanja jednog podatka
    result = db.fetch_one("SELECT * FROM test WHERE id = ?", (1,))
    print(result)

    # Primjer dohvaćanja svih podataka
    results = db.fetch_all("SELECT * FROM test")
    print(results)

    # Primjer dohvaćanja više podataka
    results = db.fetch_all("SELECT * FROM test WHERE id >= ? AND id <= ?", (1, 3))
    print(results)


if __name__ == "__main__":
    db.init_db()
    primjer()