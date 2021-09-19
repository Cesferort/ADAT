CREATE TABLE `Deporte` (
	`id_deporte`	INTEGER NOT NULL,
	`nombre`	TEXT NOT NULL,
	PRIMARY KEY(`id_deporte`)
);

CREATE TABLE `Deportista` (
	`id_deportista`	INTEGER NOT NULL,
	`nombre`	TEXT NOT NULL,
	`sexo`	TEXT NOT NULL,
	`peso`	INTEGER,
	`altura`	INTEGER,
	PRIMARY KEY(`id_deportista`)
);

CREATE TABLE `Equipo` (
	`id_equipo`	INTEGER NOT NULL,
	`nombre`	TEXT NOT NULL,
	`iniciales`	TEXT NOT NULL,
	PRIMARY KEY(`id_equipo`)
);

CREATE TABLE `Evento` (
	`id_evento`	INTEGER NOT NULL,
	`nombre`	TEXT NOT NULL,
	`id_olimpiada`	INTEGER NOT NULL,
	`id_deporte`	INTEGER NOT NULL,
	FOREIGN KEY(`id_olimpiada`) REFERENCES `Olimpiada`(`id_olimpiada`),
	PRIMARY KEY(`id_evento`),
	FOREIGN KEY(`id_deporte`) REFERENCES `Deporte`(`id_deporte`)
);

CREATE TABLE `Olimpiada` (
	`id_olimpiada`	INTEGER NOT NULL,
	`nombre`	TEXT NOT NULL,
	`anio`	INTEGER NOT NULL,
	`temporada`	TEXT NOT NULL,
	`ciudad`	TEXT NOT NULL,
	PRIMARY KEY(`id_olimpiada`)
);

CREATE TABLE `Participacion` (
	`id_deportista`	INTEGER NOT NULL,
	`id_evento`	INTEGER NOT NULL,
	`id_equipo`	INTEGER NOT NULL,
	`edad`	INTEGER,
	`medalla`	TEXT,
	FOREIGN KEY(`id_evento`) REFERENCES `Evento`(`id_evento`),
	FOREIGN KEY(`id_deportista`) REFERENCES `Deportista`(`id_deportista`),
	FOREIGN KEY(`id_equipo`) REFERENCES `Equipo`(`id_equipo`),
	PRIMARY KEY(`id_deportista`,`id_evento`,`id_equipo`)
);