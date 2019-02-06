CREATE TABLE `builds` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(38) NOT NULL,
  `StartTime` varchar(45) DEFAULT NULL,
  `FinishTime` datetime DEFAULT NULL,
  `Compiler` varchar(20) DEFAULT NULL,
  `CompilerVersion` varchar(10) DEFAULT NULL,
  `Type` varchar(20) DEFAULT NULL,
  `Flags` varchar(255) DEFAULT NULL,
  `KernelRelease` varchar(45) DEFAULT NULL,
  `KernelVersion` datetime DEFAULT NULL,
  `CMakeStatus` smallint(6) DEFAULT NULL,
  `MakeStatus` smallint(6) DEFAULT NULL,
  `TestStatus` smallint(6) DEFAULT NULL,
  `BuildTime` int(11) DEFAULT NULL,
  `TestTime` int(11) DEFAULT NULL,
  `TestCount` smallint(6) DEFAULT '0',
  `TestPass` smallint(6) DEFAULT '0',
  `TestFail` smallint(6) DEFAULT '0',
  `TestNotRun` smallint(6) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `repository` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `GitHash` varchar(40) DEFAULT NULL,
  `GitRef` varchar(40) NOT NULL,
  `GitTime` datetime DEFAULT NULL,
  `GitMesage` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `GitHash_UNIQUE` (`GitHash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tests` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `BuildID` int(11) DEFAULT NULL,
  `Category` tinyint(4) DEFAULT NULL,
  `Status` tinyint(4) DEFAULT NULL,
  `RunTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `workers` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(32) DEFAULT NULL,
  `HostName` varchar(32) DEFAULT NULL,
  `OS` varchar(45) DEFAULT NULL,
  `Architecture` varchar(20) DEFAULT NULL,
  `LastSeen` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
