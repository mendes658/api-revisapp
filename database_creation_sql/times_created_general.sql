-- Para contar quantas informações de cada tipo foram adicionadas

CREATE TABLE IF NOT EXISTS public.times_created_general
(
    date date NOT NULL DEFAULT now(),
    lessons_created integer DEFAULT 0,
    users_created integer DEFAULT 0,
    subjects_created integer DEFAULT 0,
    CONSTRAINT times_created_general_pkey PRIMARY KEY (date)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.times_created_general
    OWNER to postgres;