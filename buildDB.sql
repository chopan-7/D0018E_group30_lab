-- MySQL Script generated by MySQL Workbench
-- Tue Dec  3 18:45:34 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema webshop
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `webshop` ;

-- -----------------------------------------------------
-- Schema webshop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `webshop` ;
USE `webshop` ;

-- -----------------------------------------------------
-- Table `webshop`.`products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`products` ;

CREATE TABLE IF NOT EXISTS `webshop`.`products` (
  `prodID` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) CHARACTER SET 'utf8' NOT NULL,
  `desc` VARCHAR(160) CHARACTER SET 'utf8' NULL DEFAULT NULL,
  `price` INT(11) NOT NULL,
  `img` VARCHAR(45) CHARACTER SET 'utf8' NULL DEFAULT NULL,
  `stock` INT(11) NOT NULL,
  `category` INT(11) NULL DEFAULT NULL,
  `discount` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`prodID`))
ENGINE = InnoDB
AUTO_INCREMENT = 10022
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_swedish_ci;


-- -----------------------------------------------------
-- Table `webshop`.`cart`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`cart` ;

CREATE TABLE IF NOT EXISTS `webshop`.`cart` (
  `cartID` INT(11) NOT NULL AUTO_INCREMENT,
  `prodID` INT(11) NOT NULL,
  `custID` INT(11) NOT NULL,
  `qty` INT(11) NOT NULL,
  PRIMARY KEY (`cartID`),
  INDEX `prodID_idx` (`prodID` ASC),
  CONSTRAINT `prodID`
    FOREIGN KEY (`prodID`)
    REFERENCES `webshop`.`products` (`prodID`))
ENGINE = InnoDB
AUTO_INCREMENT = 70045
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `webshop`.`customers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`customers` ;

CREATE TABLE IF NOT EXISTS `webshop`.`customers` (
  `custID` INT(11) NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(25) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  `lastname` VARCHAR(25) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  `email` VARCHAR(320) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  `password` VARCHAR(320) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  `address` VARCHAR(95) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  `postcode` VARCHAR(5) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  `country` VARCHAR(45) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  `phoneno` VARCHAR(15) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NULL DEFAULT NULL,
  `profilepic` VARCHAR(60) CHARACTER SET 'utf8' COLLATE 'utf8_swedish_ci' NOT NULL,
  PRIMARY KEY (`custID`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 800001
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_swedish_ci;


-- -----------------------------------------------------
-- Table `webshop`.`employees`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`employees` ;

CREATE TABLE IF NOT EXISTS `webshop`.`employees` (
  `employeeID` INT(11) NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(25) NOT NULL,
  `lastname` VARCHAR(25) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`employeeID`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 9000
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `webshop`.`orders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`orders` ;

CREATE TABLE IF NOT EXISTS `webshop`.`orders` (
  `orderID` INT(11) NOT NULL AUTO_INCREMENT,
  `custID` INT(11) NOT NULL,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `invoiceno` INT(11) NULL DEFAULT '0',
  `amount` DECIMAL(19,4) NOT NULL,
  `status` INT(11) NULL DEFAULT '0',
  PRIMARY KEY (`orderID`),
  INDEX `custID_idx` (`custID` ASC),
  CONSTRAINT `orders_custID`
    FOREIGN KEY (`custID`)
    REFERENCES `webshop`.`customers` (`custID`))
ENGINE = InnoDB
AUTO_INCREMENT = 60058
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `webshop`.`orderln`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`orderln` ;

CREATE TABLE IF NOT EXISTS `webshop`.`orderln` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `orderID` INT(11) NOT NULL,
  `lineno` INT(11) NOT NULL,
  `prodID` INT(11) NOT NULL,
  `qty` INT(11) NOT NULL,
  `price` INT(11) NOT NULL,
  `discount` INT(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`, `orderID`),
  INDEX `prodID_idx` (`prodID` ASC),
  INDEX `orderln_orderID` (`orderID` ASC),
  CONSTRAINT `orderln_orderID`
    FOREIGN KEY (`orderID`)
    REFERENCES `webshop`.`orders` (`orderID`),
  CONSTRAINT `orderln_prodID`
    FOREIGN KEY (`prodID`)
    REFERENCES `webshop`.`products` (`prodID`))
ENGINE = InnoDB
AUTO_INCREMENT = 68
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `webshop`.`reviews`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`reviews` ;

CREATE TABLE IF NOT EXISTS `webshop`.`reviews` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `prodID` INT(11) NOT NULL,
  `custID` INT(11) NOT NULL,
  `text` LONGTEXT NOT NULL,
  `date` VARCHAR(45) NOT NULL,
  `stars` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `prodID_idx` (`prodID` ASC),
  INDEX `fk_custID_idx` (`custID` ASC),
  CONSTRAINT `fk_custID`
    FOREIGN KEY (`custID`)
    REFERENCES `webshop`.`customers` (`custID`),
  CONSTRAINT `fk_prodID`
    FOREIGN KEY (`prodID`)
    REFERENCES `webshop`.`products` (`prodID`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `webshop`.`text`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `webshop`.`text` ;

CREATE TABLE IF NOT EXISTS `webshop`.`text` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `typeid` INT(11) NULL DEFAULT '0',
  `type` VARCHAR(45) NULL DEFAULT NULL,
  `textid` INT(11) NULL DEFAULT '0',
  `text` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `textid_UNIQUE` (`textid` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
