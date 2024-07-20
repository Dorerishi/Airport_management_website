create trigger updateairdetail
after insert on arrivals
for each row
update aircraftdetails
set currentlocation = 'At Airport'
where new.FlightNumber = AircraftDetails.FlightNumber;
create trigger upgate
after insert on Arrivals
for each row
update Gates
set Gates.status = 'Occupied' where new.GateId = GateId;
create trigger delflightschedule
after delete on Arrivals
for each row 
delete from FlightSchedule 
where old.ArrivalID=ScheduleID;
create trigger upaircraftdetails
after delete on Arrivals
for each row
update AircraftDetails
set CurrentLocation = 'Not at Airport' 
where old.FlightNumber = FlightNumber;