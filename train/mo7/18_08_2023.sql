PGDMP     ,    4                {            parth     15.4 (Ubuntu 15.4-1.pgdg20.04+1)     15.4 (Ubuntu 15.4-1.pgdg20.04+1) Q    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    25508    parth    DATABASE     k   CREATE DATABASE parth WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_IN';
    DROP DATABASE parth;
                postgres    false            �            1259    25509    trains1    TABLE     o  CREATE TABLE public.trains1 (
    train_id integer NOT NULL,
    nominal_odc character varying,
    entraning_station character varying,
    start_time timestamp without time zone,
    detraining_station character varying,
    consignment character varying,
    type character varying,
    delay_time time without time zone,
    start_time1 time without time zone
);
    DROP TABLE public.trains1;
       public         heap    postgres    false            �            1259    25514    master_train_id_seq    SEQUENCE     �   CREATE SEQUENCE public.master_train_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.master_train_id_seq;
       public          postgres    false    214            �           0    0    master_train_id_seq    SEQUENCE OWNED BY     L   ALTER SEQUENCE public.master_train_id_seq OWNED BY public.trains1.train_id;
          public          postgres    false    215            �            1259    25515    mst_capacity    TABLE     �   CREATE TABLE public.mst_capacity (
    station character varying,
    capacity integer,
    station_code character varying,
    id integer NOT NULL
);
     DROP TABLE public.mst_capacity;
       public         heap    postgres    false            �            1259    25520    mst_distance    TABLE     w   CREATE TABLE public.mst_distance (
    src character varying,
    dest character varying,
    dist double precision
);
     DROP TABLE public.mst_distance;
       public         heap    postgres    false            �            1259    25525    mst_priority    TABLE     l   CREATE TABLE public.mst_priority (
    id integer NOT NULL,
    type character(3),
    priority smallint
);
     DROP TABLE public.mst_priority;
       public         heap    postgres    false            �            1259    25528 	   mst_speed    TABLE     {   CREATE TABLE public.mst_speed (
    type character(1),
    odc character(1),
    speed integer,
    id integer NOT NULL
);
    DROP TABLE public.mst_speed;
       public         heap    postgres    false            �            1259    25531    trains    TABLE     1  CREATE TABLE public.trains (
    train_id integer DEFAULT nextval('public.master_train_id_seq'::regclass) NOT NULL,
    nominal_odc character varying,
    entraning_station character varying,
    place timestamp without time zone,
    detraining_station character varying,
    consignment character varying,
    type character varying,
    delay_time timestamp without time zone,
    e_loading timestamp without time zone,
    date0 timestamp without time zone DEFAULT '2023-01-01 00:00:00'::timestamp without time zone,
    change_station character varying
);
    DROP TABLE public.trains;
       public         heap    postgres    false    215            �            1259    25538 	   train_rpt    VIEW     �  CREATE VIEW public.train_rpt AS
 SELECT a.train_id,
    a.nominal_odc,
    a.type,
    a.entraning_station,
    a.place AS start_time,
    a.detraining_station,
    a.consignment,
    b.speed,
    c.capacity AS d_capacity,
    d.priority,
    e.dist AS distance,
    (a.place + ('01:00:00'::interval * (e.dist / (b.speed)::double precision))) AS arrival_time,
    ('01:00:00'::interval * (e.dist / (b.speed)::double precision)) AS travel_time,
    ((a.place + ('01:00:00'::interval * (e.dist / (b.speed)::double precision))) + '10:00:00'::interval) AS loading_time,
    a.delay_time
   FROM ((((public.trains a
     JOIN public.mst_speed b ON ((((a.nominal_odc)::bpchar = b.odc) AND ((a.type)::bpchar = b.type))))
     JOIN public.mst_capacity c ON (((a.detraining_station)::text = (c.station)::text)))
     JOIN public.mst_priority d ON (((a.consignment)::bpchar = d.type)))
     JOIN public.mst_distance e ON ((((a.entraning_station)::text = (e.src)::text) AND ((a.detraining_station)::text = (e.dest)::text))));
    DROP VIEW public.train_rpt;
       public          postgres    false    217    217    218    218    219    219    219    220    220    220    220    220    220    220    220    216    216    217            �            1259    25543    r_trains    VIEW     �  CREATE VIEW public.r_trains AS
 SELECT a.trains,
    a.r_count
   FROM ( SELECT array_agg(train_rpt.train_id) AS trains,
            (array_length(array_agg(train_rpt.train_id), 1) > (array_agg(train_rpt.d_capacity))[1]) AS reschedule,
            (array_length(array_agg(train_rpt.train_id), 1) - (array_agg(train_rpt.d_capacity))[1]) AS r_count
           FROM public.train_rpt
          GROUP BY train_rpt.detraining_station) a
  WHERE a.reschedule;
    DROP VIEW public.r_trains;
       public          postgres    false    221    221    221            �            1259    25548    with    VIEW     �  CREATE VIEW public."with" AS
 WITH a AS (
         SELECT r_trains.trains,
            r_trains.r_count
           FROM public.r_trains
        ), b AS (
         SELECT train_rpt.train_id,
            train_rpt.nominal_odc,
            train_rpt.type,
            train_rpt.entraning_station,
            train_rpt.start_time,
            train_rpt.detraining_station,
            train_rpt.consignment,
            train_rpt.speed,
            train_rpt.d_capacity,
            train_rpt.priority,
            train_rpt.distance,
            train_rpt.arrival_time,
            train_rpt.travel_time
           FROM public.train_rpt
        )
 SELECT b.train_id,
    b.nominal_odc,
    b.type,
    b.entraning_station,
    b.start_time,
    b.detraining_station,
    b.consignment,
    b.speed,
    b.d_capacity,
    b.priority,
    b.distance,
    b.arrival_time,
    b.travel_time,
    a.trains,
    a.r_count
   FROM b,
    a
  WHERE (b.train_id = ANY (a.trains))
  ORDER BY b.train_id;
    DROP VIEW public."with";
       public          postgres    false    221    221    221    221    221    221    221    221    221    221    221    222    221    221    222            �            1259    25553    add_time    VIEW     9  CREATE VIEW public.add_time AS
 SELECT "with".detraining_station,
    array_agg("with".train_id) AS id,
    array_agg("with".arrival_time) AS arrival,
    max("with".arrival_time) AS max,
    (max("with".arrival_time) + '10:00:00'::interval) AS addtime
   FROM public."with"
  GROUP BY "with".detraining_station;
    DROP VIEW public.add_time;
       public          postgres    false    223    223    223            �            1259    25557    date    VIEW     "  CREATE VIEW public.date AS
 SELECT a.ids
   FROM ( SELECT array_agg(train_rpt.train_id) AS ids,
            train_rpt.d_capacity
           FROM public.train_rpt
          GROUP BY train_rpt.detraining_station, train_rpt.d_capacity) a
  WHERE ((array_length(a.ids, 1) - a.d_capacity) > 0);
    DROP VIEW public.date;
       public          postgres    false    221    221    221            �            1259    25561    demo    TABLE     R   CREATE TABLE public.demo (
    start_time date,
    train_id character varying
);
    DROP TABLE public.demo;
       public         heap    postgres    false            �            1259    25566    mst_capacity_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mst_capacity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.mst_capacity_id_seq;
       public          postgres    false            �            1259    25567    mst_capacity_id_seq1    SEQUENCE     �   CREATE SEQUENCE public.mst_capacity_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.mst_capacity_id_seq1;
       public          postgres    false    216            �           0    0    mst_capacity_id_seq1    SEQUENCE OWNED BY     L   ALTER SEQUENCE public.mst_capacity_id_seq1 OWNED BY public.mst_capacity.id;
          public          postgres    false    228            �            1259    25568    mst_check_late_train_details    TABLE     4  CREATE TABLE public.mst_check_late_train_details (
    train_id integer NOT NULL,
    detraining_station character varying,
    d_capacity integer,
    start_time timestamp without time zone,
    arrival_time timestamp without time zone,
    loading_time timestamp without time zone,
    priority integer
);
 0   DROP TABLE public.mst_check_late_train_details;
       public         heap    postgres    false            �            1259    25573    mst_consignment    TABLE     �   CREATE TABLE public.mst_consignment (
    id integer NOT NULL,
    type character varying,
    consignment character varying
);
 #   DROP TABLE public.mst_consignment;
       public         heap    postgres    false            �            1259    25578    mst_consignment _id_seq    SEQUENCE     �   CREATE SEQUENCE public."mst_consignment _id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public."mst_consignment _id_seq";
       public          postgres    false    230            �           0    0    mst_consignment _id_seq    SEQUENCE OWNED BY     T   ALTER SEQUENCE public."mst_consignment _id_seq" OWNED BY public.mst_consignment.id;
          public          postgres    false    231            �            1259    25579    mst_geojson_100km    TABLE     b  CREATE TABLE public.mst_geojson_100km (
    id integer NOT NULL,
    station character varying,
    capacity integer,
    y double precision,
    x double precision,
    geometry character varying,
    in_coming_id character varying,
    in_coming_station character varying,
    out_going_id character varying,
    out_going_station character varying
);
 %   DROP TABLE public.mst_geojson_100km;
       public         heap    postgres    false            �            1259    25584    mst_geojson_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mst_geojson_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.mst_geojson_id_seq;
       public          postgres    false    232            �           0    0    mst_geojson_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.mst_geojson_id_seq OWNED BY public.mst_geojson_100km.id;
          public          postgres    false    233            �            1259    25585    mst_priority_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mst_priority_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.mst_priority_id_seq;
       public          postgres    false    218            �           0    0    mst_priority_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.mst_priority_id_seq OWNED BY public.mst_priority.id;
          public          postgres    false    234            �            1259    25586 
   mst_select    TABLE     �   CREATE TABLE public.mst_select (
    sr_no integer NOT NULL,
    nominal_odc character varying,
    entraning_station character varying,
    detraining_station character varying,
    consignment character varying,
    type character varying
);
    DROP TABLE public.mst_select;
       public         heap    postgres    false            �            1259    25591    mst_select_sr_no_seq    SEQUENCE     �   CREATE SEQUENCE public.mst_select_sr_no_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.mst_select_sr_no_seq;
       public          postgres    false    235            �           0    0    mst_select_sr_no_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.mst_select_sr_no_seq OWNED BY public.mst_select.sr_no;
          public          postgres    false    236            �            1259    25592    mst_speed_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mst_speed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.mst_speed_id_seq;
       public          postgres    false    219            �           0    0    mst_speed_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.mst_speed_id_seq OWNED BY public.mst_speed.id;
          public          postgres    false    237            �            1259    25593    recycle    TABLE     5  CREATE TABLE public.recycle (
    train_id integer,
    ir character varying,
    nominal_odc character varying,
    type character varying,
    entraning_station character varying,
    place timestamp without time zone,
    place_hours integer,
    loading_hours integer,
    start_hours integer,
    m_day text,
    start_time timestamp without time zone,
    detraining_station character varying,
    consignment character varying,
    speed integer,
    d_capacity integer,
    priority smallint,
    distance double precision,
    arrival_hours integer,
    arriv_days text,
    arriv_day integer,
    arrival_time timestamp without time zone,
    travel_hour interval,
    travel_time interval,
    loading_hour integer,
    d_loading_time timestamp without time zone,
    delay_time timestamp without time zone
);
    DROP TABLE public.recycle;
       public         heap    postgres    false            �            1259    33838 
   train_rpt1    VIEW     �  CREATE VIEW public.train_rpt1 AS
 SELECT a.train_id,
    a.nominal_odc,
    a.type,
    a.entraning_station,
    a.place,
    ((date_part('epoch'::text, (a.place - a.date0)) / ((3600)::numeric)::double precision))::integer AS place_hours,
    ((date_part('epoch'::text, (a.e_loading - a.place)) / ((3600)::numeric)::double precision))::integer AS loading_hours,
    ((date_part('epoch'::text, (a.e_loading - a.date0)) / ((3600)::numeric)::double precision))::integer AS start_hours,
        CASE
            WHEN ((((date_part('epoch'::text, (a.e_loading - a.date0)) / ((3600)::numeric)::double precision))::integer / 24) = 0) THEN 'm'::text
            ELSE ('m+'::text || (((date_part('epoch'::text, (a.e_loading - a.date0)) / ((3600)::numeric)::double precision))::integer / 24))
        END AS m_day,
    a.e_loading AS start_time,
    a.detraining_station,
    a.consignment,
    b.speed,
    c.capacity AS d_capacity,
    d.priority,
    e.dist AS distance,
    (((date_part('epoch'::text, ((a.e_loading - a.e_loading) + ('01:00:00'::interval * (e.dist / (b.speed)::double precision)))) / ((3600)::numeric)::double precision))::integer + ((date_part('epoch'::text, (a.e_loading - a.date0)) / ((3600)::numeric)::double precision))::integer) AS arrival_hours,
        CASE
            WHEN (((((date_part('epoch'::text, ((a.e_loading - a.e_loading) + ('01:00:00'::interval * (e.dist / (b.speed)::double precision)))) / ((3600)::numeric)::double precision))::integer + ((date_part('epoch'::text, (a.e_loading - a.date0)) / ((3600)::numeric)::double precision))::integer) / 24) = 0) THEN 'm'::text
            ELSE ('m+'::text || ((((date_part('epoch'::text, ((a.e_loading - a.e_loading) + ('01:00:00'::interval * (e.dist / (b.speed)::double precision)))) / ((3600)::numeric)::double precision))::integer + ((date_part('epoch'::text, (a.e_loading - a.date0)) / ((3600)::numeric)::double precision))::integer) / 24))
        END AS arriv_days,
    ((((date_part('epoch'::text, ((a.e_loading - a.e_loading) + ('01:00:00'::interval * (e.dist / (b.speed)::double precision)))) / ((3600)::numeric)::double precision))::integer + ((date_part('epoch'::text, (a.e_loading - a.date0)) / ((3600)::numeric)::double precision))::integer) / 24) AS arriv_day,
    (a.e_loading + ('01:00:00'::interval * (e.dist / (b.speed)::double precision))) AS arrival_time,
        CASE
            WHEN (date_part('minute'::text, ('01:00:00'::interval * (e.dist / (b.speed)::double precision))) >= ((30)::numeric)::double precision) THEN (date_trunc('hour'::text, ('01:00:00'::interval * (e.dist / (b.speed)::double precision))) + '01:00:00'::interval)
            ELSE date_trunc('hour'::text, ('01:00:00'::interval * (e.dist / (b.speed)::double precision)))
        END AS travel_hour,
    ('01:00:00'::interval * (e.dist / (b.speed)::double precision)) AS travel_time,
    ((((date_part('epoch'::text, ((a.e_loading - a.e_loading) + ('01:00:00'::interval * (e.dist / (b.speed)::double precision)))) + date_part('epoch'::text, (a.e_loading - a.date0))) + date_part('epoch'::text, '12:00:00'::interval)) / ((3600)::numeric)::double precision))::integer AS loading_hour,
    ((a.e_loading + ('01:00:00'::interval * (e.dist / (b.speed)::double precision))) + '12:00:00'::interval) AS d_loading_time,
    a.delay_time
   FROM ((((public.trains a
     JOIN public.mst_speed b ON ((((a.nominal_odc)::bpchar = b.odc) AND ((a.type)::bpchar = b.type))))
     JOIN public.mst_capacity c ON (((a.detraining_station)::text = (c.station)::text)))
     JOIN public.mst_priority d ON (((a.consignment)::bpchar = d.type)))
     JOIN public.mst_distance e ON ((((a.entraning_station)::text = (e.src)::text) AND ((a.detraining_station)::text = (e.dest)::text))))
  ORDER BY a.train_id;
    DROP VIEW public.train_rpt1;
       public          postgres    false    219    217    219    220    216    219    216    218    217    220    220    220    217    218    220    220    220    220    220    220            �            1259    25603    wh    VIEW     !  CREATE VIEW public.wh AS
 SELECT a.trains,
    a.r_count
   FROM ( SELECT array_agg(date(train_rpt.arrival_time)) AS array_agg,
            array_agg(train_rpt.train_id) AS trains,
            (array_length(array_agg(train_rpt.train_id), 1) > (array_agg(train_rpt.d_capacity))[1]) AS reschedule,
            (array_length(array_agg(train_rpt.train_id), 1) - (array_agg(train_rpt.d_capacity))[1]) AS r_count
           FROM public.train_rpt
          GROUP BY train_rpt.detraining_station, (date(train_rpt.arrival_time))) a
  WHERE a.reschedule;
    DROP VIEW public.wh;
       public          postgres    false    221    221    221    221            �            1259    25608    your_table_name    TABLE     X   CREATE TABLE public.your_table_name (
    id integer NOT NULL,
    duration interval
);
 #   DROP TABLE public.your_table_name;
       public         heap    postgres    false            �            1259    25611    your_table_name_id_seq    SEQUENCE     �   CREATE SEQUENCE public.your_table_name_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.your_table_name_id_seq;
       public          postgres    false    240            �           0    0    your_table_name_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.your_table_name_id_seq OWNED BY public.your_table_name.id;
          public          postgres    false    241            �           2604    25612    mst_capacity id    DEFAULT     s   ALTER TABLE ONLY public.mst_capacity ALTER COLUMN id SET DEFAULT nextval('public.mst_capacity_id_seq1'::regclass);
 >   ALTER TABLE public.mst_capacity ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    216            �           2604    25613    mst_consignment id    DEFAULT     {   ALTER TABLE ONLY public.mst_consignment ALTER COLUMN id SET DEFAULT nextval('public."mst_consignment _id_seq"'::regclass);
 A   ALTER TABLE public.mst_consignment ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    231    230            �           2604    25614    mst_geojson_100km id    DEFAULT     v   ALTER TABLE ONLY public.mst_geojson_100km ALTER COLUMN id SET DEFAULT nextval('public.mst_geojson_id_seq'::regclass);
 C   ALTER TABLE public.mst_geojson_100km ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    233    232            �           2604    25615    mst_priority id    DEFAULT     r   ALTER TABLE ONLY public.mst_priority ALTER COLUMN id SET DEFAULT nextval('public.mst_priority_id_seq'::regclass);
 >   ALTER TABLE public.mst_priority ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    218            �           2604    25616    mst_select sr_no    DEFAULT     t   ALTER TABLE ONLY public.mst_select ALTER COLUMN sr_no SET DEFAULT nextval('public.mst_select_sr_no_seq'::regclass);
 ?   ALTER TABLE public.mst_select ALTER COLUMN sr_no DROP DEFAULT;
       public          postgres    false    236    235            �           2604    25617    mst_speed id    DEFAULT     l   ALTER TABLE ONLY public.mst_speed ALTER COLUMN id SET DEFAULT nextval('public.mst_speed_id_seq'::regclass);
 ;   ALTER TABLE public.mst_speed ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    237    219            �           2604    25618    trains1 train_id    DEFAULT     s   ALTER TABLE ONLY public.trains1 ALTER COLUMN train_id SET DEFAULT nextval('public.master_train_id_seq'::regclass);
 ?   ALTER TABLE public.trains1 ALTER COLUMN train_id DROP DEFAULT;
       public          postgres    false    215    214            �           2604    25619    your_table_name id    DEFAULT     x   ALTER TABLE ONLY public.your_table_name ALTER COLUMN id SET DEFAULT nextval('public.your_table_name_id_seq'::regclass);
 A   ALTER TABLE public.your_table_name ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    241    240            y          0    25561    demo 
   TABLE DATA           4   COPY public.demo (start_time, train_id) FROM stdin;
    public          postgres    false    226   �{       t          0    25515    mst_capacity 
   TABLE DATA           K   COPY public.mst_capacity (station, capacity, station_code, id) FROM stdin;
    public          postgres    false    216   @|       |          0    25568    mst_check_late_train_details 
   TABLE DATA           �   COPY public.mst_check_late_train_details (train_id, detraining_station, d_capacity, start_time, arrival_time, loading_time, priority) FROM stdin;
    public          postgres    false    229   x}       }          0    25573    mst_consignment 
   TABLE DATA           @   COPY public.mst_consignment (id, type, consignment) FROM stdin;
    public          postgres    false    230   �}       u          0    25520    mst_distance 
   TABLE DATA           7   COPY public.mst_distance (src, dest, dist) FROM stdin;
    public          postgres    false    217   ~                 0    25579    mst_geojson_100km 
   TABLE DATA           �   COPY public.mst_geojson_100km (id, station, capacity, y, x, geometry, in_coming_id, in_coming_station, out_going_id, out_going_station) FROM stdin;
    public          postgres    false    232   ٞ       v          0    25525    mst_priority 
   TABLE DATA           :   COPY public.mst_priority (id, type, priority) FROM stdin;
    public          postgres    false    218   9�       �          0    25586 
   mst_select 
   TABLE DATA           r   COPY public.mst_select (sr_no, nominal_odc, entraning_station, detraining_station, consignment, type) FROM stdin;
    public          postgres    false    235   ��       w          0    25528 	   mst_speed 
   TABLE DATA           9   COPY public.mst_speed (type, odc, speed, id) FROM stdin;
    public          postgres    false    219   -�       �          0    25593    recycle 
   TABLE DATA           X  COPY public.recycle (train_id, ir, nominal_odc, type, entraning_station, place, place_hours, loading_hours, start_hours, m_day, start_time, detraining_station, consignment, speed, d_capacity, priority, distance, arrival_hours, arriv_days, arriv_day, arrival_time, travel_hour, travel_time, loading_hour, d_loading_time, delay_time) FROM stdin;
    public          postgres    false    238   ��       x          0    25531    trains 
   TABLE DATA           �   COPY public.trains (train_id, nominal_odc, entraning_station, place, detraining_station, consignment, type, delay_time, e_loading, date0, change_station) FROM stdin;
    public          postgres    false    220   Ũ       r          0    25509    trains1 
   TABLE DATA           �   COPY public.trains1 (train_id, nominal_odc, entraning_station, start_time, detraining_station, consignment, type, delay_time, start_time1) FROM stdin;
    public          postgres    false    214   ��       �          0    25608    your_table_name 
   TABLE DATA           7   COPY public.your_table_name (id, duration) FROM stdin;
    public          postgres    false    240   B�       �           0    0    master_train_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.master_train_id_seq', 50, true);
          public          postgres    false    215            �           0    0    mst_capacity_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.mst_capacity_id_seq', 90, true);
          public          postgres    false    227            �           0    0    mst_capacity_id_seq1    SEQUENCE SET     C   SELECT pg_catalog.setval('public.mst_capacity_id_seq1', 42, true);
          public          postgres    false    228            �           0    0    mst_consignment _id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public."mst_consignment _id_seq"', 3, true);
          public          postgres    false    231            �           0    0    mst_geojson_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.mst_geojson_id_seq', 8458, true);
          public          postgres    false    233            �           0    0    mst_priority_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.mst_priority_id_seq', 14, true);
          public          postgres    false    234            �           0    0    mst_select_sr_no_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.mst_select_sr_no_seq', 37, true);
          public          postgres    false    236            �           0    0    mst_speed_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.mst_speed_id_seq', 24, true);
          public          postgres    false    237            �           0    0    your_table_name_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.your_table_name_id_seq', 2, true);
          public          postgres    false    241            �           2606    25621    trains1 master_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.trains1
    ADD CONSTRAINT master_pkey PRIMARY KEY (train_id);
 =   ALTER TABLE ONLY public.trains1 DROP CONSTRAINT master_pkey;
       public            postgres    false    214            �           2606    25623    trains master_pkey1 
   CONSTRAINT     W   ALTER TABLE ONLY public.trains
    ADD CONSTRAINT master_pkey1 PRIMARY KEY (train_id);
 =   ALTER TABLE ONLY public.trains DROP CONSTRAINT master_pkey1;
       public            postgres    false    220            �           2606    25625    mst_capacity mst_capacity_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.mst_capacity
    ADD CONSTRAINT mst_capacity_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.mst_capacity DROP CONSTRAINT mst_capacity_pkey;
       public            postgres    false    216            �           2606    25627 >   mst_check_late_train_details mst_check_late_train_details_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.mst_check_late_train_details
    ADD CONSTRAINT mst_check_late_train_details_pkey PRIMARY KEY (train_id);
 h   ALTER TABLE ONLY public.mst_check_late_train_details DROP CONSTRAINT mst_check_late_train_details_pkey;
       public            postgres    false    229            �           2606    25629 %   mst_consignment mst_consignment _pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.mst_consignment
    ADD CONSTRAINT "mst_consignment _pkey" PRIMARY KEY (id);
 Q   ALTER TABLE ONLY public.mst_consignment DROP CONSTRAINT "mst_consignment _pkey";
       public            postgres    false    230            �           2606    25631 "   mst_geojson_100km mst_geojson_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.mst_geojson_100km
    ADD CONSTRAINT mst_geojson_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.mst_geojson_100km DROP CONSTRAINT mst_geojson_pkey;
       public            postgres    false    232            �           2606    25633    mst_priority mst_priority_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.mst_priority
    ADD CONSTRAINT mst_priority_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.mst_priority DROP CONSTRAINT mst_priority_pkey;
       public            postgres    false    218            �           2606    25635    mst_select mst_select_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.mst_select
    ADD CONSTRAINT mst_select_pkey PRIMARY KEY (sr_no);
 D   ALTER TABLE ONLY public.mst_select DROP CONSTRAINT mst_select_pkey;
       public            postgres    false    235            �           2606    25637    mst_speed mst_speed_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.mst_speed
    ADD CONSTRAINT mst_speed_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.mst_speed DROP CONSTRAINT mst_speed_pkey;
       public            postgres    false    219            �           2606    25639 $   your_table_name your_table_name_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.your_table_name
    ADD CONSTRAINT your_table_name_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.your_table_name DROP CONSTRAINT your_table_name_pkey;
       public            postgres    false    240            y   ]   x�]���0D�3Ԃ#､���C$��h�M-'��J���
