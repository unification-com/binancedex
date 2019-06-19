-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               5.7.26-0ubuntu0.18.04.1 - (Ubuntu)
-- Server OS:                    Linux
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for binance
CREATE DATABASE IF NOT EXISTS `binance` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `binance`;

-- Dumping structure for table binance.Addresses
CREATE TABLE IF NOT EXISTS `Addresses` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Address` varchar(128) NOT NULL DEFAULT '0',
  `token` varchar(128) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=472 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table binance.Transactions
CREATE TABLE IF NOT EXISTS `Transactions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Order ID` varchar(200) NOT NULL DEFAULT '0',
  `SIDE` int(10) NOT NULL DEFAULT '0',
  `transactionHash` varchar(100) NOT NULL,
  `SYMBOL` varchar(50) NOT NULL DEFAULT '0',
  `Total` double NOT NULL DEFAULT '0',
  `Owner` varchar(50) NOT NULL DEFAULT '0',
  `Price` double NOT NULL DEFAULT '0',
  `quantity` double NOT NULL DEFAULT '0',
  `orderCreateTime` datetime NOT NULL DEFAULT '2019-06-17 09:09:37',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2203 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
