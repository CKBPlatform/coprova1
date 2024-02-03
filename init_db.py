# Module Imports
import sys
import mysql.connector

# Connect to MariaDB Platform
try:
    conn = mysql.connector.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306
    )
except mysql.connector.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
cur.execute("DROP DATABASE IF EXISTS ckb_platform;") 
cur.execute("CREATE DATABASE ckb_platform;")
cur.execute("USE ckb_platform;")
#cur.execute("grant all privileges on ckb_platform.* TO 'root'@'localhost' identified by 'root';") 
#cur.execute("flush privileges;") 

##CREATE USER TABLE
cur.execute("""
            CREATE TABLE users (
            id UUID NOT NULL DEFAULT UUID() PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            score INT NOT NULL DEFAULT '0',
            type VARCHAR(10) NOT NULL DEFAULT 'invalid',
            educator BOOL NOT NULL DEFAULT 0
);""")

cur.execute("""
            CREATE TABLE mails (
            id UUID NOT NULL DEFAULT UUID() PRIMARY KEY,
            type VARCHAR(50) NOT NULL DEFAULT 'activation',
            code VARCHAR(50) NOT NULL,
            user_id UUID NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
);""")




##CREATE TORUNAMENT TABLE
cur.execute("""
            CREATE TABLE tournaments (
            id UUID NOT NULL DEFAULT UUID() PRIMARY KEY,
            tournament_name VARCHAR(50) NOT NULL,
            tournament_description VARCHAR(50) NOT NULL,
            deadline_subscription  VARCHAR(50) NOT NULL DEFAULT CURDATE(),
            creator_id UUID NOT NULL,  
            FOREIGN KEY (creator_id) REFERENCES users(id),
            status VARCHAR(50) NOT NULL DEFAULT 'created'
);""")


##CREATE KATA-BATTLE TABLE
cur.execute("""
            CREATE TABLE katabattles (
            id UUID NOT NULL DEFAULT UUID() PRIMARY KEY,
            battle_name VARCHAR(50) NOT NULL,
            link_github VARCHAR (500) DEFAULT "NOT CREATED YET",
            deadline_subscription VARCHAR(50) NOT NULL DEFAULT CURDATE(),
            deadline_battle VARCHAR(50) NOT NULL DEFAULT CURDATE(),
            min_partecipants INT NOT NULL DEFAULT '1',
            max_partecipants INT NOT NULL DEFAULT '1',
            file VARCHAR(500) NOT NULL,
            manual_evaluation BOOL NOT NULL DEFAULT 0,
            creator_id UUID NOT NULL,  
            tournament_id UUID NOT NULL,
            FOREIGN KEY (creator_id) REFERENCES users(id),
            FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
            status VARCHAR(50) NOT NULL DEFAULT 'created'
);""")

##CREATE BELONGS RELATIONSHIPS
cur.execute("""
            CREATE TABLE belongs (
            user_id UUID NOT NULL,
            tournament_id UUID NOT NULL,
            PRIMARY KEY (user_id, tournament_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
);""")


cur.execute("""
            CREATE TABLE teams (
            id UUID NOT NULL DEFAULT UUID() PRIMARY KEY,
            team_score VARCHAR(50) NOT NULL DEFAULT '0',
            team_name VARCHAR(50) NOT NULL
);""")

cur.execute("""
            CREATE TABLE notifications (
            id UUID NOT NULL DEFAULT UUID() PRIMARY KEY,
            type VARCHAR(50) NOT NULL,
            text VARCHAR(200) NOT NULL,
            id_reference VARCHAR(50) NOT NULL DEFAULT '0',
            user_id UUID NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
);""")

#cur.execute("""
#            CREATE TABLE notifies (
#            user_id UUID NOT NULL,
#            notification_id UUID NOT NULL,
#            PRIMARY KEY (user_id, notification_id),
#            FOREIGN KEY (user_id) REFERENCES users (id),
#            FOREIGN KEY (notification_id) REFERENCES notifications (id)
#);""")


cur.execute("""
            CREATE TABLE team_battles (
            id UUID NULL DEFAULT UUID(),
            team_id UUID NOT NULL,
            battle_id UUID NOT NULL,
            account_name VARCHAR(100) NOT NULL,
            team_score VARCHAR(50) NOT NULL DEFAULT '0',
            PRIMARY KEY (id),
            FOREIGN KEY (team_id) REFERENCES teams(id),
            FOREIGN KEY (battle_id) REFERENCES katabattles(id)
);""")


cur.execute("""
            CREATE TABLE team_partecipants(
            user_id UUID NOT NULL,
            team_id UUID NOT NULL,
            PRIMARY KEY (user_id, team_id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (team_id) REFERENCES teams (id)
);""")

cur.execute("""
            CREATE TABLE tournaments_permission(
            id UUID NOT NULL DEFAULT UUID() PRIMARY KEY,
            user_id UUID NOT NULL,
            tournament_id UUID NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
);""")


cur.execute("""INSERT INTO `users` 
            (name, surname, email, password) VALUES 
            ('Test', 'User', 'test@example.it', 'test')
;""")


cur.execute("""INSERT INTO `users` 
            (name, surname, email, password, score) VALUES 
            ('Triulu', 'A', 'a@example.it', 'test', 10)
;""")

cur.execute("""INSERT INTO `users` 
            (name, surname, email, password, score) VALUES 
            ('Malanova', 'B', 'b@example.it', 'test', 20)
;""")

cur.execute("""INSERT INTO `users` 
            (name, surname, email, password, score, educator) VALUES 
            ('Scuntintizza', 'C', 'c@example.it', 'test', 30, 1)
;""")


conn.commit()