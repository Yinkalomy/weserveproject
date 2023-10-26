# =============================================== FOR DEV SCHEMA
dev_call_log = '''CREATE TABLE IF NOT EXISTS raw_data.dev_call_log
(
    id int,
    callerid varchar,
    agentID int,
    complaintTopic varchar,
    assignedTo int,
    status varchar,
    resolutionDurationInHours int
);'''

dev_call_details = '''CREATE TABLE IF NOT EXISTS raw_data.dev_call_details
(
    callID int,
    callDurationInSeconds int,
    agentsGradeLevel varchar,
    callType varchar,
    callEndedByAgent bool default True
);'''


# =============================================== FOR STAR SCHEMA
ft_call_log = '''
CREATE TABLE IF NOT EXISTS staging.ft_call_log(
    call_id int,
    caller_ID varchar, 
    agentID INT, 
    callDurationInSeconds NUMERIC(3, 2)
);
'''

dim_call_details = '''
    CREATE TABLE IF NOT EXISTS staging.dim_call_details(
        callID int,
        resolutionDurationInHours int, 
        callType varchar, 
        complaintTopic varchar,
        assignedTo int,
        status varchar
    );
'''

dim_agent = '''
    CREATE TABLE IF NOT EXISTS staging.dim_agent (
        agentID int,
        agentsGradeLevel varchar
    );
'''

agg_KPI1 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI1 (
    agentID int,
    noOfResolvedCalls int,
    noOfCallsReceived int
);
'''

agg_KPI2 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI2
(
    agentID int, 
    noOfCallsReceived int,
    callsAssignedOrResolved int
);
'''

agg_KPI3 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI3
(
    agentID int, 
    agentsGradeLevel VARCHAR,
    totalCallDuration integer,
    avgCallDuration NUMERIC (3, 2)
);
'''

agg_KPI4 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI4
(
    agentID integer, 
    agentsGradeLevel VARCHAR,
    earliestClosedCall integer,
    latestClosedCall integer
);
'''

dev_tables = [dev_call_log, dev_call_details]
transformed_tables = [ft_call_log, dim_call_details, dim_agent, agg_KPI1, agg_KPI2, agg_KPI3, agg_KPI4]