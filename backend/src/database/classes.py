from neo4j import GraphDatabase
import os
import dotenv
PERSON = 'Person'
TOWN = 'Town'
LIVES_IN = 'Lives in'

print(dotenv.load_dotenv(dotenv.find_dotenv()))
print(os.environ)
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_ADDR = os.environ.get("DB_ADDR")


class DBUser:
    def __init__(self, uri, user, password):
        print(uri)
        print(user)
        print(password)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    def _create_object(self, obj_type, **kwargs):
        labels = "{"
        for key in kwargs.keys():
            labels += str(key) + ': '
            labels += f'\'{kwargs[key]}\', '
        labels=labels[:-2] + '}'

        with self.driver.session() as session:
            session.run(f"CREATE (n:{obj_type} {labels})")
    
    #def _create_relationship(self, node_1, node_2):
    def _get_object(self, obj_type,  **kwargs):
        query = f"MATCH (a:{obj_type}), WHERE"
        for key in kwargs:
            query += f" a.{key} = \'{kwargs[key]}\' AND"

        query = query[-3] + "return a"
        with self.driver.session() as session:
            res = session.run(query)
        return res
        
    def get_person(self, **kwargs):
        return self._get_object(PERSON, **kwargs)

    def create_person(self, **kwargs):
        self._create_object(PERSON, **kwargs)

    def create_town(self, **kwargs):
        self._create_object(TOWN, **kwargs)

    #def move_person(self, id, town_id):


class DB_Node:
    db_user = DBUser(DB_ADDR, DB_USER, DB_PASS)

class Person(DB_Node):
    def __init__(self, id, first_name, family_name, wealth=0) -> None:
        super().__init__(id)
        self.first_name = first_name
        self.family_name = family_name
        self.wealth = wealth
    
    @classmethod
    def get(cls, **kwargs):
        cls.db_user.get_person()