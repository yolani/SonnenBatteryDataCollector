-- Table: public.measurements

-- DROP TABLE public.measurements;

CREATE TABLE public.measurements
(
    production_w smallint,
    consumption_w smallint,
    grid_feed_in_w smallint,
    grid_retrieve_w smallint,
    battery_level smallint,
    battery_charge_w smallint,
    battery_discharge_w smallint,
    consumption_ws double precision,
    production_ws double precision,
    grid_feed_in_ws double precision,
    grid_retrieve_ws real,
    battery_charge_ws double precision,
    battery_discharge_ws double precision,
    "timestamp" timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT measurements_pkey PRIMARY KEY ("timestamp")
)

TABLESPACE pg_default;

