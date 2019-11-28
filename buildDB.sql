-- MySQL Script generated by MySQL Workbench
-- ons 27 nov 2019 17:52:14
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

-- -----------------------------------------------------
-- Schema webshop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `webshop` DEFAULT CHARACTER SET utf8 ;
USE `webshop` ;

-- -----------------------------------------------------
-- Table `webshop`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webshop`.`products` (
  `prodID` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) CHARACTER SET 'utf8' NOT NULL,
  `desc` MEDIUMTEXT CHARACTER SET 'utf8' NULL DEFAULT NULL,
  `price` INT(11) NOT NULL,
  `img` VARCHAR(45) CHARACTER SET 'utf8' NULL DEFAULT NULL,
  `stock` INT(11) NOT NULL,
  `category` INT(11) NULL DEFAULT NULL,
  `discount` DECIMAL(4,0) NULL DEFAULT NULL,
  PRIMARY KEY (`prodID`))
ENGINE = InnoDB
AUTO_INCREMENT = 10007
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_swedish_ci;


-- -----------------------------------------------------
-- Table `webshop`.`cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webshop`.`cart` (
  `cartID` INT(11) NOT NULL AUTO_INCREMENT,
  `prodID` INT(11) NOT NULL,
  `custID` INT(11) NOT NULL,
  `qty` INT(11) NOT NULL,
  PRIMARY KEY (`cartID`),
  INDEX `prodID_idx` (`prodID` ASC),
  CONSTRAINT `prodID`
    FOREIGN KEY (`prodID`)
    REFERENCES `webshop`.`products` (`prodID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 70000
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `webshop`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webshop`.`customers` (
  `custID` INT NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(25) NOT NULL,
  `lastname` VARCHAR(25) NOT NULL,
  `email` VARCHAR(320) NOT NULL,
  `password` VARCHAR(320) NOT NULL,
  `address` VARCHAR(95) NOT NULL,
  `postcode` VARCHAR(5) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `phoneno` VARCHAR(15) NULL,
  PRIMARY KEY (`custID`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 800000
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_swedish_ci;


-- -----------------------------------------------------
-- Table `webshop`.`employees`
-- -----------------------------------------------------
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
-- Table `webshop`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webshop`.`reviews` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `prodID` INT(11) NOT NULL,
  `custID` INT(11) NOT NULL,
  `text` LONGTEXT NOT NULL,
  `date` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `prodID_idx` (`prodID` ASC),
  INDEX `fk_custID_idx` (`custID` ASC),
  CONSTRAINT `fk_custID`
    FOREIGN KEY (`custID`)
    REFERENCES `webshop`.`customers` (`custID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prodID`
    FOREIGN KEY (`prodID`)
    REFERENCES `webshop`.`products` (`prodID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Populate product table
-- -----------------------------------------------------
INSERT INTO `products` (`name`, `desc`, `price`, `img`, `stock`) VALUES
    ('Brun stickad mössa', '', 100, 'brun-stickad-mössa.jpg', 20),
    ('Blå stickad mössa', '', 100, '', 20),
    ('Grön stickad mössa', '', 100, '', 20),
    ('Gul stickad mössa', '', 100, '', 20),
    ('Svart stickad mössa', '', 100, '', 20),
    ('Lila stickad mössa', '', 100, '', 20),
    ('Transparant stickad mössa', '', 100, '', 20);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
