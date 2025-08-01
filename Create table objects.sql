CREATE TABLE rugby.competitors (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(100),
    country_code VARCHAR(10),
    abbreviation VARCHAR(10),
    gender VARCHAR(10)
);

CREATE TABLE rugby.competitions (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10)
);

CREATE TABLE rugby.seasons (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    year INT,
    competition_id VARCHAR(50),
    FOREIGN KEY (competition_id) REFERENCES competitions(id)
);

CREATE TABLE rugby.sport_events (
    id VARCHAR(50) PRIMARY KEY,
    start_time DATETIME,
    start_time_confirmed BOOLEAN,
    season_id VARCHAR(50),
    stage_type VARCHAR(50),
    stage_phase VARCHAR(50),
    stage_start_date DATE,
    stage_end_date DATE,
    round_number INT,
    group_id VARCHAR(50),
    group_name VARCHAR(100),
    FOREIGN KEY (season_id) REFERENCES seasons(id)
);

CREATE TABLE rugby.event_competitors (
    sport_event_id VARCHAR(50),
    competitor_id VARCHAR(50),
    qualifier VARCHAR(10), -- 'home' or 'away'
    PRIMARY KEY (sport_event_id, competitor_id),
    FOREIGN KEY (sport_event_id) REFERENCES sport_events(id),
    FOREIGN KEY (competitor_id) REFERENCES competitors(id)
);

CREATE TABLE rugby.sport_event_status (
    sport_event_id VARCHAR(50) PRIMARY KEY,
    status VARCHAR(20),
    match_status VARCHAR(20),
    home_score INT,
    away_score INT,
    winner_id VARCHAR(50),
    match_tie BOOLEAN,
    FOREIGN KEY (sport_event_id) REFERENCES sport_events(id),
    FOREIGN KEY (winner_id) REFERENCES competitors(id)
);

CREATE TABLE rugby.period_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sport_event_id VARCHAR(50),
    home_score INT,
    away_score INT,
    type VARCHAR(50),
    number INT,
    FOREIGN KEY (sport_event_id) REFERENCES sport_events(id)
);
