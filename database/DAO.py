from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = {}
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """SELECT * from airports a order by a.AIRPORT asc"""

            cursor.execute(query)

            for row in cursor:
                result[row["ID"]] = (Airport(**row))

            cursor.close()
            conn.close()
        return result

    @staticmethod
    def get_dep_airlines(airportID):
        """
        :return: set di airlinesID che entrano nell'areoporto
        """
        conn = DBConnect.get_connection()
        result = set()
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select distinct(f.AIRLINE_ID)
                        from flights f
                        where f.ORIGIN_AIRPORT_ID = %s"""
            cursor.execute(query, (airportID,))
            for row in cursor:
                result.add(row[0])  # row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def get_arr_airlines(airportID):
        """
        :return: set di airlinesID che entrano nell'areoporto
        """
        conn = DBConnect.get_connection()
        result = set()
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select distinct(f.AIRLINE_ID)
                        from flights f
                        where f.DESTINATION_AIRPORT_ID  = %s"""
            cursor.execute(query, (airportID,))
            for row in cursor:
                result.add(row[0])  # row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def get_edge_weight(id1, id2):
        conn = DBConnect.get_connection()
        result = 0
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select count(*)
                        from flights f 
                        where f.ORIGIN_AIRPORT_ID = %s
                        and f.DESTINATION_AIRPORT_ID = %s"""
            cursor.execute(query, (id1, id2,))
            for row in cursor:
                result += (row[0])  # row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()

            cursor = conn.cursor()
            cursor.execute(query, (id2, id1,))
            for row in cursor:
                result += (row[0])  # row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

