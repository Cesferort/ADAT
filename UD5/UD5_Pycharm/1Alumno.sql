DROP TYPE BODY T_ALUMNO;
DROP TYPE T_ALUMNO;
DROP TYPE PERSONA;
DROP TYPE BODY DIRECCION;
DROP TYPE DIRECCION;

CREATE OR REPLACE TYPE DIRECCION AS OBJECT
(
    CALLE               VARCHAR2(25),
    CIUDAD              VARCHAR2(20),
    CODIGO_POST         NUMBER(5),
    MEMBER PROCEDURE SET_CALLE(C VARCHAR2),
    MEMBER FUNCTION GET_CALLE RETURN VARCHAR2,
    CONSTRUCTOR FUNCTION DIRECCION (CA VARCHAR2, CI VARCHAR2, CO VARCHAR2) RETURN SELF AS RESULT
);
/
CREATE OR REPLACE TYPE BODY DIRECCION AS
    CONSTRUCTOR FUNCTION DIRECCION (CA VARCHAR2, CI VARCHAR2, CO VARCHAR2)
    RETURN SELF AS RESULT
    AS
    BEGIN
        SELF.CALLE := CA;
        SELF.CIUDAD := CI;
        SELF.CODIGO_POST := CO;
        RETURN;
    END;

    MEMBER PROCEDURE SET_CALLE(C VARCHAR2) IS
        BEGIN
            CALLE := C;
        END;

    MEMBER FUNCTION GET_CALLE RETURN VARCHAR2 IS
        BEGIN
            RETURN CALLE;
        END;
END;
/
CREATE OR REPLACE TYPE PERSONA AS OBJECT (
    CODIGO              NUMBER,
    NOMBRE              VARCHAR2(35),
    DIR                 DIRECCION,
    FECHA_NAC           DATE
);
/
CREATE OR REPLACE TYPE T_ALUMNO AS OBJECT (
    P                   PERSONA,
    NOTA_PRIMERA        NUMBER,
    NOTA_SEGUNDA        NUMBER,
    NOTA_TERCERA        NUMBER,
	ID					NUMBER, 
    MEMBER FUNCTION NOTA_MEDIA RETURN NUMBER
);
/
CREATE OR REPLACE TYPE BODY T_ALUMNO AS
    MEMBER FUNCTION NOTA_MEDIA RETURN NUMBER IS
    BEGIN
        RETURN ((NOTA_PRIMERA + NOTA_SEGUNDA + NOTA_TERCERA) / 3);
    END;
END;
/

SET SERVEROUTPUT ON;
DECLARE
    DIR                  DIRECCION  	:= DIRECCION('Calle de Prueba', 'Vitoria', 1007);
    P                    PERSONA     	:= PERSONA(1, 'Prueba', DIR, '30/6/1999');
    ALUMNO               T_ALUMNO    	:= T_ALUMNO(P, 5, 10, 5, 0);
BEGIN
    DBMS_OUTPUT.PUT_LINE(ALUMNO.NOTA_MEDIA);
END;
/

CREATE TABLE ALUMNOS2 OF T_ALUMNO 
(
	ID					 PRIMARY KEY
);
DECLARE
    DIR                  DIRECCION  	:= DIRECCION('Calle de Prueba', 'Vitoria', 1007);
    P                    PERSONA     	:= PERSONA(1, 'Prueba', DIR, '30/6/1999');
BEGIN
    INSERT INTO ALUMNOS2 VALUES(P, 5, 10, 5, 0);
END;
/
SELECT A.P.NOMBRE, A.NOTA_MEDIA()
FROM ALUMNOS2 A;