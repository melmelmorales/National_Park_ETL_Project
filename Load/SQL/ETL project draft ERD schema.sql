-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "nps_amenities_data" (
    "amenity_id" varchar(50)   NOT NULL,
    "amenity_name" varchar(100)   NOT NULL,
    "amenity_category" varchar(100)   NOT NULL,
    CONSTRAINT "pk_nps_amenities_data" PRIMARY KEY (
        "amenity_id"
     )
);

CREATE TABLE "nps_amen_place_data" (
    "amenity_id" varchar(50)   NOT NULL,
    "amenity_name" varchar(100)   NOT NULL,
    "park_code" varchar(10)   NOT NULL,
    "park_name" varchar(50)   NOT NULL,
    "park_states" varchar(10)   NOT NULL,
    "park_designation" varchar(50)   NOT NULL,
    "park_url" varchar(250)   NOT NULL,
    CONSTRAINT "pk_nps_amen_place_data" PRIMARY KEY (
        "amenity_id"
     )
);

CREATE TABLE "nps_places_data" (
    "place_id" varchar(50)   NOT NULL,
    "park_url" varchar(250)   NOT NULL,
    "park_name" varchar(50)   NOT NULL,
    "park_code" varchar(10)   NOT NULL,
    "park_latitude" varchar(50)   NOT NULL,
    "park_longitude" varchar(50)   NOT NULL,
    "park_designation" varchar(50)   NOT NULL,
    CONSTRAINT "pk_nps_places_data" PRIMARY KEY (
        "place_id"
     )
);

CREATE TABLE "nps_parks_data" (
    "park_id" varchar(50)   NOT NULL,
    "park_url" varchar(250)   NOT NULL,
    "park_name" varchar(50)   NOT NULL,
    "park_code" varchar(10)   NOT NULL,
    "park_latitude" varchar(50)   NOT NULL,
    "park_longitude" varchar(50)   NOT NULL,
    "park_designation" varchar(50)   NOT NULL,
    CONSTRAINT "pk_nps_parks_data" PRIMARY KEY (
        "park_id"
     )
);

CREATE TABLE "activities" (
    "activity_id" varchar(50)   NOT NULL,
    "activity_name" varchar(100)   NOT NULL,
    CONSTRAINT "pk_activities" PRIMARY KEY (
        "activity_id"
     )
);

CREATE TABLE "activities_parks" (
    "activity_id" varchar(50)   NOT NULL,
    "activity_name" varchar(100)   NOT NULL,
    "designation" varchar(50)   NOT NULL,
    "fullName" varchar(50)   NOT NULL,
    "name" varchar(50)   NOT NULL,
    "parkCode" varchar(10)   NOT NULL,
    "states" varchar(10)   NOT NULL,
    "url" varchar(250)   NOT NULL,
    CONSTRAINT "pk_activities_parks" PRIMARY KEY (
        "activity_id"
     )
);

CREATE TABLE "feespasses" (
    "parkCode" varchar(10)   NOT NULL,
    "totalFees" int   NOT NULL,
    "averageFees" float   NOT NULL,
    "totalPasses" int   NOT NULL,
    "averagePasses" int   NOT NULL,
    "isFeeFreePark" varchar(10)   NOT NULL,
    "entrancePassDescription" varchar(500)   NOT NULL,
    "entraceFeeDescription" varchar(500)   NOT NULL,
    "feesAtWorkUrl" varchar(250)   NOT NULL,
    CONSTRAINT "pk_feespasses" PRIMARY KEY (
        "parkCode"
     )
);

ALTER TABLE "nps_amenities_data" ADD CONSTRAINT "fk_nps_amenities_data_amenity_id" FOREIGN KEY("amenity_id")
REFERENCES "nps_amen_place_data" ("amenity_id");

ALTER TABLE "nps_amen_place_data" ADD CONSTRAINT "fk_nps_amen_place_data_park_code" FOREIGN KEY("park_code")
REFERENCES "nps_parks_data" ("park_code");

ALTER TABLE "nps_places_data" ADD CONSTRAINT "fk_nps_places_data_park_code" FOREIGN KEY("park_code")
REFERENCES "nps_parks_data" ("park_code");

ALTER TABLE "activities" ADD CONSTRAINT "fk_activities_activity_id" FOREIGN KEY("activity_id")
REFERENCES "activities_parks" ("activity_id");

ALTER TABLE "activities_parks" ADD CONSTRAINT "fk_activities_parks_parkCode" FOREIGN KEY("parkCode")
REFERENCES "nps_parks_data" ("park_code");

ALTER TABLE "feespasses" ADD CONSTRAINT "fk_feespasses_parkCode" FOREIGN KEY("parkCode")
REFERENCES "nps_places_data" ("park_code");

