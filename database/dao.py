from database.DB_connect import DBConnect
from model.artist import Artist
from model.connessioni import Connessioni
from model.traccia import Traccia


class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artists_album(n_album):


        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a.artist_id, COUNT(a.id)
                from album a 
                group by (a.artist_id )
                having COUNT(a.id)>=%s
                """
        cursor.execute(query,(n_album,))
        for row in cursor:

            result.append(row['artist_id'])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_generi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select a.artist_id as artist ,t.genre_id as genere 
                from track t , album a
                where t.album_id = a.id 
                group by a.artist_id ,t.genre_id 

                """
        cursor.execute(query)
        for row in cursor:
            result.append(Connessioni(**row))
        cursor.close()
        conn.close()
        return result