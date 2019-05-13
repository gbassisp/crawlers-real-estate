-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: May 10, 2019 at 05:06 AM
-- Server version: 10.1.10-MariaDB
-- PHP Version: 7.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `real_estate`
--

-- --------------------------------------------------------

--
-- Table structure for table `css`
--

CREATE TABLE `css` (
  `CSSID` int(11) NOT NULL,
  `FileName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `domain`
--

CREATE TABLE `domain` (
  `DomainID` int(11) NOT NULL,
  `DomainName` text NOT NULL,
  `CountryName` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='This table contain all allowed domains';

--
-- Dumping data for table `domain`
--

INSERT INTO `domain` (`DomainID`, `DomainName`, `CountryName`) VALUES
(1, 'zapimoveis.com.br', 'Brazil');

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

CREATE TABLE `request` (
  `RequestID` int(11) NOT NULL,
  `URLID` int(11) DEFAULT NULL,
  `DateOfRequest` date NOT NULL,
  `ResponseCode` int(11) NOT NULL,
  `FileName` text NOT NULL,
  `CSSID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `url`
--

CREATE TABLE `url` (
  `URLID` int(11) NOT NULL,
  `FullURL` text NOT NULL,
  `DomainID` int(11) DEFAULT NULL,
  `DateIndexed` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `url`
--

INSERT INTO `url` (`URLID`, `FullURL`, `DomainID`, `DateIndexed`) VALUES
(1, 'https://www.zapimoveis.com.br/', 1, '2019-04-25');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `css`
--
ALTER TABLE `css`
  ADD PRIMARY KEY (`CSSID`);

--
-- Indexes for table `domain`
--
ALTER TABLE `domain`
  ADD PRIMARY KEY (`DomainID`),
  ADD KEY `DomainID` (`DomainID`);

--
-- Indexes for table `request`
--
ALTER TABLE `request`
  ADD PRIMARY KEY (`RequestID`) USING BTREE,
  ADD KEY `URLID` (`URLID`),
  ADD KEY `CSSID` (`CSSID`);

--
-- Indexes for table `url`
--
ALTER TABLE `url`
  ADD PRIMARY KEY (`URLID`),
  ADD KEY `DomainID` (`DomainID`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `css`
--
ALTER TABLE `css`
  MODIFY `CSSID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `domain`
--
ALTER TABLE `domain`
  MODIFY `DomainID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `request`
--
ALTER TABLE `request`
  MODIFY `RequestID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `url`
--
ALTER TABLE `url`
  MODIFY `URLID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `request`
--
ALTER TABLE `request`
  ADD CONSTRAINT `request_ibfk_1` FOREIGN KEY (`CSSID`) REFERENCES `css` (`CSSID`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `request_ibfk_2` FOREIGN KEY (`URLID`) REFERENCES `url` (`URLID`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `url`
--
ALTER TABLE `url`
  ADD CONSTRAINT `url_ibfk_1` FOREIGN KEY (`DomainID`) REFERENCES `domain` (`DomainID`) ON DELETE SET NULL ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