�A>'9 �0e�X�k`'�g�~�,(����U�]0SL���徘�\[+�      t   (  x�MQK�� [Ǉ�i�|)L !$"0UG����(���~?��Y�u�V[1l��4:�*��qu4�-��'��L6�g�o��]��+R����NH�r��ӍT�\���2b5L��v�-��.�R��Im̽-&
�;�=�+�YE^9�>%s����s�g�!�/�^g�k�\�,�3�,�c� ��t̵�3i Q�.Ƣ�8:���
yTO�/��E��3�`^��W��1���M!�����V�1�Ę�H�-8�S��&�/6|�X���"�M�^�~M%Q�ﭬ���?�\|0      |      x������ � �      }   b   x�-�I�P��U��S��$�|%����ɩ
%�v��W*=�Q۞��9�eO��l;�Y;Z4�3�s!*�5e˖��G��7Z5���      u      x�u]ٲǍ|&?�D��㕩!)Q��"���D���� �D��8�Ĺ]����Ϸoo_��������~��׏o�u~�τ���:߯�����_��mz�M����O��}�m�����}���n?����_�����ӻm?^�U��_?|�_�'��/?����?��n�����?~��ۏ���m~�����߼'��:��y����/_��n����>��ۏ��n?[ǿ|����ӻcه�z��������{]m���������y�Z�������bZ�ޡ���A�	����ݼN�kn��O?��j_����F�׏�����Zڏ����/o����u�������Ƿ_�>X��گ����}��߯������W�������}Ʈc}-�Կ�f=Z������_>Ŋ̗}�/�/�~�m����<m�(�d���ǵ��A����o��ڮ��_>����>u���B~�����7����_W��例6�۾���}�!�m��l�8�-�k=�d$���εI����bih���zop��xhB<8'�X	H�ÿu<��N�s�$"�vn���)ٰؔ������n��ñ�2�6!��v],a��:��[N�c{��i�b�6gU�ŶL�:���Ź=���8����}h�����uXWPc��ױ�7v�7�n@�q5��a�IoA�X&kc�I�XlO���'A��zm�"&C�}m밶��r���t�즎W���دa����������?��O��p.�6J������ۉ���Σ.Q���j�4|__@/Y3q�� mM��������?����-����q/8b~���z�����%�#ا��ص)���|��@����kk8��G��R��0��7L�Q�a:c�.1��� �i�?W0��͊�GG}�Xm_���t����4�����A��>�HF�>Z���n�뾞�@�j��t>�I{���`d�w:�V�U��9Y�5ck����6��&�1�2����c2������V��=ϟ�~0���}��voEkl%)Rs;(Ѹ+��%%�g�y7\t�m�����m����m;^k�y����<Nof(��)Q�ܾ�3���ܣ7 �^�((���sZ���l&��L���<�~2v3[�7��u��5	����w)�\������ǹ����:�Zjn�)f�y�r�m���\쯖sXT0�,�{X�W��b����^��H�X��B���AD��␫�A�o?�#Cw�z�r�-��
�ݶ��ò6�-��}rH��Fi�9!�!�#ژ_��@3H��M͈�cg�D�-fn}(ص�3"�ly��9ye�D�n��v�S_$��m-��ش�RنIX\��Є$�<F���d�Pj-�X�1mz���i��!��q��AYJژo��o�3Wi�㎿~(��o�4w�L���Z��6�i�>�$����X�m���g�>ڨq�Mx��T�',ڻ���$�jqHs\ux���ы�."���^�Y�)�I2��p	%l��"{>a�ܺ�p��/Ȋeޝ��ɋu���̰�FGr�6S�x��tiidu��pE�f
��#��''<i�Zy�&��S9}����h�	g���n_!a��cRf�o�[�	�\��5��ـ�>�N�k�P�-"����m�>ۂ֭���o��0���-��N���gA,����vfBιwTT����1}:#���0�s��LmN�Q�'�U��"��Zȝҁ^����>� �}�.���8m�l�O�M�'�!J����"��=�"�[�gc"�g���߉���� K"n���bɸ��2�-J~��$�ꉠ�"1-~��g7��n��e�v��Ug�v�~c?���y*�㏒�;L�8�F����o�]?� ����1�s]N���9�/sЖGs-T�~��
�f�سɤ�y���FR���xji=��(;��#�j�v�ޞؗ��њI� ��Lz:����wI�����*�_�c��� ]�9|���Q\|RIJ�K8��%�ÝZ@I�}�� �A���V�:LpcF,�6{|�F�cN�U����᪩tRm�}�vΆ�L�3��ina��9�j@.��J�����A�]Πm�l���WbA��lN_���6z��K��v0'et �%'�ܿl���q.�ȱ��+e�p0E�٦���R$�(i�9 �}@�B�,�7£^��P�^�f{Ԭ�(��Ye�1�{uG_^&Ɯ�M_(o��)Q���Y�J%7U�4�Ts���1Ss]z/�	��̓R�N���&� 5���I�:�=G�Zo��<�����[h-Ej�\�_��zJB(ܸۖ�M.�?��
M�#��ъ�־+l�թcł���x��Ս��{�<��,8���T���qK�m�8�">n��SS��wd������`��Z�l�oE����@b��Hmͭ޸4駵���.	�vo��m���ᯋ�7;E6�.��ʨ9Cjv���_3�}�i��;�m��~�\0�cVS����F@.��[ją���~�'��Zr���rរ�!�,mn��"ꛍ�՚�₩H}W\8{�l���Zra߫�h������*��2(AH�.�L6c> G3)+>0ᛂLD�*��L#\O|`#��1n	�&1��$��ֿ�i�=\d�J�2�/V���,@�B�kJD,�p� ��TU`q����|��S�֕H�Ma�T`v\�	��P{��#q�qg��\��j$�#��^�M���Փ��W�A����o���?�k�H�'�\4�����
�w?�VԿxU˖A�d����1��A:�!��Pw�T�-��V��@WRTl�1�߳�(R�E&�?2jbS�W�P��f� KA0g�D!ZH��Uc,�,rN���걼)�7�YySG�%I�(��f�9�[�U'��bW�	�Y3`�"��:�e���i�Y��ʍ�jf��M��Z
Pc3~��R��C(���6��Oo��Rċ{[�� ��>���t�V��vng�Q�̨c�Q�`��3���# �H�i��!
u$���zɊ8� +g�@�\	�r$�$D��^�Y��hAp�)�o\%
n7guY�pU��U�N0My{����ܽ�͎��p/��U��5�[F�۔��W�Äʪ\�~���Y1{�g8��8��+�']C�ʇ'e�Z�i9�n��m�cܽ�H�k�PZ�$��v�r�5�/^=�VQ���c�-sS��ʻzոs��f�e���`�HE)(ꔠ��p�d�TP�"a�Up�.�H���+^�C�����6I#�iu"��f!�`1*\.������&%\���r�?��cmNe~�K��a��0�}D����'�mB�-q`^�EKdf��"���7���o��5�n��r�g_*�$Ӆ����Q� �\;N�����a2�����4��u4I3N>ӭ�����Һ*uF���2M��y����)�"�����Ԇ��u�pu�24��u����s���d]��-�������q��2X'�ZK��T�i��'ZD�(%aԆO&4y�p���oY7G5w�2LeL[�,�%O}\m�Qp��Q�F�c3��5���Տ<F1�h������l�N�d�u��
7��im�C{d�����(�i�8�Uڤ�%�j��m3D(�%hl��{-�쐟Bt�Qٚ�ׇ�
��X�2w���EA^.����X%�)}:�J��(�z��2^_�`�'>�;8�K��<� �G%H�&J� ����h��&a���s��C��b!0&a%�<�M���l�K��H���>��dd�L9��e��éBӇ���g��H��a+5��q�˄�2-��!��z�u�W�/	Fj�ȵ�}Z�2�"՗e��S	ep�B}I��C�e�3l�<I����@�T��L��k��u,�+4�7��.A
FƠ�8e�c��|�鯡�*�bL�$<&��S|�)]B��,4�;#���肼V�I��BE�,�]�x%��3,�z�Z4�K�'�9�������[��$6L���yW7�J��X�=�<��mܙm��6��C*m� �V�|    1�����e�É���t�y����^[��/:/A�:����W*m�|t��U_���ޝ�.5���JF�l.Y+�G���c��D�=��������ZK�6��DG9V���3QҤ(�Ɖv�3��`$�p���A*�IT(=?FX.b�&*�1K)� G��%�aq�@^�5�O�o�9���>����6VFk1�gK�������h^�i~��H���ѵ�ɹ����7�\�kT�,�6����VHK��V�Hkn��'k�չd�|�+�yx�J�TT�Y'��ظ�PZ���-_�:N�EC�jsx<�H�1j��BT��5�@G���+Hx-!*F�(�p�"�c��0�7E1� ���H$��Bdˀ�z����M�`�E�n@��i��h���8���d^������C3�4���v1������{�g����y։'.O�u���3:A�����<�|�h�z���Op%�2��J��,;�܀	�f?Kx�ZO]��J�9��0������eM�� \˂�);n� nNZ~�yhgu�aa�Z�W����#�����u�&�� eIVd���#	��G���ϧ��V�@Y�X�']�e���Ł��l��p����r��&̓��]�]��g{��+�M=�c��,�Z���kM�� ��y���M�x��dK��YN�i��^gN�n�.r�蕴�b�����W[�+{;���V\:��Fq-�1��j�>྿�
��b��!D=��{N�s��-��]�V�x��*Y�X��?@�yDa@�~V� �F�sq���,��|(�v ���[��홅b_3��X�ʌ(4m����\�𤸿g/|�\��vl�*X���4��"	�p���Ɓk{Z^�݅Fx���>bG#��s��b�����+c�gR}?יR'�����T|���kҡ�˺xGSZ�ʕ_H���l�U/����d|���I����<u��� �[���x�y�C���Z�γ��tP ˹A�P��p�MP:ϣ<���<� \:�+��:�LP�<�eM�t�~.A�<���E�<�y`4�y~�u~��y+�~���M��8��*���a�V��懭����Y���h��`�,۞����]�#����8�a����r�do����Aө��v�E0����zp�D���k�ON�=Q	�i=ߐxTz^��� .�:�*�;x����Q��Z.�j	��%ہ����5��v��&eg5S���,� �B�8���hq�����c�9��J͙ʉ��w���q���퇎�o	*�MK�*���nd毚����E��6t���P�}?Z�8���&��X�[�n�8�R�7#���O_ƫ���5�{�ӟ��e�ٻ����D,>�s��`���|�xSm��B�#Q�W(k��5*g�uR�M�q_���伞CԜ��)ˊ*m���W%Zʎ=�rgP�D���u�K�yxL\:�C��rj=s��[�{d	kK�ђ@�x�/�~8����a�up?϶������wW-J��gӫI����1���T�M����e�6��hĄ-�q�.�k��:��}�E lin��1b��L���5�Aj�͵�XM��{�Ԅ'�|4y��4a҄w������>�d#]x[��A���Sx҆W�$�Â�&�` u�M$
���K*,@�R��� �MVu\8I�cR�#�JT���ɯx��a]4 3��b�&H�y �u �F�7�t�a��CWt�āg�ݠ��.�(@\q쏿�����#6�>j��h��.��y�q�^S�(3,&��?�^�,�*���sBz������\<H��u(�7��@�7�4 ڈ���ğ�7�����7n�S�G��ĕ	�E9Ԉ�P�hQe��P�D��Ted����pQgl5�E+�hE@)d?��	Y"��rێ��X6�aE��9<�3�˔#h:����L��N��=N�k.�f�R���lY�|	.���T
F�S��HSȑ��Z?�]�(�#g�55�����}���0�ؑ	��
�+EY7Sx���x҃`���X&܇��V	�A��"�b����-xG���̼�z,T�o�J����ل�B����ˍ�sM`{��j3HN0����H�'�8¢!�AX�m9'���	:f9�����:�R�j�#�G�~9���:f'y��l�t!�!%'V�@�@�D<vU��Mm��<�բ5Rx�n�H��LF�E
�@J�q��/R0���QT���N�I	>hCP��;�GF� ʂ�M���%Qby�7.�K2�f��oE$�'�P�M���jU�I�e_I�M.����-��C_-�3�'^�F�AeK�PA撲%'�-��`$;_<����	��q��AN���mX5Ug��V9$�s)�
�'3��^] .O�,�
��0�b��7�"A�k��et�%���.���6
|�|=�f���|�	`���4�G���`�   �^4��
� 
��>P\4y��>/㵫�]���,���S�5M���+�i�dX�K����ً`��8�"�;e+8����	lj�k?�\�;�&�\��c�a�>�>U�b��[������
�~�<[V^+��rʡ�n)ԡ�{�<?�����Z�����IK�J����D���iLI���>�D >V�x���'�$y� O�HJ&���".>�b����J���5���#I�.��I����1�!�4�@$aI]��*�@�O[5P��_`N��0qvV����B5�9R�5`T5�n<�A�� ��L��w����X�����hq���{j2O��x��z�1Ƽ�HR�]����S��߾Ej]s�>dG�Z|�]�fR��D#�����E-�w)	������W|�L��V|IR�Y8}�A�)��k�U�r�p�Z�.� -<)�+q4���zRR����Pݯ'��aE�|��Ok�5rm�p5C�W��,�H��*8v�5�:��8Q�qFMMr�5�� ��V�'/U���X48E7�Ͼ��B�S:e��M(Ɛ��]!���]�*pּ[��&���ݒ���.9��L|���Ǔ�x���f��@,�4P|!�h�'>�G|dQ�L�Y"����M��'8���vxl�p�w��A��Q�E^~#.���O�Ywq��pyk(֮9,w-
H�"(��+mٕ`�2|GIF.���-=kr�/Ǧ�;��E&^�P�ޑe��atfL�!G�o��!cJUi���n�3U��P2|�"���@n>[�:/l�=��LiM���W<$���?_ уx�\�N��,���Bx{ZO_J�`I��G)y��Ǆ�)x�I���gi��3�x�C�o.��F�$�3�*I���j���,.bo3�	wXa�V�A�i�W�z�I��_���P�Q�fbxm=I���R�*�z�3s��� HO5�c����G��9�]���)���U0-ՙ��}�ɫݽ��ǡ�e��Gj-���F�}s���ठ{p��?R�p���
���7�S���ZN�8�WcS�p���d
��վ��y�7�L�-sJPL�5��qý�� HA��p�:��]Qv[^.�%.��O�˺㋛�:p�P�]=
��5Q�l���"�ÉMI�Æ���I����5�����[����["�[(��Hg���S�{X�r��h�:s�p!�����S]˃I�F�i�h�-a�̑m_���S�QM�OZ�O�4����&�G.x��	u�Gɛ������&{�����&�޺,X�0x��It��К��c��SUmMܹ�:��#M֎f�A����]�!��KKR5�I7N��ƛ=ê����.�X'��Ji�
�@���}^3�+�mz�`3
V� �A��P¬�y��+�dƙ� ���H!����"�֕Q�>�
��(׍����E<p��g�VkXh����zb��Z)��6����.�G!�I�z���*c� X�^2��a�+��uxO�*���f�*`�� �gxD�(�g�V��� �   �J�5�U��7�U�	����p�T�V$�-�\ ԭ�Pv��u
`Y�6�F(ZC!.��Q5�gFKn��Vņґ\xw87�f��Ʊab��p����~"�L}���T�>[N��&{�a�\	�<L���6���������e������=���?=���?��.�-�^�߿�?pEU�         P  x�mW�nG}}�>ր0 g�C�q��bYd�A� ����ᮤ��6��0�<7��i��v���Z*=[뚌��^ҏ���4���d�Y�t�fCej�r�Nb��<�߇�����r<�V��a�ܽ�({vWIZ��۵�n��`�*C)Z���JĎ�����B7����z�G��[K��q�u���g^�
աx��-I�"�_�zz9�?�m*1�Z񤞩���T�Zj��HǓu��j�$j���ϒ6���%���JҘ���"�9/��&�Q�\H��?�c��!*2)�K���X
w�\*>dѡ���
lJ��0ui����<�06�!�IK6����(Hilͥx��I�J�F��CMI��8^��q3�5��T�E��𦬊ᣄ��T)[w�Z	*=}nw�ͥU�MϦ�<Au)�w*��=�6a��$�O�cU�<��K�\�&4U!�k�NZ!�/u%`��h6��V�=`����|-q�y��̖NA3�YXa%J#��3�2{`�rzޞ?���\�@G@���V��A�g�Z5y�+1���nEK�O�q��5w�	Rb[X�h�4�l	��vW:�P�����8�e�=:7m鴹u��a�:0�A�nM���������u�8\�'hU�,U�3T�X��@����xBP�?�T��/�5�"o6��ٝM��s��,�'t&�"�<���g���NP���
N��N��tGIXIZ(�>�dM��=��1�fq\�|U7��!jĳϟTk�pխ����������i�qX���xz�^4��d?<���fְ
�ܐ��bC�dJm=�����[�/\��x>���Mmݢ� 2��abHP	�kH`����/C���q�<?%���i�AoaY-��u�U�F�tiΔ�
{w�\�_v����ӓ���!��p�dU)�}�W�Cm���}�A*�>���}i}`xG��X��͟bk�b�]�*�%XYv��C`����i,ȅ��P�[�a�T�ͷ������n~lj���S��)T��*��5��#`+��Z�˾�B��z�h&�Q�d�-�8�K�L�
b�K~�@Mu= s�4��If�ۗ�V�E���,�����}���}���K�65cS*��z/��~����|P:���8[��Ұ nYnr��c�!yD�[�!�WnK����Ҹ�E�����8�m��⮹���B6��4�9H�8����!��8Q���Pz�t����KiK�;-�@U�����	��]z`k\���¾��+�z���z��z5����X�W!N0bi�X��w9:�,�,8:pu9p�U�Fr� ���y���*��Q��Kؾ�pA�谒p��@+3����厍�"�s���-&w� {��bNkP6#�,P�wp��	����l������^!kf�O���zw��X�pPոũL�O#�p~4?Sn���&K]�~=\A\�/>��Sp�$�q����8�m:WKh�j�[!ncl\$�Lj�,���k�|�]�.�\��b��@����%�a^������B=ԉj%���
l��U��|�w�1]\\�t���\����g~�)�	�UWn��<X�Ϋ��_w�Y      v   P   x�%�;
�0@���)rq��QA�`!��?�aS�(�9T<��̊5�f0f��0;N��Iђ%Gys<SN�����W�n      �   �  x�URAr�0<��t�&m��]l0�1v3�d���E�, �h�Z�����8�o;Y����D:�0帡h_D�]�h7�L�"وyC�.D�����<Q��&ҎACb���^��$J�@$`v�D��6{#Q�G� S�dى!5�
����E�L������ڭ ʹ���+�r)JK�
���\D'����~�T�Qم��W����^̋�+�r,���?�QOe|�qGъ/v0z��J��,�K�V5����^���/UM�u��rh�[��rh��T$������\�m��]�+n��p�Fh�Թ� ���+/��Q�%К)�I��v��w�g�r�+���1���a�nxe�g4sZ���Q�Γ��<y�+T��@i�w�jR�7��?��T      w      x�-�I�0C�5y�B��$˴=@:oz�s���{�?a���np8�B� M�b:o�!��2^����W�	ٸI�K�H�l�&U�����Φnk�H;����M���3��Z�K����/M�ut~O$�5#�      �   �   x��ҿn�0������پ�����Q�K�+���:&��HQ��Ͽ(&�����n�^��e��A]Q��]1D �y|���ZR��
�������	��@s�1���m�\�K;�Tq]�������!�kn����vqfz`��H��f�{5�����42�sl�'��x���Ỵ[�.fh��<��l.�U͇~VH��$��M�`4���Ϝ�~���E�8�[Eo��I���V/
M�� ���      x   �  x���[n�0E��*��"? ��@1/��(R�����@x*�5���\{�'r&�EC*�ZN��������4���O���q�1��c��1��+�">��I�'Ta��D�]�kx/2#�(��f9%\�*Ȁ��e9RJ�	HPs��a�����-��c}�9�;���� ���Z����&!	�j����=�w�O�ߞ9�Ag ��M/�l=;w�ֻ)�ptQ���-(4TPD�����W���jvw�n�O\���8ˮ��}�o,�,n��;Z󸢋�_�dG��@Yp�4((�)�G-O��3������*����7ORB%5��k�[�?��<A=�6c����qt �o�@�t�匤�>�
�����^!;-�-�,�!��f	;�n�x���C����G(�(�t��x��wfV�0���&o�lӚC8�O� ��yȈ��w7��>��      r   �  x�u��r� ���)�v��Z�ۘTb"f��q���]��L�>���N���}Mr�Ċ���(�Hg�
GR���I'tC��\�;o�(g���hp�BO�Lu�E�נ������UݶWr��o���E���ɠ�Y9��^�����ٻ�l�%c�Ď���`�U<<z����PNM�-vNFd�������R�iJ�H7��M�b�
���]�HE'LN����B�ot�&|*cZ�l�j�����TUֻ���l6��Tj�C�1%#'����P�>�t����^�a*�$r�����x�9)�d��r�A�7e;�,�Vr��F�o�Z(L]�BC gצ�J���!���tN9G��7�|�ٌ������b�霆,6����q�r0`����8������h���R�]�      �   &   x�3�40�26�20�2�4UHI�,V02rA"1z\\\ u��     