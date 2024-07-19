-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 13, 2023 at 01:52 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qr_code`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_login`
--

CREATE TABLE `admin_login` (
  `id` int(11) NOT NULL,
  `bus_depo_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `place` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_login`
--

INSERT INTO `admin_login` (`id`, `bus_depo_name`, `password`, `place`) VALUES
(1, 'Ghandipuram', 'depo@123', 'Coimbatore');

-- --------------------------------------------------------

--
-- Table structure for table `bus_schedule`
--

CREATE TABLE `bus_schedule` (
  `id` int(11) NOT NULL,
  `bus_number` varchar(20) DEFAULT NULL,
  `from_place` varchar(255) DEFAULT NULL,
  `destination` varchar(255) DEFAULT NULL,
  `num_of_stops` int(11) DEFAULT NULL,
  `total_fare` decimal(10,2) DEFAULT NULL,
  `message` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bus_schedule`
--

INSERT INTO `bus_schedule` (`id`, `bus_number`, `from_place`, `destination`, `num_of_stops`, `total_fare`, `message`) VALUES
(1, 'S11', 'Singanallur', 'Ganapathy', 10, '56.00', NULL),
(2, 'S11', 'Singanallur', 'Ganapathy', 10, '56.00', NULL),
(3, '70', 'Ghandipuram', 'Maruthamalai', 15, '80.00', NULL),
(4, '95A', 'Ghandipuram', 'Singanallur', 15, '85.00', NULL),
(5, '100', 'Ghandipuram', 'Singanallur', 3, '25.00', 'xyz'),
(6, '100', 'Ghandipuram', 'Singanallur', 3, '25.00', 'xyz'),
(7, '100', 'Ghandipuram', 'Singanallur', 3, '25.00', 'xyz'),
(8, '10000A', 'Ghandipuram', 'Singanallur', 5, '30.00', 'xyz');

-- --------------------------------------------------------

--
-- Table structure for table `bus_stops`
--

CREATE TABLE `bus_stops` (
  `id` int(11) NOT NULL,
  `bus_schedule_id` int(11) DEFAULT NULL,
  `stop_name` varchar(255) NOT NULL,
  `stop_fare` decimal(10,2) NOT NULL,
  `stop_timing` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bus_stops`
--

INSERT INTO `bus_stops` (`id`, `bus_schedule_id`, `stop_name`, `stop_fare`, `stop_timing`) VALUES
(1, 5, 'Peelamedu', '5.00', '8 AM'),
(2, 6, 'Peelamedu', '5.00', '8 AM'),
(3, 6, 'hopes college', '10.00', '8.15 AM'),
(4, 7, 'Peelamedu', '5.00', '8 AM'),
(5, 7, 'hopes college', '10.00', '8.15 AM'),
(6, 7, 'ESI', '10.00', '8.25 AM'),
(7, 8, 'Peelamedu', '5.00', '8 AM'),
(8, 8, 'hopes college', '10.00', '8.15 AM'),
(9, 8, 'ESI', '10.00', '8.25 AM'),
(10, 8, 'Mall', '15.00', '8.30 AM'),
(11, 8, 'KG', '30.00', '8.45 AM');

-- --------------------------------------------------------

--
-- Table structure for table `qr_code_images`
--

CREATE TABLE `qr_code_images` (
  `id` int(11) NOT NULL,
  `bus_number` varchar(255) NOT NULL,
  `image_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qr_code_images`
--

INSERT INTO `qr_code_images` (`id`, `bus_number`, `image_path`) VALUES
(1, 'S11', 'static\\S11.png'),
(2, '95A', 'static\\95A.png'),
(3, '10000A', 'static\\10000A.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_login`
--
ALTER TABLE `admin_login`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bus_schedule`
--
ALTER TABLE `bus_schedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bus_stops`
--
ALTER TABLE `bus_stops`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bus_schedule_id` (`bus_schedule_id`);

--
-- Indexes for table `qr_code_images`
--
ALTER TABLE `qr_code_images`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_login`
--
ALTER TABLE `admin_login`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bus_schedule`
--
ALTER TABLE `bus_schedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `bus_stops`
--
ALTER TABLE `bus_stops`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `qr_code_images`
--
ALTER TABLE `qr_code_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bus_stops`
--
ALTER TABLE `bus_stops`
  ADD CONSTRAINT `bus_stops_ibfk_1` FOREIGN KEY (`bus_schedule_id`) REFERENCES `bus_schedule` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
