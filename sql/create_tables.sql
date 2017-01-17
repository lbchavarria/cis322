CREATE DATABASE IF NOT EXISTS `lost`
USE `lost`;


DROP TABLE IF EXISTS `acquisitions`;
CREATE TABLE `acquisitions` (
	`product` char(20) DEFAULT NULL,
	`purchase order number` char(10) DEFAULT NULL,
	`order date` date DEFAULT NULL,
	`ship date` date DEFAULT NULL,
	`arrive date` date DEFAULT NULL,
	`asset tag` char(15) DEFAULT NULL
);

DROP TABLES IF EXISTS `convoy`;
CREATE TABLE `convoy` (
	`transport request #` char(10) DEFAULT NULL,
	`depart time` datetime DEFAULT NULL,
	`waypoint 1 time` datetime DEFAULT NULL,
	`waypoint 2 time` datetime DEFAULT NULL,
	`waypoint 3 time` datetime DEFAULT NULL,
	`waypoint 4 time` datetime DEFAULT NULL,
	`arrive time` datetime DEFAULT NULL,
	`assigned vehicles` char(50) DEFAULT NULL
);

DROP TABLE IF EXISTS `DC_inventory`;
CREATE TABLE `DC_inventory` (
	`asset tag` char(15) DEFAULT NULL,
	`product` char(20) DEFAULT NULL,
	`room` char(10) DEFAULT NULL,
	`compartments` char(20) DEFAULT NULL,
	`intake date` date DEFAULT NULL,
	`expunged date` date DEFAULT NULL
);

DROP TABLE IF EXISTS `HQ_inventory`;
CREATE TABLE `HQ_inventory` (
	`asset tag` char(15) DEFAULT NULL,
	`product` char(20) DEFAULT NULL,
	`room` char(10) DEFAULT NULL,
	`compartments` char(20) DEFAULT NULL,
	`intake date` date DEFAULT NULL,
	`expunged date` date DEFAULT NULL
);

DROP TABLE IF EXISTS `MB005_inventory`;
CREATE TABLE `MB005_inventory` (
	`asset tag` char(15) DEFAULT NULL,
	`product` char(20) DEFAULT NULL,
	`room` char(10) DEFAULT NULL,
	`compartments` char(20) DEFAULT NULL,
	`intake date` date DEFAULT NULL,
	`expunged date` date DEFAULT NULL
);

DROP TABLE IF EXISTS `NC_inventory`;
CREATE TABLE `NC_inventory` (
	`asset tag` char(15) DEFAULT NULL,
	`product` char(20) DEFAULT NULL,
	`room` char(10) DEFAULT NULL,
	`compartments` char(20) DEFAULT NULL,
	`intake date` date DEFAULT NULL,
	`expunged date` date DEFAULT NULL
);

DROP TABLE IF EXISTS `product_list`;
CREATE TABLE `product_list` (
	`name` char(20) DEFAULT NULL,
	`model` char(10) DEFAULT NULL,
	`description` char(50) DEFAULT NULL,
	`unit price` float(6) NOT NULL DEFAULT '0',
	`vendor` char(25) DEFAULT NULL,
	`compartments` char(20) DEFAULT NULL
);

DROP TABLE IF EXISTS `security_compartments`;
CREATE TABLE `security_compartments` (
	`compartment_tag` char(10) DEFAULT NULL,
	`compartment_desc` char(15) DEFAULT NULL
);

DROP TABLE IF EXISTS `security_levels`;
CREATE TABLE `security_levels` (
	`level` char(5) DEFAULT NULL,
	`description` char(25) DEFAULT NULL
);

DROP TABLE IF EXISTS `SPNV_inventory`;
CREATE TABLE `SPNV_inventory` (
	`asset tag` char(15) DEFAULT NULL,
	`product` char(20) DEFAULT NULL,
	`room` char(10) DEFAULT NULL,
	`compartments` char(20) DEFAULT NULL,
	`intake date` date DEFAULT NULL,
	`expunged date` date DEFAULT NULL
);

DROP TABLE IF EXISTS `transit`;
CREATE TABLE `transit` (
	`asset tag` char(50) DEFAULT NULL,
	`src facility` char(20) DEFAULT NULL,
	`dst facility` char(20) DEFAULT NULL,
	`depart date` date DEFAULT NULL,
	`arrive date` date DEFAULT NULL,
	`transport request #` char(10) DEFAULT NULL,
	`comments` char(15) DEFAULT NULL
);

DROP TABLE IF EXISTS `vendors`;
CREATE TABLE `vendors` (
	`vendor` char(20) DEFAULT NULL,
	`contact name` char(20) DEFAULT NULL,
	`contact phone` char(15) DEFAULT NULL,
	`contract #` char(10) DEFAULT NULL,
	`term`char(10) DEFAULT NULL,
	`credit line` char(15) DEFAULT NULL
);
