from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas

app = FastAPI()

host_name = "52.2.83.96"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_seguros3"

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        return mydb
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database connection error: {err}")

# Get all claims
@app.get("/claims")
def get_claims():
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM siniestros2")
        result = cursor.fetchall()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mydb.close()
    return {"claims": result}

# Get a claim by ID
@app.get("/claims/{id}")
def get_claim(id: int):
    try:
        mydb = get_db_connection()
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM siniestros2 WHERE id = %s", (id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Claim not found")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mydb.close()
    return {"claim": result}

# Add a new claim
@app.post("/claims")
def add_claim(item: schemas.Claim):
    try:
        mydb = get_db_connection()
        poliza_id = item.poliza_id
        descripcion = item.descripcion
        monto = item.monto
        cursor = mydb.cursor()
        sql = "INSERT INTO siniestros2 (poliza_id, descripcion, monto) VALUES (%s, %s, %s)"
        val = (poliza_id, descripcion, monto)
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mydb.close()
    return {"message": "Claim added successfully"}
