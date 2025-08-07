select * from rugby.competitors;
select * from rugby.competitions;
select * from rugby.seasons;
select * from rugby.sport_events;
select * from rugby.event_competitors;
select * from rugby.sport_event_status;
select * from rugby.period_scores;

select group_name,count(group_name) 
from rugby.sport_events
group by group_name
order by group_name


/*
rugby.competitors;
rugby.competitions;
rugby.seasons;
rugby.sport_events;
rugby.event_competitors;
rugby.sport_event_status;
rugby.period_scores;
*/