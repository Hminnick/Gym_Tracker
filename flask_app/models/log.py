from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

# how to make it so that they can have as many sets as they want instead of a set amount?
# how to add user posted pictures as well as pictures included in logs
class Log:
    db = 'gym_tracker'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.weight = db_data['weight']
        self.description = db_data['description']
        self.exercise_name = db_data['exercise_name']
        self.exercise_sets = db_data['exercise_sets']
        self.exercise_set_1 = db_data['exercise_set_1']
        self.exercise_set_2 = db_data['exercise_set_2']
        self.exercise_set_3 = db_data['exercise_set_3']
        self.exercise_set_4 = db_data['exercise_set_4']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        if 'first_name' in db_data:
            self.posted_by = db_data['first_name'] + db_data['last_name']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO logs (weight, description, exercise_name, exercise_sets, exercise_set_1, exercise_set_2, exercise_set_3, exercise_set_4) VALUES (%(weight)s, %(description)s, %(exercise_name)s, %(exercise_sets)s, %(exercise_set_1)s, %(exercise_set_2)s, %(exercise_set_3)s, %(exercise_set_4)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM logs;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_logs = []
        for row in results:
            all_logs.append( cls(row) )
        return all_logs

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM logs JOIN users ON logs.user_id = users.id WHERE logs.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls( results[0] )
        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE logs SET weight = %(weight)s, description = %(description)s, exercise_name = %(exercise_name)s, exercise_sets = %(exercise_sets)s, exercise_set_1 = %(exercise_set_1)s, exercise_set_2 = %(exercise_set_2)s, exercise_set_3 = %(exercise_set_3)s, exercise_set_4 = %(exercise_set_4)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM logs WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_log(log):
        is_valid = True
        if log['weight'] == "":
            is_valid = False
            flash("Log must include weight even if it was 0!","log")
        if len(log['exercise_name']) < 2:
            is_valid = False
            flash("Log's name must be at least 2 characters!","log")
        if log['reps'] == "":
            is_valid = False
            flash("Log must include number of reps!","log")
        return is_valid