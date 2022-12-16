CREATE TABLE IF NOT EXISTS public.lessons
(
    id serial,
    lesson character varying COLLATE pg_catalog."default" NOT NULL,
    subject_id integer,
    revision_dates character varying COLLATE pg_catalog."default",
    first_rev_date timestamp without time zone,
    last_rev_date timestamp without time zone,
    created_at timestamp with time zone DEFAULT now(),
    date timestamp without time zone,
    CONSTRAINT lessons_pkey PRIMARY KEY (id),
    CONSTRAINT lessons_subject_id_fkey FOREIGN KEY (subject_id)
        REFERENCES public.subjects (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.lessons
    OWNER to postgres;