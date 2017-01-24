/*Create temp tables to take in CSV files */

/* product data */
CREATE temporary TABLE prod(product_pk serial not null, name text, model text, description text, unit_price text, compartments text);

COPY prod(product_pk, name, model, description, unit_price, compartments) from '$HOME/sql/osnap_legacy/product_list.csv' with DELIMITER ',' CSV HEADER;

CREATE temporary TABLE acquisitions(product text, purchase_order_number text, order_date timestamp, ship_date timestamp, arrive_date timestamp, asset_tag text);

COPY acquisitions(product, purchase_order_number, order_date, ship_date, arrive_date, asset_tag) from '$HOME/sql/osnap_legacy/acquisitions.csv', with DISCLAIMER ',' CSV HEADER;

/*Cat files from inventory or load them all into one but try to preserve facility name*/

CREATE temporary TABLE hqinv(assettag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp);

COPY hqinv(assettag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp) from '$HOME/sql/osnap_legacy/HQ_inventory.csv' with DELIMITER ',' CSV HEADER;

ALTER TABLE hqinv ADD COLUMN Location character varying(50) DEFAULT 'HQ';

CREATE temporary TABLE inv(assettag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp);

COPY dcinv(assettag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp) from '$HOME/sql/osnap_legacy/DC_inventory.csv' with DELIMITER ',' CSV HEADER;


ALTER TABLE DCinv ADD COLUMN Location character varying(50) DEFAULT 'DC';


CREATE temporary TABLE ncinv(asset_tag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp);

COPY ncinv(asset_tag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp) from '$HOME/sql/osnap_legacy/NC_inventory.csv' with DELIMITER ',' CSV HEADER;

ALTER TABLE ncinv ADD COLUMN Location character varying(50) DEFAULT 'NC';

CREATE temporary TABLE MB008inv(asset_tag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp);

COPY MB008inv(asset_tag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp) from '$HOME/sql/osnap_legacy/MB008_inventory.csv' with DELIMITER ',' CSV HEADER;


ALTER TABLE MB008inv ADD COLUMN Location character varying(50) DEFAULT 'MB008';

CREATE temporary TABLE spnvinv(asset_tag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp);

COPY spnvinv(asset_tag text,product text,room text,compartments text,intakedate timestamp,expungeddate timestamp) from '$HOME/sql/osnap_legacy/SPNV_inventory.csv' with DELIMITER ',' CSV HEADER;


ALTER TABLE spnvinv ADD COLUMN Location character varying(50) DEFAULT 'SPNV';

/*create one large master table this will create columns to fill assets,
asset_at,*/

INSERT INTO hqinv (SELECT * FROM dcinv WHERE asset_tag NOT IN (SELECT asset_tag FROM hqinv));
INSERT INTO hqinv (SELECT * FROM ncinv WHERE asset_tag NOT IN (SELECT asset_tag FROM hqinv));
INSERT INTO hqinv (SELECT * FROM MB008inv WHERE asset_tag NOT IN (SELECT asset_tag FROM hqinv));
INSERT INTO hqinv (SELECT * FROM spnvinv WHERE asset_tag NOT IN (SELECT asset_tag FROM hqinv));

/*Now need to attach a serial asset primary key to this */

ALTER TABLE hqinv ADD COLUMN asset_pk serial not null;

/*Drop unnecessary tables */
DROP TABLE ncinv;
DROP TABLE dcinv;
DROP TABLE MB008inv;
DROP TABLE SPNVinv;

/*Create a temporary table that is a join or result of query of other tables */
CREATE temp TABLE as (select * from …)

INSERT INTO asset_tables.assets(asset_tag, product)
SELECT asset_tag, product
FROM hqinv;

/* need product from acq, */
COPY asset_tables.products(product_pk,vendor,description,alt_description)
FROM '$HOME/sql/osnap_legacy/file.' DELIMITER ',' CSV HEADER;


COPY asset_tables.assets(asset_pk,product_fk,asset_tag,description,alt_description);
/* need assets from all locations from *_inventory pages?*/

COPY asset_tables.vehicles(vehicle_pk,asset_fk);
/* for facilities, don't import csv file. Just create a table with the 5 names */
COPY asset_tables.facilities(facility_pk,fcode,common_name,locationn);

COPY asset_tables.asset_at(asset_fk,facility_fk,arrive_dt,depart_dt);
COPY asset_tables.convoys(convoy_pk,request,source_fk,dest_fk,depart_dt,arrive_dt);
COPY asset_tables.used_by(vehicle_fk,convoy_fk);
COPY asset_tables.asset_on(asset_fk,convoy_fk,load_dt,unoad_dt);
COPY user_tables.users(user_pk,username,active);
COPY user_tables.roles(role_pk,title);
COPY user_tables.user_is(user_fk,role_fk);
COPY user_tables.user_supports(user_fk,facility_fk);
COPY security_tables.levels(level_pk,abbrv,comment);
COPY security_tables.compartments(compartment_pk,abbrv,commentt);
COPY security_tables.security_tags(tag_pk,level_fk,compartment_fk,user_fk,product_fk,asset_fk);

