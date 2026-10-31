DO $$
BEGIN
    CREATE TYPE estacao AS ENUM (
        'PRIMAVERA', 'VERAO', 'OUTONO', 'INVERNO', 'ANUAL'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE estado AS ENUM (
        'AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO', 'AL', 'BA', 'CE',
        'MA', 'PB', 'PE', 'PI', 'RN', 'SE', 'GO', 'MT', 'MS', 'DF',
        'ES', 'RJ', 'SP', 'MG', 'PR', 'SC', 'RS'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE tipolimiar AS ENUM ('MAXIMO', 'MINIMO', 'DIASSEMCHUVA');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE variavel AS ENUM (
        'TEMPERATURA', 'UMIDADE', 'PRECIPITACAO',
        'VELOCIDADEVENTO', 'PRESSAOATMOSFERICA'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS "Localidades" (
    "IDLocalidade" SERIAL NOT NULL,
    "Nome" VARCHAR(150) NOT NULL,
    "Cidade" VARCHAR(150) NOT NULL,
    "Estado" estado NOT NULL,
    "Latitude" NUMERIC(8, 6) NOT NULL
        CHECK ("Latitude" >= -90 and "Latitude" <= 90),
    "Longitude" NUMERIC(9, 6) NOT NULL
        CHECK ("Longitude" >= -180 and "Longitude" <= 180),
    "Ativo" BOOLEAN NOT NULL,
    PRIMARY KEY ("IDLocalidade"),
    CONSTRAINT uq_localidades_latitude_longitude
        UNIQUE ("Latitude", "Longitude")
);

CREATE TABLE IF NOT EXISTS "RegistrosClimaticos" (
    "IDRegistrosClimaticos" SERIAL NOT NULL,
    "TempMax" NUMERIC(4, 1) NOT NULL
        CHECK ("TempMax" between -20 and 50),
    "TempMin" NUMERIC(4, 1) NOT NULL
        CHECK ("TempMin" between -20 and 50),
    "TempMedia" NUMERIC(4, 1) NOT NULL
        CHECK ("TempMedia" between -20 and 50),
    "UmidadeRelativa" NUMERIC(5, 2) NOT NULL
        CHECK ("UmidadeRelativa" between 0 and 100),
    "Precipitacao" NUMERIC(5, 2) NOT NULL
        CHECK ("Precipitacao" >= 0),
    "VelocidadeVento" NUMERIC(5, 2) NOT NULL
        CHECK ("VelocidadeVento" between 0 and 150),
    "PressaoAtmosferica" NUMERIC(7, 2) NOT NULL
        CHECK ("PressaoAtmosferica" between 800 and 1100),
    "Data" DATE NOT NULL,
    "Hora" TIME WITHOUT TIME ZONE NOT NULL,
    "Ativo" BOOLEAN NOT NULL,
    "FKLocalidade" INTEGER NOT NULL,
    PRIMARY KEY ("IDRegistrosClimaticos"),
    CONSTRAINT ck_registros_tempmin_tempmax
        CHECK ("TempMin" <= "TempMax"),
    CONSTRAINT ck_registros_tempmin_tempmedia_tempmax
        CHECK ("TempMin" <= "TempMedia" and "TempMedia" <= "TempMax"),
    CONSTRAINT uq_registros_data_hora_localidade
        UNIQUE ("Data", "Hora", "FKLocalidade"),
    FOREIGN KEY ("FKLocalidade")
        REFERENCES "Localidades" ("IDLocalidade") ON DELETE no action
);

CREATE TABLE IF NOT EXISTS "Thresholds" (
    "IDThreshold" SERIAL NOT NULL,
    "FKLocalidade" INTEGER NOT NULL,
    "Variavel" variavel NOT NULL,
    "TipoLimiar" tipolimiar NOT NULL,
    "EstacaoDoAno" estacao NOT NULL,
    "Valor" NUMERIC(7, 2) NOT NULL,
    "Ativo" BOOLEAN NOT NULL,
    PRIMARY KEY ("IDThreshold"),
    CONSTRAINT uq_thresholds_localidade_variavel_tipo_estacao
        UNIQUE ("FKLocalidade", "Variavel", "TipoLimiar", "EstacaoDoAno"),
    FOREIGN KEY ("FKLocalidade")
        REFERENCES "Localidades" ("IDLocalidade") ON DELETE no action
);
